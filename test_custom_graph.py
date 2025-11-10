"""
Test GraphQA with a custom GML file

This script demonstrates how to load a GML file and use GraphQA's
natural language interface to analyze it.
"""

import networkx as nx
from graphqa.agent import UniversalRetrievalAgent
from graphqa.loaders.base_loader import BaseGraphLoader

# Option 1: Simple direct loading (recommended for quick testing)
def test_with_direct_loading(gml_file_path):
    """Load GML file and test with GraphQA - Simple approach"""

    print("="*60)
    print("Loading GML file...")
    print("="*60)

    # Load GML file using NetworkX
    graph = nx.read_gml(gml_file_path)

    # Convert to MultiDiGraph if needed (GraphQA expects MultiDiGraph)
    if not isinstance(graph, nx.MultiDiGraph):
        print(f"Converting {type(graph).__name__} to MultiDiGraph...")
        graph = nx.MultiDiGraph(graph)

    print(f"✅ Loaded graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
    print()

    # Initialize GraphQA agent
    print("Initializing GraphQA agent...")
    agent = UniversalRetrievalAgent(verbose=True)

    # Assign the graph
    agent.graph = graph
    agent.dataset_name = "custom_gml"

    # Discover schema automatically
    print("Discovering graph schema...")
    loader = BaseGraphLoader({})
    agent.schema = loader.discover_schema(graph)

    print(f"✅ Schema discovered:")
    print(f"   - Node attributes: {list(agent.schema.node_attributes.keys())[:10]}")  # Show first 10
    print(f"   - Edge attributes: {list(agent.schema.edge_attributes.keys())[:5]}")   # Show first 5
    print()

    # Initialize tools and agent
    print("Initializing agent tools...")
    agent._initialize_tools()
    agent._create_agent()

    print("✅ GraphQA ready!")
    print()

    # Ask some questions
    questions = [
        "What does this graph contain? Describe its structure.",
        "What are the most connected nodes?",
        "What attributes do the nodes have?",
        "Find any interesting patterns or communities in this graph."
    ]

    for i, question in enumerate(questions, 1):
        print("="*60)
        print(f"Question {i}: {question}")
        print("="*60)

        try:
            response = agent.ask(question)
            print(f"\n📊 Answer:\n{response}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

    # Cleanup
    agent.shutdown()
    print("✅ Test complete!")


# Option 2: Custom loader (better for reusable code)
class GMLGraphLoader(BaseGraphLoader):
    """Custom loader for GML files"""

    def __init__(self, config=None):
        super().__init__(config or {})
        self.gml_file = self.config.get('gml_file', 'graph.gml')
        self.graph_name = self.config.get('graph_name', 'Custom Graph')

    def load_graph(self) -> nx.MultiDiGraph:
        """Load GML file and return as MultiDiGraph"""
        print(f"Loading GML file: {self.gml_file}")

        # Load using NetworkX
        graph = nx.read_gml(self.gml_file)

        # Convert to MultiDiGraph if needed
        if not isinstance(graph, nx.MultiDiGraph):
            graph = nx.MultiDiGraph(graph)

        print(f"✅ Loaded {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
        return graph

    def get_dataset_description(self) -> str:
        return f"{self.graph_name} - Custom graph data loaded from GML file"

    def get_sample_queries(self) -> list[str]:
        return [
            "What is the structure of this graph?",
            "What are the most connected nodes?",
            "Find communities or clusters in the graph",
            "What attributes do nodes have?",
            "Show me nodes with unusual connection patterns"
        ]


def test_with_custom_loader(gml_file_path, graph_name="My GML Graph"):
    """Load GML file using custom loader - Better for reusable code"""

    print("="*60)
    print("Using Custom Loader Approach")
    print("="*60)
    print()

    # Create loader with config
    config = {
        'gml_file': gml_file_path,
        'graph_name': graph_name
    }
    loader = GMLGraphLoader(config)

    # Load graph
    graph = loader.load_graph()

    # Discover schema
    schema = loader.discover_schema(graph)

    # Create agent
    agent = UniversalRetrievalAgent(verbose=True)
    agent.graph = graph
    agent.schema = schema
    agent.dataset_name = graph_name.lower().replace(' ', '_')

    # Initialize
    agent._initialize_tools()
    agent._create_agent()

    print("\n✅ GraphQA ready with custom loader!")
    print()

    # Interactive mode
    print("Enter your questions (type 'quit' to exit):")
    print()

    while True:
        try:
            question = input("🤔 Ask GraphQA: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                break

            if not question:
                continue

            response = agent.ask(question)
            print(f"\n📊 Answer:\n{response}\n")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

    agent.shutdown()
    print("✅ Session ended!")


# Quick inspection helper
def inspect_gml_file(gml_file_path):
    """Quick inspection of GML file structure"""
    print("="*60)
    print("GML File Inspection")
    print("="*60)
    print()

    graph = nx.read_gml(gml_file_path)

    print(f"Graph Type: {type(graph).__name__}")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    print(f"Directed: {graph.is_directed()}")
    print()

    # Sample node attributes
    if graph.number_of_nodes() > 0:
        sample_node = list(graph.nodes(data=True))[0]
        print(f"Sample Node: {sample_node[0]}")
        print(f"Node Attributes: {list(sample_node[1].keys())}")
        print(f"Example values: {dict(list(sample_node[1].items())[:5])}")
        print()

    # Sample edge attributes
    if graph.number_of_edges() > 0:
        sample_edge = list(graph.edges(data=True))[0]
        print(f"Sample Edge: {sample_edge[0]} -> {sample_edge[1]}")
        print(f"Edge Attributes: {list(sample_edge[2].keys())}")
        print(f"Example values: {dict(list(sample_edge[2].items())[:5])}")
        print()

    # Degree distribution
    degrees = [d for n, d in graph.degree()]
    print(f"Degree Statistics:")
    print(f"  Min: {min(degrees)}")
    print(f"  Max: {max(degrees)}")
    print(f"  Avg: {sum(degrees)/len(degrees):.2f}")
    print()


if __name__ == "__main__":
    import sys

    # Update this path to your GML file
    GML_FILE = "path/to/your/graph.gml"

    if len(sys.argv) > 1:
        GML_FILE = sys.argv[1]

    print("\n🚀 GraphQA GML File Test\n")

    # Choose which approach to use:

    # 1. Quick inspection first
    inspect_gml_file(GML_FILE)

    # 2. Simple direct loading (recommended for quick tests)
    # test_with_direct_loading(GML_FILE)

    # 3. Custom loader (better for reusable code)
    test_with_custom_loader(GML_FILE, graph_name="My GML Graph")
