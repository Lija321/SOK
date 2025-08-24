from movies_json.plugin import MoviesDataSourcePlugin

if __name__ == "__main__":
    plugin = MoviesDataSourcePlugin()
    graph = plugin.load_data()
    print("Test plugin executed successfully.")
    print("Number of nodes:", len(graph.nodes))
    print("Number of edges:", len(graph.edges))
    print("Top 3 movies:", [m.data["title"] for m in plugin.get_top_rated_movies(graph.nodes, 3)])