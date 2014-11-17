from pymongo import MongoClient
import re
import tornado.ioloop
import tornado.web
from note import Note, NoteManager
import datetime


class DebugHandler(tornado.web.RequestHandler):

    def get_manager(self):
        return self.application.settings.get('settings').get('note_manager')

    def get(self, user_id):
        notes = self.get_manager().find_all({'user_id': user_id})
        self.render("note_form.html", notes=notes, user_id=user_id)


class NoteListHandler(tornado.web.RequestHandler):

    def get_manager(self):
        return self.application.settings.get('settings').get('note_manager')

    def get(self, user_id):
        data = []
        notes = self.get_manager().find_all({'user_id': user_id})

        for note in notes:
            data.append(note.as_dict())
        self.write(tornado.web.escape.json_encode({
            'code': 0,
            'notes': data
        }))


class NoteHandler(tornado.web.RequestHandler):

    def get_manager(self):
        return self.application.settings.get('settings').get('note_manager')

    def get(self, user_id, note_id):
        note = self.get_manager().find({'note_id': note_id, 'user_id': user_id})
        if note is not None:
            self.write(tornado.web.escape.json_encode({
                'code': 'OK',
                'note': note.as_dict()
            }))
        else:
            self.write(tornado.web.escape.json_encode({
                'code': 'NOT_FOUND',
                'note': None
            }))

    def post(self, user_id):
        note_id = self.get_argument('note_id', None)
        if note_id is None or re.match(r'[a-z0-9]{32}', str(note_id)):
            note = Note(
                note_id,
                user_id,
                Note.STATUS_ACTIVE,
                self.get_argument('title'),
                self.get_argument('text'),
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            self.get_manager().save(note)

            self.write(tornado.web.escape.json_encode({
                'code': 'OK',
                'note': note.as_dict()
            }))
        else:
            self.write(tornado.web.escape.json_encode({
                'code': 'WRONG_PARAMS',
                'note': None
            }))


mongo_client = MongoClient()
note_manager = NoteManager(mongo_client.nevernote.note)
application = tornado.web.Application([
    (r"/debug/([a-zA-z0-9]+)/", DebugHandler),
    (r"/note/([a-zA-z0-9]+)/", NoteHandler),
    (r"/notes/([a-zA-z0-9]+)/", NoteListHandler),
], settings={'note_manager': note_manager})
if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()