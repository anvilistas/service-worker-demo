import anvil.server
from anvil_labs import kompot


@kompot.register
@anvil.server.portable_class
class Todo:
    attributes = ("uuid", "description")

    @classmethod
    def _from_row(cls, row):
        return cls(**dict(row))

    def __init__(self, description, uuid=None):
        self.uuid = uuid
        self.description = description

    def _serialise(self):
        return {key: getattr(self, key) for key in self.attributes}