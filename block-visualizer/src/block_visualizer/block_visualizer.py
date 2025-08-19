import os
from api.model.graph import Graph
from mako.template import Template
from datetime import datetime
import json

class BlockVisualizer:
    def __init__(self):
        '''
        default constructor
        sets up the template necessary for dynamic Graph visualization
        '''

        self.template = Template(self.load_template())

    def __str__(self):
        '''
        str(BlockVisualizer)
        returns the simple name used to denote which Visualizer is currently utilized in View(s)
        '''

        return 'Block'

    def load_template(self) -> str:
        '''
        loads the stringed HTML template from file
        (specifically, templates/block.html)
        '''

        template_path = os.path.join(os.path.dirname(__file__), "templates", "block.html")
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def display(self, graph: Graph, directed = False):
        '''
        "main" method of the visualizer
        renders the in-memory graph object into the template-compatible HTML format used for visualization
        '''

        nodes = [
            {
                "id": n.id,
                "data": {k: convert_json_safe(v) for k, v in n.data.items()}
            }
            for n in graph.nodes
        ]

        edges = [
            {
                "source": e.origin.id,
                "target": e.target.id
            }
            for e in graph.edges
        ]

        return self.template.render(
            name=str(self),
            nodes=nodes,
            edges=edges,
            directed=json.dumps(directed)
        )

def convert_json_safe(value):
    """
    converts problematic data types to ISO strings
    (specifically, datetime)
    """
    if isinstance(value, datetime):
        return value.strftime("%d-%m-%Y")
    if isinstance(value, bool):
        return str(value).lower()
    return value