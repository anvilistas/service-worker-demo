import anvil

from .session import store

store.sync()
anvil.open_form("Main")