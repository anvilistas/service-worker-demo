from .model.client import TodoStore

store = TodoStore()


def onsync():
    self.raise_event("todos.sync.starting")
    store.sync()
    self.raise_event("todos.sync.done")

self.BackgroundSync("todos.online", onsync)

print("Service worker loaded")