# JPetAPI
- [Endpointy](#endpointy)
    
- [Przyklady](#przykłady)
    - [Sesja i CSRFToken](#sesja)
    - [Task JSON](#task-json)

- [Modele](#modele)
    - [Authorization](#authorization-model)
    - [Entity](#entity-model)
    - [Task](#task-model)
    - [Job](#job-model)
    - [File](#file-model)
    
### Endpointy
#### Klient
<table>
    <tr>
        <th>URL</th>
        <th>Metoda</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td colspan=3><b>Tasks</b></td>
    </tr>
    <tr>
        <td rowspan=2>/tasks</td>
        <td>GET</td>
        <td>Zwraca lisę Tasks dla danego Entity którego common_name został podany w nagłówku CNAME.</td>
        </tr>
        <tr>
        <td>POST</td>
            <td>Umożliwia dodanie nowego Task. Wymaga CSRFToken. Patrz: <b>Sesja i CSRFToken</b>, <b>Task JSON</b></td>
    </tr>
    <tr>
        <td>/task/&ltid&gt/status</td>
        <td>GET</td>
        <td>Zwraza <b>task_status</b> dla Task identyfikowanego przez id. Dodatkowo zwraca listę Jobs zawierających informacje o: <b>job_status</b> i <b>exit_code</b>.</td>
    </tr>
        <tr>
        <td>/task/&ltid&gt/log</td>
        <td>GET</td>
        <td>Zwraca <b>log_file</b> i <b>task_status</b> dla Task identyfikowanego przez id. Dodatkowo zawiera listę Jobs zawierających informacje o: <b>job_status</b>, <b>exit_code</b>, <b>err_file</b> i <b>out_file</b>.</td>
    </tr>
        <tr>
        <td>/task/&ltid&gt/kill</td>
        <td>POST</td>
        <td>Ustawia status Task na killed.</td>
    </tr>
    <tr>
        <td colspan=3><b>Files</b></td>
    </tr>
            <tr>
        <td>/task/&ltid&gt/files</td>
        <td>GET</td>
        <td>Zwraca wszystkie pliki powiązanych z Task powiązanego z id. Jeśli dany Job zwraca więcej plików niż w specyfikacji Task-a to będą one widoczne ale bez pola <b>saved_id</b>.</td>
    </tr>
            <tr>
        <td>/task/&ltid&gt/input_files</td>
        <td>GET</td>
        <td>Zwraca listę plików, które nie są plikami wynikowymi żadnego Job.</td>
    </tr>
            <tr>
        <td>/task/&ltid&gt/output_files</td>
        <td>GET</td>
        <td>Zwraca listę plików, które nie są plikami wejściowymi do żadnego Job.</td>
    </tr>
    <tr>
        <td colspan=3><b>Entity</b></td>
    </tr>
    <tr>
        <td>/entity</td>
        <td>GET</td>
        <td>Zwraca indormacje o Entity z którego uzyskano dostęp do API.</td>
    </tr>
        <tr>
        <td colspan=3><b>Authorizations</b></td>
    </tr>
    <tr>
        <td>/authorizations</td>
        <td>GET</td>
        <td>Zwraca listę wszystkich autoryzacji.</td>
    </tr>
    <tr>
        <td>/authorizations/active</td>
        <td>GET</td>
        <td>Zwraca listę aktywnych autoryzacji.</td>
    </tr>
</table>

### Przykłady

#### Sesja
Autoryzacja odbywa się na podstawie zawartości nagłówka ```CNAME```. Jeśli w zapytaniu poda się poprawną wartość common_name z modelu Entity to w przypadku zapytania GET uzyska się ID sesji, token CSRF i wynik zapytania. W prypadku zapytań PUT, PATCH , POST wymagane jest podanie tokenu CSRF. Jeśli w nagłówku brakuje pola X_CSRFToken to zapytanie nie będzie miało efektu a w nagłówku zwrócony zostanie token którego można użyć do wysłania kolejnego zapytania. 

1. Rozpoczęcie sesji:
```
http --session=ent1 HEAD localhost:8000/api/tasks

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 1771
Content-Type: application/json
Date: Sun, 01 Jul 2018 22:46:05 GMT
Server: WSGIServer/0.2 CPython/3.6.4
Set-Cookie: csrftoken=fiG1vhd5ZLx1cmNeaYwloj4vVXuOrTB4mpsfasD1wsmnLjC5IhZdaGFhRcgOPyUj; expires=Sun, 30-Jun-2019 22:46:05 GMT; Max-Age=31449600; Path=/
Set-Cookie: sessionid=tx9qsglukjpygp1ley008ma8qu7bgmcp; expires=Sun, 15-Jul-2018 22:46:05 GMT; HttpOnly; Max-Age=1209600; Path=/
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN
```

2. Uzyskany plik ```ent1.json``` (plik opisu sesji httpie) należy zmodyfikować, dodać nagłówek X_CSRFToken i można usunąć nagłówek CNAME.

ent1.json:
```
{
    "__meta__": {
        "about": "HTTPie session file",
        "help": "https://httpie.org/docs#sessions",
        "httpie": "0.9.9"
    },
    "auth": {
        "password": null,
        "type": null,
        "username": null
    },
    "cookies": {
        "csrftoken": {
            "expires": 1561934765,
            "path": "/",
            "secure": false,
            "value": "fiG1vhd5ZLx1cmNeaYwloj4vVXuOrTB4mpsfasD1wsmnLjC5IhZdaGFhRcgOPyUj"
        },
        "sessionid": {
            "expires": 1531694765,
            "path": "/",
            "secure": false,
            "value": "tx9qsglukjpygp1ley008ma8qu7bgmcp"
        }
    },
    "headers": {
        "X-CSRFToken":"fiG1vhd5ZLx1cmNeaYwloj4vVXuOrTB4mpsfasD1wsmnLjC5IhZdaGFhRcgOPyUj"
    }
}
```

3. Po nawiązaniu sesji i uzysakniu tokenu można utworzyć nowy Task.
```
http --session=ent1 POST localhost:8000/api/tasks <new_task.json

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 1769
Content-Type: application/json
Date: Sun, 01 Jul 2018 22:49:15 GMT
Server: WSGIServer/0.2 CPython/3.6.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "comments": "some-comment",
    "completed_date": null,
    "files": [
        {
            "comments": "This is input for Job 1.",
            "id": 22,
            "name": "File#01",
            "path": "1/4/22"
        },
        ...
```

#### Task JSON

Najprostszy Task można utworzyć poprzez wysłanie JSON-a postaci:
```
{ 
    "comments":"some-comment", 
    "priority":"1", 
    "parameters":"some-params",
    "jobs":[],
    "files":[]
}
```

Task-i składają się z Jobs i Files, które przekazywane są w listach ```"jobs"``` i ```"files"```.

Najprostszy Job ma postać:
```
{   
    "saved_id":"4",
    "input_data":[],
    "output_data":[],
    "job_previous":[],
    "job_description":"job-type-desc",
    "job_params":"some-params"
}
```
 - ```saved_id``` musi być unikatowe w ramach danego Task.
 - ```input_data``` i ```output_data``` są listami __nazw__ plików. Pliki do których odnoszą się Jobs muszą być zdefiniowane w liście ```files``` dla danego Tasku. Kolejność plików w liście zostaje zachowana. 
 - ```job_previous``` jest listą pól ```saved_id``` na zakończenie których definiowany Job ma zaczekać.
 
 File:
 ```
{
    "name":"File#01",
    "comments":"This is input for Job 1."
}
```

Stworzenie struktury:
```

 |File#02|-->[Job#01]-->|#File04|-->[Job#03]
 |File#01|--> +                        |
                                       |
 |File#03|-->[Job#02]-->|File#05|-->[Job#04]-->|File#06|
                                           +-->|File#07|
```

W której:

  - Job#01: Wymaga 2 plików(File#01, File#02) i tworzy co najmniej jeden plik (#File04)
  - Job#02: Wymaga 1 pliku(File#03) i tworzy co najmniej jeden plik(File#05)
  - Job#03: Wymaga 1 pliku(File#04), może zależeć od Job#01 i nie musi tworzyć pliku
  - Job#04: Wymaga 1 pliku(File#05) i ukończenia zadania Job#03, tworzy co najmniej dwa pliki(File#06, File#07)
    
Wymaga nasępującego formatu Task:
```
{ "comments":"some-comment", 
    "priority":"1", 
    "parameters":"some-params",
    "jobs":[
        {   
            "saved_id":"1",
            "input_data":["File#01", "File#02"],
            "output_data":["File#04"],
            "job_description":"job-type-desc",
            "job_params":"some-params"

        }, 
        {
            "saved_id":"2",
            "input_data":["File#03"],
            "output_data":["File#05"],
            "job_description":"job-type-desc",
            "job_params":"some-params"
        },
        {   
            "saved_id":"3",
            "input_data":["File#04"],
            "job_description":"job-type-desc",
            "job_params":"some-params"
        },
        {   
            "saved_id":"4",
            "input_data":["File#05"],
            "output_data":["File#06", "File#07"],
            "job_previous":["3"],
            "job_description":"job-type-desc",
            "job_params":"some-params"
        }
            ],

    "files":[
        {
            "name":"File#01",
            "comments":"This is input for Job 1."
        },
        {
            
            "name":"File#02"
        },
        {
            "name":"File#03"
        },
        {
            "name":"File#04"
        },
        {
            "name":"File#05"
        },
        {
           "name":"File#06"
        },
        {
            "name":"File#07",
            "comments":"This is very important file."
        }
    ]
    
    }
```

1. Każde zadanie może wymagać pewnej liczby plików, tworzyć pewną ilość plików i zależeć od pewnej ilości zadań które muszą zostać wykonane wcześniej.

2. Cała struktura (workflow) musi być zadeklarowana w momencie tworzenia Task.
3. Pliki:
     - Każdy zadeklarowany w momencie tworzenia Task plik ma w strukturze określone ID. To ID jest zachowane i reprezentowane przez pole saved_id w modelu File.
     - Każdemu zadeklarowanemu plikowi przypisana zostaje ścieżka stworzona z ID entity, ID task i ID pliku.
     - W rezultacie wykonania Task/Job może powstać więcej plików niż zadeklarowano. Przykładowo Job#01 może stworzyć 3 pliki ale tylko jeden z nich musi być specjalnie rozróżniony (np. zostanie wykorzystany w kolejnym zadaniu). Taki plik może być rozróżniony przez swoje saved_id, w parametrach zadania może być zadeklarowane który z plików wyjściowych ma zostać wyróżniony i czy zachwać pozostałe pliki. Pozostałe pliki wystarczy dodać w bazie i przypisać do wykonywanego Task/Job. 
     - Tak samo trzeba rozróżnić pliki wejściowe by nie zgubić informacji który plik ma być którym argumentem wykonania Job. Przykładowo Job#01 przyjmuje plik a i b i wykonuje na nich różne operacje. Zadeklarowanie id unikatowego w kontekście danego Task i użycie parametrów wykonania Job można wybrać który plik zostanie jak potraktowany.
 4. Job:
     - Job może zależeć id poprzednich Job lub od plików.
     - Job zawiera informacje o poprzednich i następnych Job oraz o danych/plikach wejściowych i wyjściowych.
     - Rozróżnienie Job odbywa się na podstawie ID unikatowego w kontekście danego Task, to ID jest zachowywane jako saved_id.


### Modele
#### Authorization Model
Endpointy: [LINK](#authorization-endpoint)
<table>
    <tr>
        <th>Pole</th>
        <th>Typ</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td>id</td>
        <td>-</td>
        <td>ID dodawane automatycznie przez Django.</td>
    </tr>
    <tr>
        <td>subject</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td>...</td>
    </tr>
        <tr>
        <td>issue_date</td>
        <td><pre>DateTimeField()</pre></td>
        <td>...</td>
    </tr>
        <tr>
        <td>expiry_date</td>
        <td><pre>DateTimeField()</pre></td>
        <td>...</td>
    </tr>
            <tr>
        <td>created</td>
        <td><pre>DateTimeField(auto_now_add=True)</pre></td>
        <td>...</td>
    </tr>
            <tr>
        <td>fingerprint</td>
        <td></td>
        <td>...</td>
    </tr>
            <tr>
        <td>entity</td>
        <td><pre>ForeignKey(to = 'Entity',
            on_delete = models.CASCADE,
            related_name='authorizations')</pre></td>
        <td>...</td>
    </tr>
</table>

#### Entity Model
<table>
    <tr>
        <th>Pole</th>
        <th>Typ</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td>common_name</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>name</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>address</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td></td>
    </tr>
 <tr>
        <td>contact</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td></td>
    </tr>
<tr>
        <td>comments</td>
        <td><pre>TextField(null=True)</pre></td>
        <td></td>
    </tr>
<tr>
        <td>created</td>
        <td><pre>DateTimeField(auto_now_add=True)</pre></td>
        <td></td>
    </tr>
<tr>
        <td>authorizations</td>
        <td>Z modelu Authorization:<pre>ForeignKey(to = 'Entity', 
            on_delete = models.CASCADE, 
            related_name='authorizations')</pre></td>
        <td></td>
    </tr>
<tr>
        <td>tasks</td>
        <td>Z modelu Task:<pre>ForeignKey(to = 'Entity', 
            on_delete = models.CASCADE, 
            related_name='tasks')</pre></td>
        <td>...</td>
    </tr>
</table>
Dodatkowo: 

```
@receiver(post_save, sender=Entity)
def create_user(sender, instance, created, **kwargs):
    if created:
        user = User(username = instance.common_name)
        user.save()
        instance.user = user
        instance.save()
```

Automatycznie stworzy obiekt User powiązany z Entity i używany do autoryzacji.

#### Task Model
<table>
    <tr>
        <th>Pole</th>
        <th>Typ</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td>task_status</td>
        <td><pre>IntegerField()</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>issued_date</td>
        <td><pre>DateTimeField(auto_now_add=True) </pre></td>
        <td></td>
    </tr>
    <tr>
        <td>started_date</td>
        <td><pre>DateTimeField(null=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>completed_date</td>
        <td><pre>DateTimeField(null=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>priority</td>
        <td><pre>IntegerField(default=1)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>parameters</td>
        <td><pre>CharField(max_length=45, 
            default=None)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>comments</td>
        <td><pre>TextField(null=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>task_type</td>
        <td><pre>CharField(max_length=45,
            default='default-task-type')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>entity</td>
        <td><pre>ForeignKey(to = 'Entity', 
            on_delete = models.CASCADE, 
            related_name='tasks')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>jobs</td>
        <td>Z modelu Job:<pre>ForeignKey(to = 'Task', 
            on_delete = models.CASCADE, 
            related_name='jobs')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>files</td>
        <td>Z modelu File:<pre>ForeignKey(Task, 
            on_delete=models.CASCADE, 
            related_name='files')</pre></td>
        <td></td>
    </tr>
    
</table>
    
#### Job Model
<table>
   <tr>
        <th>Pole</th>
        <th>Typ</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td>job_status</td>
        <td><pre>IntegerField()</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>job_description</td>
        <td><pre>CharField(max_length=45)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>job_params</td>
        <td><pre>CharField(max_length = 45)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>job_previous</td>
        <td><pre>ManyToManyField(to = 'Job', 
            related_name = 'job_next')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>saved_id</td>
        <td><pre>IntegerField(null = True, 
            default = None)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>created</td>
        <td><pre>DateTimeField(auto_now_add=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>start_date</td>
        <td><pre>DateTimeField(null=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>finish_date</td>
        <td><pre>DateTimeField(null=True)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>input_data</td>
        <td><pre>ManyToManyField(File,
            related_name='destination_job')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>output_data</td>
        <td><pre>ManyToManyField(File,
            related_name='source_job')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>task</td>
        <td><pre>ForeignKey(to = 'Task', 
            on_delete = models.CASCADE, 
            related_name='jobs')</pre></td>
        <td></td>
    </tr>
</table>
    
#### File Model
<table>
   <tr>
        <th>Pole</th>
        <th>Typ</th>
        <th>Opis</th>
    </tr>
    <tr>
        <td>comments</td>
        <td><pre>CharField(max_length = 45,
            default = None)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>saved_id</td>
        <td><pre>IntegerField(default = None)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>path</td>
        <td><pre>CharField(max_length = 45, 
            null = True, 
            default = None)</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>task</td>
        <td><pre>ForeignKey(Task, 
            on_delete=models.CASCADE, 
            related_name='files')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>destination_job</td>
        <td>Z modelu Job:<pre>ManyToManyField(File, 
            related_name='destination_job')</pre></td>
        <td></td>
    </tr>
    <tr>
        <td>source_job</td>
        <td>Z modelu Job:<pre>ManyToManyField(File, 
            related_name='source_job')</pre></td>
        <td></td>
    </tr>
</table>


#### Paginator
Przykład w endpoince /api/tasks z page_size = 2.
Klasa Paginator dodaje pola "next", "previous" i "results".
```
http GET http://127.0.0.1:8000/api/tasks?cursor=cD0yMDE4LTA1LTA4KzIyJTNBMjclM0E0Ny42Njg0MDQlMkIwMCUzQTAw PETNAME:cname

HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 1900
Content-Type: application/json
Date: Tue, 08 May 2018 22:41:44 GMT
Server: WSGIServer/0.2 CPython/3.6.4
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "next": "http://127.0.0.1:8000/api/tasks?cursor=cD0yMDE4LTA1LTA4KzIyJTNBMjclM0E0OS43NTI5MjAlMkIwMCUzQTAw",
    "previous": "http://127.0.0.1:8000/api/tasks?cursor=cj0xJnA9MjAxOC0wNS0wOCsyMiUzQTI3JTNBNDguNjI4MDEyJTJCMDAlM0EwMA%3D%3D",
    "results": [
        {
            "comments": "some_comment",
            "completed_date": null,
            "created": "2018-05-08T22:27:48.628012Z",
            "entity": 1,
            "id": 3,
            "issued_date": "2018-05-08T22:27:48.627933Z",
            "jobs": [...],
            "priority": 1,
            "processed_data": null,
            "raw_data": "path-to-data",
            "task_status": 11,
            "task_type": "default-task-type"
        },
        {
            "comments": "some_comment",
            "completed_date": null,
            "created": "2018-05-08T22:27:49.752920Z",
            "entity": 1,
            "id": 4,
            "issued_date": "2018-05-08T22:27:49.752845Z",
            "jobs": [...],
            "priority": 1,
            "processed_data": null,
            "raw_data": "path-to-data",
            "task_status": 11,
            "task_type": "default-task-type"
        }
    ]
}
```
Paginator korzysta z zapytania:
```

//pobranie entity
(0.000) SELECT (1) AS "a" FROM "RestAPI_entity" WHERE "RestAPI_entity"."common_name" = 'cname' LIMIT 1; args=('cname',)
(0.000) SELECT "RestAPI_entity"."id", "RestAPI_entity"."common_name", "RestAPI_entity"."name", "RestAPI_entity"."address", "RestAPI_entity"."contact", "RestAPI_entity"."comments", "RestAPI_entity"."created" FROM "RestAPI_entity" WHERE "RestAPI_entity"."common_name" = 'cname'; args=('cname',)

//pobranie task 
(0.000) SELECT "RestAPI_task"."id", "RestAPI_task"."task_status", "RestAPI_task"."issued_date", "RestAPI_task"."completed_date", "RestAPI_task"."raw_data", "RestAPI_task"."processed_data", "RestAPI_task"."comments", "RestAPI_task"."task_type", "RestAPI_task"."priority", "RestAPI_task"."entity_id", "RestAPI_task"."created"
//--!!--
FROM "RestAPI_task" 
WHERE ("RestAPI_task"."entity_id" = 1 AND "RestAPI_task"."created" > '2018-05-08 22:27:47.668404') 
ORDER BY "RestAPI_task"."created" ASC LIMIT 3; args=(1, '2018-05-08 22:27:47.668404')

//pobranie job
(0.000) SELECT "RestAPI_job"."id", "RestAPI_job"."job_status", "RestAPI_job"."job_description", "RestAPI_job"."start_date", "RestAPI_job"."finish_date", "RestAPI_job"."input_data", "RestAPI_job"."output_data", "RestAPI_job"."task_id", "RestAPI_job"."created" FROM "RestAPI_job" WHERE "RestAPI_job"."task_id" = 3; args=(3,)
(0.000) SELECT "RestAPI_job"."id", "RestAPI_job"."job_status", "RestAPI_job"."job_description", "RestAPI_job"."start_date", "RestAPI_job"."finish_date", "RestAPI_job"."input_data", "RestAPI_job"."output_data", "RestAPI_job"."task_id", "RestAPI_job"."created" FROM "RestAPI_job" WHERE "RestAPI_job"."task_id" = 4; args=(4,)
[08/May/2018 22:41:44] "GET /api/tasks?cursor=cD0yMDE4LTA1LTA4KzIyJTNBMjclM0E0Ny42Njg0MDQlMkIwMCUzQTAw HTTP/1.1" 200 1900
```
