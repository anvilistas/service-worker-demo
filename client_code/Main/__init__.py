import anvil.js
import anvil.server
import anvil_labs.service_worker as sw

from ..model.portable import Todo
from ..session import publisher, store
from ._anvil_designer import MainTemplate


class Main(MainTemplate):
    def __init__(self, **properties):
        self._sync_status = "done"
        self.init_components(**properties)
        publisher.subscribe("todos", self, self.message_handler)
        sw.subscribe("todos.sync.starting", self.on_sync)
        sw.subscribe("todos.sync.done", self.on_sync)
        self.refresh_todos()

    @property
    def sync_status(self):
        return self._sync_status

    @sync_status.setter
    def sync_status(self, value):
        self._sync_status = value
        self.refresh_data_bindings()

    @property
    def sync_label_props(self):
        props = {
            "done": {"text": "Synced", "icon": "fa:check"},
            "starting": {"text": "Syncing with server...", "icon": "fa:refresh"},
            "offline": {"text": "Offline", "icon": "fa:chain-broken"}
        }
        return props[self.sync_status]

    def message_handler(self, message):
        self.refresh_todos()
        self.do_sync()

    def do_sync(self):
        if not anvil.server.is_app_online():
            self.sync_status = "offline"
        
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

    def on_sync(self, event_name, **event_args):
        self.sync_status = event_name.split(".")[-1]

    def text_box_1_pressed_enter(self, sender, **event_args):
        todo = Todo(sender.text)
        sender.text = ""
        store.save(todo)
        publisher.publish("todos", "todo.added", todo.uuid)