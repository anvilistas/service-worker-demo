import anvil.server
import anvil_labs.service_worker as sw
import anvil.js

from ..model.portable import Todo
from ..session import publisher, store
from ._anvil_designer import MainTemplate


class Main(MainTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        publisher.subscribe("todos", self, self.message_handler)
        sw.subscribe("todos.sync", self.on_sync)
        self.refresh_todos()

    def message_handler(self, message):
        self.refresh_todos()
        self.do_sync()

    def do_sync(self):
        if not anvil.server.is_app_online():
            msg = "It looks like you're offline - we'll try again when you're back"
            anvil.Notification(msg).show()
        try:
            sw.register_sync("todos.online")
        except anvil.js.ExternalError as err:
            print(err.original_error.name)
            if err.original_error.name == "NotAllowedError":
                msg = (
                    "It looks like your browser isn't supported by this app.\n\n"
                    "Try using Chrome or Vivaldi instead."
                )
                anvil.alert(msg)
            else:
                raise err

    def refresh_todos(self):
        self.repeating_panel_1.items = store.all()

    def on_sync(self, **event_args):
        msg = "Syncing todos with server..."
        anvil.Notification(msg).show()

    def text_box_1_pressed_enter(self, sender, **event_args):
        todo = Todo(sender.text)
        sender.text = ""
        store.save(todo)
        publisher.publish("todos", "todo.added", todo.uuid)