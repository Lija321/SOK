from functools import wraps


def validate_json(data: dict):
    """
    Validate JSON structure: ids, references, edges.
    """
    node_ids = {n["id"] for n in data.get("nodes", [])}
    for edge in data.get("edges", []):
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise ValueError(f"Invalid edge: {edge}")


def cache_graph(func):
    """
    Decorator for caching Graph results.

    If the graph has already been built once, return the cached version
    instead of reconstructing it again.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._graph_cache is not None:
            return self._graph_cache
        graph = func(self, *args, **kwargs)
        self._graph_cache = graph
        return graph
    return wrapper
