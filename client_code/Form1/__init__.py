from ._anvil_designer import Form1Template
import anvil.server
import anvil_labs.service_worker as sw
from ..model import Todo
from ..session import publisher, store

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        publisher.subscribe("todos", self, self.message_handler)
        sw.add_listener("sync", self.on_bg_sync)
        self.refresh_todos()

    def message_handler(self, message):
        self.refresh_todos()
        self.do_sync()

    def do_sync(self):
        try:
            store.sync()
        except anvil.server.AppOfflineError as e:
            print(f"Failed to sync: {e!r}")
            sw.register_sync("todos.online") # this won't work in all browsers!

    def refresh_todos(self):
        self.repeating_panel_1.items = store.all()

    def on_bg_sync(self, **event_args):
        tag = event_args.get("tag")
        print("service worker sync event fired with tag:", tag)
        if tag == "todos.online":
            self.do_sync()

    def text_box_1_pressed_enter(self, sender, **event_args):
        todo = Todo(sender.text)
        sender.text = ""
        store.save(todo)
        publisher.publish("todos", "todo.added", todo.uuid)
