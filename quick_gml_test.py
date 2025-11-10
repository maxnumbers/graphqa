#!/usr/bin/env python3
"""
Quick Graph Test - Load and query graph files (GML, GraphML, etc.)

Supports: GML, GraphML (XML), NetworkX Pickle

Usage:
    python quick_gml_test.py your_graph.gml
    python quick_gml_test.py your_graph.graphml
"""

import sys
import networkx as nx
from graphqa.agent import UniversalRetrievalAgent
from graphqa.loaders.base_loader import BaseGraphLoader

def main():
    # Get GML file path
    if len(sys.argv) < 2:
        print("Usage: python quick_gml_test.py <path_to_gml_file>")
        print("Example: python quick_gml_test.py data/my_graph.gml")
        sys.exit(1)

    gml_file = sys.argv[1]

    print(f"\n🔍 Loading {gml_file}...")

    # 1. Detect format and load graph
    try:
        # Try to peek at file to detect format
        with open(gml_file, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        if first_line.startswith('<?xml') or first_line.startswith('<graphml'):
            print("📄 Detected GraphML (XML) format")
            graph = nx.read_graphml(gml_file)
        else:
            print("📄 Detected GML format")
            graph = nx.read_gml(gml_file)

    except UnicodeDecodeError:
        # Try binary formats
        print("⚠️  Text format failed, trying binary...")
        try:
            graph = nx.read_gpickle(gml_file)
            print("📄 Loaded as pickle format")
        except:
            print("❌ Could not load file in any known format")
            print("   Supported formats: GML, GraphML (XML), Pickle")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        print("\n💡 Tip: Check the file format:")
        print("   - GML: Plain text format")
        print("   - GraphML: XML format (starts with <?xml)")
        print("   - Try: nx.read_graphml() for XML files")
        sys.exit(1)

    # 2. Convert to MultiDiGraph (GraphQA requirement)
    if not isinstance(graph, nx.MultiDiGraph):
        graph = nx.MultiDiGraph(graph)

    print(f"✅ Loaded: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges\n")

    # 3. Create agent and assign graph
    agent = UniversalRetrievalAgent(verbose=True)
    agent.graph = graph
    agent.dataset_name = "custom_gml"

    # 4. Discover schema
    print("🔍 Discovering schema...")

    # Create a minimal concrete loader just for schema discovery
    class SimpleLoader(BaseGraphLoader):
        def load_graph(self):
            return graph

        def get_dataset_description(self):
            # Auto-generate description from graph structure
            node_count = graph.number_of_nodes()
            edge_count = graph.number_of_edges()
            is_directed = "directed" if graph.is_directed() else "undirected"

            # Sample node to get attributes
            sample_attrs = []
            if node_count > 0:
                sample_node = list(graph.nodes(data=True))[0]
                sample_attrs = list(sample_node[1].keys())[:5]  # First 5 attributes

            desc = f"{is_directed.capitalize()} graph with {node_count} nodes and {edge_count} edges"
            if sample_attrs:
                desc += f". Node attributes: {', '.join(sample_attrs)}"

            return desc

        def get_sample_queries(self):
            return [
                "What does this graph contain?",
                "What are the most connected nodes?",
                "Find communities or clusters",
                "What attributes do nodes have?"
            ]

    loader = SimpleLoader({})
    agent.schema = loader.discover_schema(graph)
    print(f"✅ Found {len(agent.schema.node_attributes)} node attributes, {len(agent.schema.edge_attributes)} edge attributes\n")

    # 5. Initialize tools
    print("🔧 Initializing GraphQA tools...")
    agent._initialize_tools()
    agent._create_agent()
    print("✅ Ready!\n")

    # 6. Interactive mode
    print("="*60)
    print("GraphQA Interactive Mode")
    print("="*60)
    print("Ask questions about your graph (type 'quit' to exit)\n")

    # Helpful starter questions
    print("💡 Try these questions:")
    print("  - What does this graph contain?")
    print("  - What are the most connected nodes?")
    print("  - Find communities in this graph")
    print("  - What attributes do nodes have?\n")

    while True:
        try:
            question = input("🤔 Ask: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                break

            if not question:
                continue

            # Handle special commands
            if question.lower() == 'help':
                print("\n📖 Available commands:")
                print("  - Type your question in natural language")
                print("  - 'quit' or 'exit' to exit")
                print("  - 'info' to see graph info")
                print("  - 'help' for this message\n")
                continue

            if question.lower() == 'info':
                print(f"\n📊 Graph Info:")
                print(f"  Nodes: {graph.number_of_nodes()}")
                print(f"  Edges: {graph.number_of_edges()}")
                print(f"  Directed: {graph.is_directed()}")
                print(f"  Node attributes: {list(agent.schema.node_attributes.keys())[:10]}")
                print(f"  Edge attributes: {list(agent.schema.edge_attributes.keys())[:5]}\n")
                continue

            # Ask GraphQA
            response = agent.ask(question)
            print(f"\n📊 {response}\n")

        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

    # Cleanup
    agent.shutdown()
    print("\n✅ Session ended!")


if __name__ == "__main__":
    main()
