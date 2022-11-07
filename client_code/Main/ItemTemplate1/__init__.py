from ._anvil_designer import ItemTemplate1Template
from ...session import publisher, store


class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

    def delete_button_click(self, **event_args):
        store.delete(self.item)
        publisher.publish("todos", "todo.deleted", self.item.uuid)
