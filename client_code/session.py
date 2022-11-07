import anvil_labs.service_worker as sw
from anvil_extras.messaging import Publisher

from .model.client import TodoStore

sw.init("service_worker")
publisher = Publisher(with_logging=False)
store = TodoStore()
store.sync()