from .model.client import TodoStore

store = TodoStore()


@self.sync_event_handler
def onsync(e):
    if e.tag != "todos.online":
        return
    self.raise_event("todos.sync.starting")
    store.sync()
    self.raise_event("todos.sync.done")


self.onsync = onsync

print("Service worker loaded")