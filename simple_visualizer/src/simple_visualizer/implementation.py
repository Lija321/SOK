import os.path
from abc import ABC
from datetime import datetime

from django.views import View
from jinja2 import Environment, FileSystemLoader
from api.model.graph import Graph
from api.services.visualizer import Visualizer
from serializer import serialize


class SimpleVisualizer(Visualizer,ABC):
    def __init__(self):
        """Init function"""
        template_path = os.path.join(os.path.dirname(__file__))
        env = Environment(
            loader = FileSystemLoader(template_path + "/template"),
        )
        env.filters['serializeToJson'] = serialize
        self.template = env.get_template('simple-visualizer.html')
    def identifier(self):
        return "simple_visualizer"

    def name(self):
        """Implementation of the abstract method"""
        return "Simple Visualizer"

    def display_graph(self,graph : Graph,**kwargs):
        """Display function"""
        nodes_list = [{"id": n.id, "data": n.data} for n in graph.nodes]
        edges_list = [{"from": e.origin.id, "to": e.target.id} for e in graph.edges]
        return self.template.render(nodes=nodes_list,edges=edges_list,directed=graph.is_directed())