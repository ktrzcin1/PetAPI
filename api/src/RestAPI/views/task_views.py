from rest_framework import generics, pagination, mixins, views, exceptions
from .. import models, serializers, permissions
from . import common
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
import datetime
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

class TaskListCreate(common.PermissionMixin, generics.GenericAPIView, mixins.ListModelMixin):

    serializer_class = serializers.TaskSerializer

    def get_queryset(self):
        queryset = self.request.entity.tasks.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        '''POST /entity/<pk:int>/tasks or /tasks when authorization will be working...'''
        for key in request.META:
            if key.startswith('HTTP'):
                print(key)
        kwargs['pk'] = str(self.request.entity.id)
        #from request get and split task, jobs and files data
        task_data = request.data            #Retrieve data from request
        task_data['entity'] = kwargs['pk']  #Add entity info/id                    

        jobs_data = task_data.pop('jobs', [])       #Retrieve Jobs info
        files_data = task_data.pop('files', [])     #Retrieve Files info

        # task_data     -> dict with task data only;
        # jobs_data     -> list of dicts with full info about job
        # files_data    ->              -||-                  file

        #Creating Task
        task_serializer = serializers.TaskSerializer(data = task_data)      #Create serializer with task_data
        if not task_serializer.is_valid():                                  #Check if data is valid
                raise exceptions.ParseError(detail=task_serializer.errors)  #Throw error if not

        task_object = task_serializer.save()                                #Create object from serialized data and save it in databse
        task_id = task_object.id                                            #Retrieve ID as it is useful to prevent hitting DataBase
        
        # task_serializer -> serializer object, not useful later
        # task_object     -> Django repr object of database Task record
        # task_id         -> ID of created Task

        #Creating Files
        file_name_id_map = dict()       #Empty dict, used to map file names to ids

        for file_data in files_data:                                        #For every element of files_data

            file_data['task'] = task_id                                     #add task id to file_data, it allows automatically binding file with task by serializer

            file_serializer = serializers.FileSerializer(data = file_data)  #Create serializer with file_data
            if not file_serializer.is_valid():                              #Check if data is valid
                task_object.delete()                                        #Delete task if not
                raise exceptions.ParseError(detail=file_serializer.errors)  #And throw error with info what went wrong

            file_object = file_serializer.save()                            #Create File object from serialized data and save it in DB.

            file_object.path = str(task_object.entity.id) + '/' + str(task_object.id) + '/' + str(file_object.id)
            file_object.save()                                              #Generate filepath and save changes
           
           #Check File name uniqueness and update name <-> ID map
            if file_object.name not in file_name_id_map:                    #If name did not occurred earlier       
                file_name_id_map[file_object.name] = file_object.id             #Add name as key and ID as value
            else:                                                           #If not
                task_object.delete()                                            #Delete Task
                raise exceptions.ParseError(detail='Duplicated file name ' + str(file_object.name))                    #Throw parsing error

        # file_name_id_map  -> file name <-> file ID map
            #it helps with file serialization

        #Creating Jobs    
        #Function mapping file name to it's id, it uses file_name_id_map, throws Exception if name is not specified
        def mapper(file_name):
                if file_name in file_name_id_map:           #If file name is in map
                    return file_name_id_map[file_name]          #Return its id
                else:                                       #If not
                    task_object.delete()                        #Delete Task and rise parsing exception
                    raise exceptions.ParseError(detail='File name specified in Job but not in files section: ' + file_name)

        job_objects = [] #List that will store tuples of (job_object, previous_data) used later to make previous_job assignement 

        for job_data in jobs_data:                                              #For every dict of job_data

            job_data['task'] = task_id                                          #Add assigned Task id
            job_previous_data = job_data.get('job_previous', [])               #Save previous_jobs id's list to job_previous_data
            if 'input_data' in job_data:                                        #If there is input data
                mapped_input_data = list(map(mapper, job_data['input_data']))       #Map names list to ids list
                job_data['input_data'] = mapped_input_data                          #Swap lists, it allows serializer to automatically assign Files
            
            if 'output_data' in job_data:                                       #If there is output data
                mapped_output_data = list(map(mapper, job_data['output_data']))     #Same as before
                job_data['output_data'] = mapped_output_data

            #To this point job_data has mapped input/output data tables. Info about previous jobs is in job_previous_data list

            job_serializer = serializers.JobSerializer(data = job_data)     #Create serilalizer object
            if not job_serializer.is_valid():                               #If serialized data is not valid
                task_object.delete()                                            #Delete task
                raise exceptions.ParseError(detail=job_serializer.errors)       #Rise parsing error
                
            job_object = job_serializer.save()                              #If data is valid, create object and save it in DB.
            job_objects.append((job_object, job_previous_data))             #Add (job_object, job_previous_data) tuple to list

        for job, job_previous_list in job_objects:                          #For every tuple in job_objects
            for previous in job_previous_list:                              #For every element in job_previous_data list
                job.job_previous.add(task_object.jobs.get(saved_id = int(previous)))    #Assign appropriate objects from jobs assigned to task
            job.job_status = 'CREATED'                                      #Change status
            job.save()                                                      #Save changed

        task_object.task_status = 'CREATED'     #Task ready, change status and save.
        task_object.save()

        return Response(data = serializers.TaskSerializer(task_object).data, status=200)
        
