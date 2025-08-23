from typing import List, Dict, Callable, Any

from api.model import Graph

from .model.command_processor import CommandProcessor, Command
from .model.filter import Filter
from .model.workspace import  Workspace
from .service import PluginService


class Application:

    def __init__(self, workspaces=None):
        if workspaces is None:
            workspaces = []
        self.workspaces = workspaces
        self.current_workspace_id = None
        self.service_plugin = PluginService()
        self.service_plugin.load_plugins("graph_explorer.visualizers")
        self.service_plugin.load_plugins("sok.plugins.datasource")
        self.command_processor = CommandProcessor()
        self.command_processor.register(Command.FILTER_GRAPH,self.filter_graph)
        self.command_processor.register(Command.CREATE_WORKSPACE,self.create_workspace)
        self.command_processor.register(Command.SELECT_WORKSPACE,self.select_workspace)
        self.command_processor.register(Command.SELECT_VISUALIZER,self.select_visualizer)

    def filter_graph(self, **kwargs):
        name = kwargs.get("name")
        filter : Filter = kwargs.get("filter")
        if name:
            return [ws.add_filter(filter) for ws in self.workspaces if ws.name == name]
        return None

    def search_graph(self, query: str, **kwargs):
        return [ws.graph for ws in self.workspaces if query in ws.graph.name]

    def create_workspace(self, **kwargs):
        data_plugins = self.service_plugin.get_plugins("sok.plugins.datasource")
        visualizer_plugins = self.service_plugin.get_plugins("graph_explorer.visualizers")
        data_plugin_name = kwargs.get("data_plugin")
        visualizer_name = kwargs.get("visualizer")
        data_plugin = next((p for p in data_plugins if p.__class__.__name__ == data_plugin_name ), None)
        visualizer = next((p for p in visualizer_plugins if p.__class__.__name__ == visualizer_name ), None)

        workspace = kwargs.get("workspace")
        ws = Workspace(visualizer_id=visualizer.identifier(), data_source_plugin=data_plugin,name=workspace)
        self.current_workspace_id = ws.id
        self.workspaces.append(ws)
    def select_workspace(self, **kwargs):
        self.current_workspace_id = kwargs.get("id")

    def select_visualizer(self, **kwargs):
        ws = next((w for w in self.workspaces if w.id == self.current_workspace_id), None)
        if ws:
            ws.visualizer_id = kwargs.get("visualizer", ws.visualizer_id)



