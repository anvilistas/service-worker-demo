from anvil_extras.messaging import Publisher
import anvil_labs.service_worker as sw
from .model.client import TodoStore

sw.init("service_worker")
publisher = Publisher()
store = TodoStore()