#!/usr/bin/env python3
"""
Quick GML Test - Minimal example to load and query a GML file

Usage:
    python quick_gml_test.py your_graph.gml
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

    # 1. Load GML file
    graph = nx.read_gml(gml_file)

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
    loader = BaseGraphLoader({})
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
