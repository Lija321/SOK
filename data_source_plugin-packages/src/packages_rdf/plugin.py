import os
from pathlib import Path
from typing import Dict, Set
from rdflib import Graph as RDFGraph, Namespace, URIRef, Literal
from rdflib.namespace import FOAF, XSD

from api.model import Node, Edge, Graph
from api.services import DataSourcePlugin


class PackagesDataSourcePlugin(DataSourcePlugin):
    """
    Data source plugin for loading package dependency graphs from RDF/TTL files.
    
    This plugin parses package information, dependencies, optional dependencies,
    and conflicts from RDF data to create a graph representation.
    """

    def __init__(self):
        # Define namespaces used in the RDF data
        self.EX = Namespace("http://example.org/")
        self.FOAF = FOAF
        self.XSD = XSD
        
        # Cache for loaded data
        self._graph_cache = None

    def load_data(self, file_path: str = None, **kwargs) -> Graph:
        """
        Load package dependency data from RDF/TTL file and create a Graph.

        :param file_path: Path to the TTL file. If not provided, uses default data file.
        :param kwargs: Additional keyword arguments
        :return: Graph containing nodes (packages) and edges (dependencies/conflicts)
        :rtype: Graph
        """
        # Use default file path if none provided
        if file_path is None:
            plugin_dir = Path(__file__).parent
            file_path = plugin_dir / "data" / "pkg_graph.ttl"
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"RDF data file not found: {file_path}")
        
        # Load and parse RDF data
        rdf_graph = RDFGraph()
        rdf_graph.parse(file_path, format="turtle")
        
        # Create nodes and edges
        nodes = self._create_nodes(rdf_graph)
        edges = self._create_edges(rdf_graph, nodes)
        
        # Create and return the graph
        graph = Graph(edges=edges, nodes=nodes, directed=True)
        return graph

    def _create_nodes(self, rdf_graph: RDFGraph) -> Set[Node]:
        """
        Create Node objects from package data in the RDF graph.
        
        :param rdf_graph: RDF graph containing package data
        :return: Set of Node objects representing packages
        """
        nodes = set()
        
        # Query for all packages
        packages = rdf_graph.subjects(predicate=URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), object=self.EX.Package)
        
        for package_uri in packages:
            # Extract package properties
            node_data = self._extract_package_properties(rdf_graph, package_uri)
            
            # Create node with package URI as ID
            package_id = str(package_uri).split("/")[-1]  # Extract pkg000, pkg001, etc.
            node = Node(id=package_id, data=node_data)
            nodes.add(node)
        
        return nodes

    def _extract_package_properties(self, rdf_graph: RDFGraph, package_uri: URIRef) -> Dict:
        """
        Extract all properties for a package from the RDF graph.
        
        :param rdf_graph: RDF graph
        :param package_uri: URI of the package
        :return: Dictionary of package properties
        """
        properties = {}
        
        # Map of RDF predicates to property names
        property_mapping = {
            self.FOAF.name: "name",
            self.EX.version: "version", 
            self.EX.language: "language",
            self.EX.category: "category",
            self.EX.license: "license",
            self.EX.maintainer: "maintainer",
            self.EX.downloads: "downloads",
            self.EX.isStable: "is_stable"
        }
        
        # Extract basic properties
        for predicate, prop_name in property_mapping.items():
            values = list(rdf_graph.objects(package_uri, predicate))
            if values:
                value = values[0]
                if isinstance(value, Literal):
                    # Handle typed literals
                    if value.datatype == XSD.integer:
                        properties[prop_name] = int(value)
                    elif value.datatype == XSD.boolean or prop_name == "is_stable":
                        properties[prop_name] = str(value).lower() == "true"
                    else:
                        properties[prop_name] = str(value)
                else:
                    properties[prop_name] = str(value)
        
        # Add URI for reference
        properties["uri"] = str(package_uri)
        
        return properties

    def _create_edges(self, rdf_graph: RDFGraph, nodes: Set[Node]) -> Set[Edge]:
        """
        Create Edge objects from dependency and conflict relationships.
        
        :param rdf_graph: RDF graph containing relationship data
        :param nodes: Set of nodes to find relationships between
        :return: Set of Edge objects representing relationships
        """
        edges = set()
        node_dict = {node.id: node for node in nodes}
        
        # Create dependency edges
        edges.update(self._create_dependency_edges(rdf_graph, node_dict))
        
        # Create optional dependency edges  
        edges.update(self._create_optional_dependency_edges(rdf_graph, node_dict))
        
        # Create conflict edges
        edges.update(self._create_conflict_edges(rdf_graph, node_dict))
        
        return edges

    def _create_dependency_edges(self, rdf_graph: RDFGraph, node_dict: Dict[str, Node]) -> Set[Edge]:
        """Create edges for regular dependencies."""
        edges = set()
        
        for subject, obj in rdf_graph.subject_objects(self.EX.dependsOn):
            source_id = str(subject).split("/")[-1]
            target_id = str(obj).split("/")[-1]
            
            if source_id in node_dict and target_id in node_dict:
                source_node = node_dict[source_id]
                target_node = node_dict[target_id]
                
                # Add edge type to track relationship type
                edge = Edge(source_node, target_node)
                # You could add metadata to edge if Edge class supports it
                edges.add(edge)
        
        return edges

    def _create_optional_dependency_edges(self, rdf_graph: RDFGraph, node_dict: Dict[str, Node]) -> Set[Edge]:
        """Create edges for optional dependencies."""
        edges = set()
        
        for subject, obj in rdf_graph.subject_objects(self.EX.optionalDependsOn):
            source_id = str(subject).split("/")[-1]
            target_id = str(obj).split("/")[-1]
            
            if source_id in node_dict and target_id in node_dict:
                source_node = node_dict[source_id]
                target_node = node_dict[target_id]
                
                edge = Edge(source_node, target_node)
                edges.add(edge)
        
        return edges

    def _create_conflict_edges(self, rdf_graph: RDFGraph, node_dict: Dict[str, Node]) -> Set[Edge]:
        """Create edges for package conflicts."""
        edges = set()
        
        for subject, obj in rdf_graph.subject_objects(self.EX.conflictsWith):
            source_id = str(subject).split("/")[-1]
            target_id = str(obj).split("/")[-1]
            
            if source_id in node_dict and target_id in node_dict:
                source_node = node_dict[source_id]
                target_node = node_dict[target_id]
                
                edge = Edge(source_node, target_node)
                edges.add(edge)
        
        return edges

    def name(self) -> str:
        """
        Returns the name of the data source plugin.

        :return: The name of the plugin.
        :rtype: str
        """
        return "Packages Data Source Plugin"

    def identifier(self) -> str:
        """
        Returns the identifier of the data source plugin.

        :return: The identifier of the plugin.
        :rtype: str
        """
        return "packages_data_source_plugin"