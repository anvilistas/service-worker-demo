from .model.client import TodoStore

store = TodoStore()


@self.sync_event_handler
def onsync(e):
    print(f"sync fired with tag: {e.tag!r}")
    self.raise_event("todos.sync.starting")
    if e.tag != "todos.online":
        return
    store.sync()
    self.raise_event("todos.sync.done")


self.onsync = onsync

print("Service worker loaded")