from packages_rdf.plugin import PackagesDataSourcePlugin

if __name__ == "__main__":
    plugin = PackagesDataSourcePlugin()
    data = plugin.load_data()
    print("Test plugin executed successfully.")
    print("Data loaded:", data)
