from RestAPI.models import Entity, Task

ent = Entity()
ent.save()
print('Entity: ' + str(ent.id))
task = Task(entity = ent)
task.save()
print('Task: ' + str(task.id))
