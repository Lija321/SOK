from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'index.html')
""""
def test_simple_visualizer(request):
    # Create a test graph (or use an actual Graph object)
    class TestGraph:
        def __init__(self):
            self.nodes = [{"id": "A"}, {"id": "B"}, {"id": "C"}]
            self.edges = [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}]
            self.name = "Test Graph"

        def get_nodes(self):
            return self.nodes

        def get_edges(self):
            return self.edges

    graph = TestGraph()
    visualizer = SimpleVisualizer()
    html = visualizer.display(graph)
    return render(request, "simple", {"graph_html": html})
"""