"""
Example Notebook demonstrating the Star Wars GraphDB Agent
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent
from src.query_builder import SPARQLQueryBuilder


def example_basic_queries():
    """Example: Basic queries on the Star Wars graph"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Queries")
    print("="*60)
    
    # Initialize database
    ttl_path = Path(__file__).parent.parent / "SWAPI-WD-data.ttl"
    db = initialize_db(str(ttl_path))
    
    # Get graph stats
    stats = db.get_graph_stats()
    print(f"\nGraph has {stats['total_triples']} triples")
    print(f"Entity types: {list(stats['entity_types'].keys())[:5]}...")
    
    # Find a character by name
    print("\nSearching for 'Luke'...")
    results = db.find_by_label("Luke")
    for entity, label in results[:3]:
        print(f"  - {label}")


def example_sparql_queries():
    """Example: Direct SPARQL queries"""
    print("\n" + "="*60)
    print("EXAMPLE 2: SPARQL Queries")
    print("="*60)
    
    ttl_path = Path(__file__).parent.parent / "SWAPI-WD-data.ttl"
    db = initialize_db(str(ttl_path))
    
    # Query 1: Count characters
    query1 = """
PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?char) as ?count) WHERE {
    ?char a voc:Character .
}
"""
    results = db.execute_sparql(query1)
    print(f"\nTotal Characters: {results[0]['count'] if results else 0}")
    
    # Query 2: Find characters with their homeworlds
    query2 = """
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?charLabel ?worldLabel WHERE {
    ?char a voc:Character ;
          rdfs:label ?charLabel ;
          voc:homeworld ?world .
    ?world rdfs:label ?worldLabel .
}
LIMIT 10
"""
    results = db.execute_sparql(query2)
    print(f"\nCharacters and their homeworlds:")
    for result in results[:5]:
        print(f"  {result['charLabel']} -> {result['worldLabel']}")


def example_agent_queries():
    """Example: Using the AI agent for natural language queries"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Natural Language Agent Queries")
    print("="*60)
    
    ttl_path = Path(__file__).parent.parent / "SWAPI-WD-data.ttl"
    db = initialize_db(str(ttl_path))
    agent = StarWarsGraphAgent(db, model="gpt-4")
    
    # Example questions
    questions = [
        "How many characters are in the database?",
        "What is the average height of characters?",
        "Find all Droid characters",
    ]
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        try:
            sparql, results = agent.query(question)
            print(f"✓ Found {len(results)} results")
            if results:
                print(f"  Sample: {results[0]}")
        except Exception as e:
            print(f"✗ Error: {e}")


def example_schema_exploration():
    """Example: Explore graph schema"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Graph Schema Exploration")
    print("="*60)
    
    ttl_path = Path(__file__).parent.parent / "SWAPI-WD-data.ttl"
    db = initialize_db(str(ttl_path))
    
    schema = db.get_graph_schema()
    
    print(f"\n📋 Classes ({len(schema['classes'])}):")
    for cls in schema['classes'][:10]:
        print(f"  - {cls}")
    
    print(f"\n🔗 Properties ({len(schema['properties'])}):")
    for prop in schema['properties'][:10]:
        print(f"  - {prop}")


def example_query_builder():
    """Example: Using the query builder"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Query Builder")
    print("="*60)
    
    builder = SPARQLQueryBuilder()
    
    # Show available templates
    print("\n📚 Available Query Templates:")
    templates = builder.get_template_info()
    for template in templates[:5]:
        print(f"\n  {template['name']}")
        print(f"    Description: {template['description']}")
        print(f"    Example: {template['example']}")
    
    # Build a query
    query = builder.build_find_by_name("Luke")
    print(f"\n🔍 Built Query for 'Find Luke':")
    print(query)


if __name__ == "__main__":
    print("\n⭐ Star Wars GraphDB Examples ⭐")
    
    # Run examples
    example_basic_queries()
    example_sparql_queries()
    example_schema_exploration()
    example_query_builder()
    
    # Note: Agent examples require OpenAI API key
    print("\n💡 Note: Agent queries require OpenAI API key in OPENAI_API_KEY environment variable")
    
    print("\n✅ Examples completed!")
