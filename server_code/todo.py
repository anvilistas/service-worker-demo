import anvil.server
from anvil.tables import app_tables
from .model.portable import Todo


@anvil.server.callable("todo.save")
def sync(todos):
    for todo in todos["new"]:
        app_tables.todo.add_row(**todo._serialise())
    for todo in todos["deleted"]:
        row = app_tables.todo.get(uuid=todo.uuid)
        if row:
            row.delete()

    return [Todo._from_row(row) for row in app_tables.todo.search()]