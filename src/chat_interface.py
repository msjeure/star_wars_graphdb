"""
Interactive CLI Chat Interface for Star Wars GraphDB
Allows conversational interaction with the knowledge graph
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

from src.rdf_graph_loader import SWAPIGraphDB, initialize_db
from src.agent import StarWarsGraphAgent
from src.query_builder import SPARQLQueryBuilder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChatInterface:
    """Interactive chat interface for querying the Star Wars knowledge graph"""
    
    def __init__(self, db_path: str, model: str = "gpt-4"):
        """
        Initialize the chat interface
        
        Args:
            db_path: Path to the TTL file
            model: LLM model to use
        """
        print("\n📚 Initializing Star Wars Knowledge Graph...")
        self.db = initialize_db(db_path)
        
        print("🤖 Initializing AI Agent...")
        self.agent = StarWarsGraphAgent(self.db, model=model)
        
        print("✅ System ready!\n")
        
        # Print initial info
        self._print_welcome_message()
    
    def _print_welcome_message(self):
        """Print welcome message with system info"""
        stats = self.db.get_graph_stats()
        
        print("=" * 60)
        print("🌟 STAR WARS KNOWLEDGE GRAPH CHATBOT 🌟")
        print("=" * 60)
        print(f"\n📊 Graph Statistics:")
        print(f"   Total Triples: {stats['total_triples']:,}")
        print(f"   Total Entities: {stats['total_entities']:,}")
        print(f"   Total Relations: {stats['total_relations']:,}")
        print(f"\n📋 Entity Types ({len(stats['entity_types'])} types):")
        for entity_type, count in sorted(stats['entity_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"   - {entity_type}: {count}")
        
        print("\n" + "=" * 60)
        print("💬 You can ask questions like:")
        print("   - 'Who is Luke Skywalker?'")
        print("   - 'What is the average height of characters?'")
        print("   - 'List all Jedi characters'")
        print("   - 'How many planets are in the database?'")
        print("   - 'Who are the droids in the films?'")
        print("\n📝 Try 'what can you do' for capabilities, 'help' for commands, 'quit' to exit")
        print("=" * 60 + "\n")
    
    def _is_meta_question(self, user_input: str) -> Optional[str]:
        """
        Detect meta-questions about system capabilities
        Returns the command to execute, or None if it's a regular query
        """
        user_lower = user_input.lower().strip()
        
        # Remove punctuation for matching
        user_clean = user_lower.rstrip('?!.')
        
        # Meta-question patterns
        meta_patterns = {
            'what can you do': 'capabilities',
            'what can i do': 'capabilities',
            'what are your capabilities': 'capabilities',
            'capabilities': 'capabilities',
            'what are you': 'capabilities',
            'tell me about yourself': 'capabilities',
            'who are you': 'capabilities',
            'what is this': 'capabilities',
            'how does this work': 'capabilities',
            'about': 'capabilities',
            'what can this do': 'capabilities',
        }
        
        # Check for exact or near matches
        for pattern, command in meta_patterns.items():
            if user_clean == pattern or user_clean.startswith(pattern):
                return command
        
        return None
    
    def _print_capabilities(self):
        """Print system capabilities"""
        stats = self.db.get_graph_stats()
        print("\n" + "=" * 60)
        print("🤖 SYSTEM CAPABILITIES")
        print("=" * 60)
        
        print("\n✨ I can help you explore the Star Wars universe!")
        print("\n📚 What I know about:")
        for entity_type, count in sorted(stats['entity_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"   ✓ {entity_type}: {count} entries")
        
        print(f"\n📊 Available Data:")
        print(f"   ✓ Total Facts: {stats['total_triples']:,}")
        print(f"   ✓ Relationships: {stats['total_relations']}")
        
        print("\n💬 Types of questions I can answer:")
        print("   ✓ Character information: 'Who is Luke Skywalker?'")
        print("   ✓ Relationships: 'Who is Han Solo married to?'")
        print("   ✓ Properties: 'How tall is Chewbacca?'")
        print("   ✓ Filtering: 'List all Jedi'")
        print("   ✓ Aggregates: 'How many planets are there?'")
        print("   ✓ Comparisons: 'Which character is the tallest?'")
        print("   ✓ Complex queries: 'Show me characters from Tatooine and their ships'")
        
        print("\n⚙️  Special commands:")
        print("   • help - Show detailed help")
        print("   • stats - Show graph statistics")
        print("   • schema - Show available data types")
        print("   • history - Show conversation history")
        print("   • clear - Clear conversation history")
        print("   • query <sparql> - Run raw SPARQL queries")
        
        print("\n💡 Tips:")
        print("   • I use natural language processing to convert your questions to queries")
        print("   • Ask in plain English - no special syntax needed")
        print("   • I can handle follow-ups based on previous questions")
        print("   • Type 'quit' or 'exit' to end the conversation")
        
        print("\n" + "=" * 60 + "\n")
    
    def _print_help(self):
        """Print help message"""
        print("\n" + "=" * 60)
        print("📖 HELP & COMMANDS")
        print("=" * 60)
        print("\n🔍 Example Queries:")
        print("   - 'Tell me about Luke'")
        print("   - 'How many characters are there?'")
        print("   - 'What species is Yoda?'")
        print("   - 'List characters in Episode IV'")
        print("   - 'Who is from Tatooine?'")
        print("   - 'Show me all vehicles'")
        print("   - 'Average height of humans'")
        print("   - 'Relationships between characters'")
        
        print("\n⚙️  Commands:")
        print("   - 'help': Show this help message")
        print("   - 'stats': Show graph statistics")
        print("   - 'schema': Show graph schema info")
        print("   - 'query <sparql>': Execute raw SPARQL query")
        print("   - 'history': Show conversation history")
        print("   - 'clear': Clear conversation history")
        print("   - 'quit' or 'exit': Exit the chat")
        print("\n" + "=" * 60 + "\n")
    
    def _print_stats(self):
        """Print graph statistics"""
        stats = self.db.get_graph_stats()
        print("\n" + "=" * 60)
        print("📊 GRAPH STATISTICS")
        print("=" * 60)
        print(f"Total Triples: {stats['total_triples']:,}")
        print(f"Total Entities: {stats['total_entities']:,}")
        print(f"Total Relations: {stats['total_relations']:,}")
        print(f"\nEntity Type Breakdown:")
        for entity_type, count in sorted(stats['entity_types'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {entity_type}: {count}")
        print("=" * 60 + "\n")
    
    def _print_schema(self):
        """Print schema information"""
        schema = self.db.get_graph_schema()
        print("\n" + "=" * 60)
        print("📋 GRAPH SCHEMA")
        print("=" * 60)
        print(f"\nEntity Classes ({len(schema['classes'])}):")
        for cls in sorted(schema['classes'])[:15]:
            print(f"  - {cls}")
        if len(schema['classes']) > 15:
            print(f"  ... and {len(schema['classes']) - 15} more")
        
        print(f"\nRelation Properties ({len(schema['properties'])}):")
        for prop in sorted(schema['properties'])[:15]:
            print(f"  - {prop}")
        if len(schema['properties']) > 15:
            print(f"  ... and {len(schema['properties']) - 15} more")
        print("\n" + "=" * 60 + "\n")
    
    def _format_results(self, results: list, max_rows: int = 10):
        """Format query results for display"""
        if not results:
            return "❌ No results found."
        
        print(f"\n✅ Found {len(results)} result(s):\n")
        
        # Display results
        for i, result in enumerate(results[:max_rows], 1):
            print(f"{i}. {result}")
        
        if len(results) > max_rows:
            print(f"\n... and {len(results) - max_rows} more results")
        
        return ""
    
    def run(self):
        """Run the interactive chat loop"""
        while True:
            try:
                user_input = input("\n🎯 You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for meta-questions first
                meta_command = self._is_meta_question(user_input)
                if meta_command == 'capabilities':
                    self._print_capabilities()
                    continue
                
                # Handle special commands
                if user_input.lower() == 'quit' or user_input.lower() == 'exit':
                    self._print_goodbye()
                    break
                
                elif user_input.lower() == 'help':
                    self._print_help()
                    continue
                
                elif user_input.lower() == 'stats':
                    self._print_stats()
                    continue
                
                elif user_input.lower() == 'schema':
                    self._print_schema()
                    continue
                
                elif user_input.lower() == 'history':
                    self._print_history()
                    continue
                
                elif user_input.lower() == 'clear':
                    self.agent.clear_history()
                    print("✅ Conversation history cleared")
                    continue
                
                elif user_input.lower().startswith('query '):
                    # Execute raw SPARQL query
                    sparql_query = user_input[6:].strip()
                    try:
                        results = self.db.execute_sparql(sparql_query)
                        self._format_results(results)
                    except Exception as e:
                        print(f"❌ Query error: {e}")
                    continue
                
                # Regular question - use the agent
                print("\n🔄 Processing your question...")
                sparql_query, results = self.agent.query(user_input)
                
                print(f"\n🔍 Generated SPARQL Query:")
                print("─" * 60)
                print(sparql_query)
                print("─" * 60)
                
                self._format_results(results)
            
            except KeyboardInterrupt:
                self._print_goodbye()
                break
            except Exception as e:
                logger.error(f"Error: {e}")
                print(f"❌ An error occurred: {e}")
    
    def _print_history(self):
        """Print conversation history"""
        history = self.agent.get_conversation_history()
        if not history:
            print("\n📭 No conversation history yet.")
            return
        
        print("\n" + "=" * 60)
        print("💬 CONVERSATION HISTORY")
        print("=" * 60)
        for i, msg in enumerate(history, 1):
            role = "👤 You" if msg['role'] == 'user' else "🤖 Agent"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            print(f"{i}. {role}: {content}")
        print("=" * 60 + "\n")
    
    def _print_goodbye(self):
        """Print goodbye message"""
        print("\n" + "=" * 60)
        print("👋 Thank you for exploring the Star Wars Universe!")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    # Determine the path to the TTL file
    current_dir = Path(__file__).parent.parent
    ttl_path = current_dir / "SWAPI-WD-data.ttl"
    
    if not ttl_path.exists():
        print(f"❌ TTL file not found at {ttl_path}")
        sys.exit(1)
    
    # Get model choice
    model = os.getenv("SWAPI_MODEL", "gpt-4")
    
    # Create and run interface
    chat = ChatInterface(str(ttl_path), model=model)
    chat.run()


if __name__ == "__main__":
    main()
