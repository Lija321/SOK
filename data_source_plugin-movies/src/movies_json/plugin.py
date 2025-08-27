import os
import json
from pathlib import Path
from typing import Dict, Set, List

from api.model import Graph, Node, Edge
from api.services import DataSourcePlugin

from .parser import create_nodes, create_edges
from .utils import validate_json, cache_graph


class MoviesDataSourcePlugin(DataSourcePlugin):
    """
    Data source plugin for loading a movie dataset from JSON file
    and creating a graph representation.

    This plugin parses movies, actors, directors, and studios,
    then builds a directed graph with typed relationships such as:
    - acted_in (actor -> film)
    - directed (director -> film)
    - produced_by (film -> studio)
    - sequel_of (film -> film)
    """

    def __init__(self):
        # Cache for loaded graph
        self._graph_cache = None

    @cache_graph
    def load_data(self, file_path: str = None, **kwargs) -> Graph:
        """
        Load movie dataset from a JSON file and construct a Graph object.

        :param file_path: Path to JSON dataset. Defaults to `data/movies.json` inside the plugin.
        :param kwargs: Optional filters (e.g. only_films=True, min_rating=8.0).
        :return: Graph instance containing nodes (films, actors, directors, studios)
                 and edges (acted_in, directed, produced_by, sequel_of).
        :rtype: Graph
        """
        if file_path is None:
            plugin_dir = Path(__file__).parent
            file_path = plugin_dir / "data" / "movies_large.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"JSON data file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # validacija
        validate_json(data)

        # kreiranje grafa
        nodes = create_nodes(data, **kwargs)
        edges = create_edges(data, nodes, **kwargs)

        graph = Graph(edges=edges, nodes=nodes, directed=True)
        return graph

    def get_top_rated_movies(self, nodes: Set["Node"], n: int = 5) -> List["Node"]:
        """
        Retrieve the top N movies ranked by rating.

        :param nodes: Set of Node objects in the graph.
        :param n: Number of movies to return (default = 5).
        :return: List of Node objects representing the top-rated movies.
        :rtype: List[Node]
        """
        films = [node for node in nodes if node.data.get("type") == "film"]
        sorted_films = sorted(films, key=lambda f: f.data.get("rating", 0), reverse=True)
        return sorted_films[:n]

    def get_movies_by_director(self, nodes: Set["Node"], edges: Set["Edge"], director_name: str) -> List["Node"]:
        """
        Retrieve all movies directed by a given director.

        :param nodes: Set of Node objects in the graph.
        :param edges: Set of Edge objects in the graph.
        :param director_name: Full name of the director.
        :return: List of Node objects representing movies directed by the specified director.
        :rtype: List[Node]
        """
        director_nodes = [n for n in nodes if n.data.get("type") == "director" and n.data.get("name") == director_name]
        if not director_nodes:
            return []
        director_id = director_nodes[0].id

        directed_edges = [e for e in edges if e.origin.id == director_id and e.data.get("type") == "directed"]
        return [e.target for e in directed_edges]

    def get_filmography(self, nodes: Set["Node"], edges: Set["Edge"], actor_name: str) -> List["Node"]:
        """
        Retrieve all movies an actor has played in.

        :param nodes: Set of Node objects in the graph.
        :param edges: Set of Edge objects in the graph.
        :param actor_name: Full name of the actor.
        :return: List of Node objects representing movies the actor starred in.
        :rtype: List[Node]
        """
        actor_nodes = [n for n in nodes if n.data.get("type") == "actor" and n.data.get("name") == actor_name]
        if not actor_nodes:
            return []
        actor_id = actor_nodes[0].id

        acted_in_edges = [e for e in edges if e.origin.id == actor_id and e.data.get("type") == "acted_in"]
        return [e.target for e in acted_in_edges]

    def get_sequels(self, edges: Set["Edge"], film_id: str) -> List["Node"]:
        """
        Retrieve all sequels of a given film.

        :param edges: Set of Edge objects in the graph.
        :param film_id: Unique identifier of the film node.
        :return: List of Node objects representing sequel movies.
        :rtype: List[Node]
        """
        return [e.target for e in edges if e.origin.id == film_id and e.data.get("type") == "sequel_of"]

    def get_movies_by_studio(self, nodes: Set["Node"], edges: Set["Edge"], studio_name: str) -> List["Node"]:
        """
        Retrieve all movies produced by a given studio.

        :param nodes: Set of Node objects in the graph.
        :param edges: Set of Edge objects in the graph.
        :param studio_name: Name of the studio.
        :return: List of Node objects representing movies produced by the specified studio.
        :rtype: List[Node]
        """
        studio_nodes = [n for n in nodes if n.data.get("type") == "studio" and n.data.get("name") == studio_name]
        if not studio_nodes:
            return []
        studio_id = studio_nodes[0].id

        produced_edges = [e for e in edges if e.target.id == studio_id and e.data.get("type") == "produced_by"]
        return [e.origin for e in produced_edges]

    def name(self) -> str:
        return "Movies Data Source Plugin"

    def identifier(self) -> str:
        return "movies_data_source_plugin"