class ListTaskFiles(generics.ListAPIView):
    serializer_class = serializers.FileSerializer

    def get_object(self):
        filter_kwargs = {"id": self.kwargs['pk']}
        obj = get_object_or_404(models.Task.objects.all(), **filter_kwargs)
        return obj

    def get_queryset(self):
        obj = self.get_object()
        queryset = obj.files
        if self.kwargs['type'] == 'output':
            queryset = obj.files.annotate(dest_count=Count('destination_task'))
            #for elem in queryset:
               # print(str(elem.saved_id) + ":" + str(elem.dest_count))
            queryset = obj.files.annotate(dest_count=Count('destination_task')).filter(dest_count__lt=1)
            #print('output')
        elif self.kwargs['type'] == 'input':
            queryset = obj.files.annotate(src_count=Count('source_task'))
            #for elem in queryset:
                #print(str(elem.saved_id) + ":" + str(elem.src_count))
            queryset = obj.files.annotate(src_count=Count('source_task')).filter(src_count__lt=1)
            #print('input')
        else:
            queryset = obj.files
            #print('all')
        return queryset



            
    


class TaskStatusView(generics.RetrieveAPIView, common.PermissionMixin):
    serializer_class = serializers.TaskStatusSerializer
    
    def get_queryset(self):
        queryset = self.request.user.entity.tasks.all()
        return queryset

class TaskLogView(generics.RetrieveAPIView, common.PermissionMixin):
    serializer_class = serializers.TaskLogSerializer
    queryset = models.Task.objects.all()

class TaskKillView(generics.GenericAPIView, mixins.RetrieveModelMixin, common.PermissionMixin):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskStatusSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.task_status = 'KILL'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)














''' class TasksEScopeLCView(generics.ListCreateAPIView):
    serializer_class = serializers.TaskListCreateSerializer
    
    def get_queryset(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(models.Entity.objects.all(), **filter_kwargs)
        queryset = obj.tasks
        return queryset

    def create(self, request, *args, **kwargs):
        data=request.data
        data['entity'] = kwargs['pk']
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class TaskLView(generics.ListAPIView):
    serializer_class = serializers.TaskSerializer
    queryset = models.Task.objects.all()

class TaskRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TaskRUDSer
    queryset = models.Task.objects.all()


class TaskPaginator(pagination.CursorPagination):
    page_size=2
    ordering = 'issued_date'

class TaskPETView(TasksEScopeLCView):
    permission_classes = (permissions.IsPetPermission,)
    pagination_class = TaskPaginator
    def get_object(self):
        name = self.request.META.get('HTTP_PETNAME', None)
        filter_kwargs = {"common_name": name}
        obj = get_object_or_404(models.Entity.objects.all(), **filter_kwargs)
        return obj

    def get_queryset(self):
        obj = self.get_object()
        queryset = obj.tasks
        return queryset

    def create(self, request, *args, **kwargs):
        data=request.data
        data['entity'] = self.get_object().id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) '''

#class TaskCompleteView(generics.CreateAPIView):
#    def create(request, *args, **kwargs):
#        filter_kwargs = {'id': kwargs['pk']}
#        obj = get_object_or_404(models.Task.objects.all(), **filter_kwargs)
#        obj.completed_date = datetime.datetime.now()
#        obj.save()
#        return Response(status=status.HTTP_201_CREATED)



#class TaskSimpleList(generics.ListAPIView):
#    serializer_class = serializers.TaskSerializer
#    queryset = models.Task.objects.all()




