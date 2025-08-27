from importlib.metadata import entry_points
from typing import List

from api.services import DataSourcePlugin

from api.services import Plugin


class PluginService(object):

    def __init__(self):
        self.plugins: dict[str,List[Plugin]] = {}

    def load_plugins(self, group: str):
        """
        Dynamically loads plugins based on entrypoint group.
        """
        self.plugins[group] = []
        for ep in entry_points(group=group):
            p = ep.load()
            plugin: DataSourcePlugin = p()
            self.plugins[group].append(plugin)

    def get_plugins(self, group: str):
        "Gets plugins based on entrypoint group."
        return self.plugins.get(group, [])