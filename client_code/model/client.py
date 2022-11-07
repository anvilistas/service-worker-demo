import anvil.server
from anvil_extras.storage import indexed_db
from anvil_extras.uuid import uuid4

from .portable import Todo


class TodoStore:
    db = indexed_db.create_store("todos")
    storage_keys = ("pushed", "deleted")

    def _restore(self, uuid):
        value = self.db[uuid]
        for key in self.storage_keys:
            del value[key]
        return Todo(**value)

    def all(self):
        return [
            self._restore(uuid)
            for uuid, value in self.db.items()
            if not value["deleted"]
        ]

    def save(self, todo):
        if todo.uuid is None:
            todo.uuid = uuid4()
        value = todo._serialise()
        for key in self.storage_keys:
            value[key] = False
        self.db[todo.uuid] = value

    def sync(self):
        new = [(k, v) for k, v in self.db.items() if not v["pushed"]]
        deleted = [k for k, v in self.db.items() if v["deleted"]]

        for _, v in new:
            v["pushed"] = True
        payload = {
            "new": [self._restore(k) for k, _ in new],
            "deleted": [self._restore(k) for k in deleted],
        }

        fetched = anvil.server.call("todo.save", payload)
        for k, v in new:
            self.db[k] = v
        for k in deleted:
            self.db.pop(k)

        unseen = [todo for todo in fetched if todo.uuid not in self.db]
        fetched_uuids = [todo.uuid for todo in fetched]
        removed = [
            value["uuid"]
            for value in self.db.values()
            if value["uuid"] not in fetched_uuids
        ]

        for todo in unseen:
            self.save(todo)
        for uuid in removed:
            self.db.pop(uuid)

    def delete(self, todo):
        value = self.db[todo.uuid]
        value["deleted"] = True
        self.db[todo.uuid] = value