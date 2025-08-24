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
        self.command_processor.register(Command.CREATE_NODE, self.create_node)
        self.command_processor.register(Command.CREATE_EDGE, self.create_edge)
        self.command_processor.register(Command.DELETE_NODE, self.delete_node)
        self.command_processor.register(Command.DELETE_EDGE, self.delete_edge)
        self.command_processor.register(Command.EDIT_NODE, self.edit_node)
        self.command_processor.register(Command.EDIT_EDGE, self.edit_edge)
        self.command_processor.register(Command.CLEAR_GRAPH, self.clear_graph)
        self.command_processor.register(Command.SEARCH_GRAPH, self.search_graph)

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

    def _current_graph(self) -> Graph:
        ws = next((w for w in self.workspaces if w.id == self.current_workspace_id), None)
        if not ws:
            raise ValueError("No active workspace.")
        return ws.graph_reference  # koristimo originalni graph, ne filtrirani

    def create_node(self, id: str, properties=None):
        graph = self._current_graph()
        from api.model import Node

        props = properties or {}
        props["id"] = id

        node = Node(id=id, data=props)
        graph.add_node(node)
        return f"Node {id} created."

    def create_edge(self, origin_id: str, target_id: str, properties=None):
        graph = self._current_graph()
        from api.model import Edge
        origin = graph.get_node(origin_id)
        target = graph.get_node(target_id)
        if not origin or not target:
            return f"Error: Missing nodes {origin_id}, {target_id}"
        edge = Edge(origin=origin, target=target, data=properties or {})
        graph.add_edge(edge)
        return f"Edge from {origin_id} to {target_id} created."

    def delete_node(self, id: str, **_):
        graph = self._current_graph()
        graph.remove_node(id)
        return f"Node {id} deleted."

    def delete_edge(self, origin_id: str, target_id: str, **_):
        graph = self._current_graph()
        graph.remove_edge(origin_id, target_id)
        return f"Edge from {origin_id} to {target_id} deleted."

    def edit_node(self, id: str, properties=None):
        graph = self._current_graph()
        graph.update_node(id, properties or {})
        return f"Node {id} updated."

    def edit_edge(self, origin_id: str, target_id: str, properties=None):
        graph = self._current_graph()
        graph.update_edge(origin_id, target_id, properties or {})
        return f"Edge from {origin_id} to {target_id} updated."

    def clear_graph(self):
        graph = self._current_graph()
        graph.clear()
        return "Graph cleared."



