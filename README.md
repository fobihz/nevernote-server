# Newernote server application
Серверное приложение для создания заметок.
### Version
0.0.1
### Requirements
* [Python 3]
* [Tornado]
* [Mongo]
* [PyMongo]

### API: create note
Request:
```
URL:
http://localhost:8888/note/USER_ID/
POST DATA:
title=string
text=string
```
Response:
```
{
    code: string
    note: {
        note_id: string,
        user_id: string,
        status: string,
        title: string,
        text: string,
        mod_time: string
    }
}
```

### API: update note
Request:
```
URL:
http://localhost:8888/note/USER_ID/
POST DATA:
note_id=string
title=string
text=string
```
Response:
```
{
    code: string
    note: {
        note_id: string,
        user_id: string,
        status: string,
        title: string,
        text: string,
        mod_time: string
    }
}
```
### API: notes list
Request:
```
URL:
http://localhost:8888/notes/USER_ID/
```
Response:
```
{
    code: string
    notes: [
            {
                note_id: string,
                user_id: string,
                status: string,
                title: string,
                text: string,
                mod_time: string
            }, ...
        ]
}
```

### Debug page
```
URL:
http://localhost:8888/debug/USER_ID/
```
[Python 3]: https://www.python.org/
[Tornado]: http://www.tornadoweb.org/
[Mongo]: http://www.mongodb.org/
[PyMongo]: http://api.mongodb.org/python/current/
