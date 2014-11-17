import datetime
import hashlib

__author__ = 'nasedkin'

import pymongo.collection


class Note:

    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'

    note_id = None
    user_id = None
    status = None
    title = None
    text = None
    mod_time = None

    def __init__(self, note_id=None, user_id=None, status=None, title=None, text=None, mod_time=None):
        self.note_id = note_id
        self.user_id = user_id
        self.status = status
        self.title = title
        self.text = text
        self.mod_time = mod_time

    def as_dict(self):
        return {
            'note_id': self.note_id,
            'user_id': self.user_id,
            'status': self.status,
            'title': self.title,
            'text': self.text,
            'mod_time': self.mod_time
        }

    def from_dict(self, data: dict):
        if 'note_id' in data:
            self.note_id = data['note_id']
        else:
            self.note_id = None

        self.user_id = data['user_id']
        self.status = data['status']
        self.title = data['title']
        self.text = data['text']
        self.mod_time = data['mod_time']


class NoteManager:

    __coll__ = None

    def __init__(self, coll: pymongo.collection.Collection):
        self.__coll__ = coll

    @staticmethod
    def __generate_note_id__(note: Note):
        mod_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        hash_string = (mod_time + str(note.as_dict())).encode('utf-8')
        return hashlib.md5(hash_string).hexdigest()

    def insert(self, note: Note):
        note.note_id = self.__generate_note_id__(note)
        return self.__coll__.insert(note.as_dict())

    def update(self, note: Note):
        if note.note_id is None:
            raise AttributeError
        return self.__coll__.update({'note_id': note.note_id}, note.as_dict())

    def save(self, note: Note):
        if note.note_id is None:
            return self.insert(note)
        else:
            return self.update(note)

    def find(self, attributes: dict):
        data = self.__coll__.find_one(attributes)
        note = Note()
        note.from_dict(data)
        return note

    def find_all(self, attributes: dict):
        result = []
        data = self.__coll__.find(attributes)
        for note_dict in data:
            note = Note()
            note.from_dict(note_dict)
            result.append(note)
        return result
