# 🌟 Star Wars Knowledge Graph Agent System

An intelligent agent system for querying and exploring the Star Wars universe through RDF/SPARQL. Ask natural language questions and get instant answers from a comprehensive knowledge graph!

## Features

✨ **Natural Language Interface**: Ask questions in plain English, get accurate results  
🤖 **AI Agent**: Uses Claude/GPT to convert natural language to SPARQL queries  
🔍 **Graph Database**: Full RDF/SPARQL support with the complete SWAPI dataset  
💬 **Interactive Chat**: Conversational interface with multi-turn dialogue support  
📊 **Rich Analytics**: Explore graph statistics and schema information  
🚀 **Multi-query Patterns**: Supports complex queries about characters, planets, vehicles, and relationships  

## Architecture

```
┌─────────────────────────────────────────┐
│   User Input (Natural Language)          │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Chat Interface (CLI)                   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   AI Agent (GPT-4/Claude)               │
│   - Converts NL → SPARQL                │
│   - Understands context                 │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   Query Builder                          │
│   - Templates                           │
│   - SPARQL Generation                   │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   RDF Graph Database (RDFlib)           │
│   - SPARQL Executor                     │
│   - Graph Analytics                     │
└────────────┬────────────────────────────┘
             │
┌────────────▼────────────────────────────┐
│   SWAPI-WD-data.ttl (RDF Data)          │
│   - 11,914 triples                      │
│   - Characters, Planets, Vehicles, etc. │
└─────────────────────────────────────────┘
```

## Project Structure

```
star_wars_graphdb/
├── SWAPI-WD-data.ttl           # RDF data file
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
├── src/
│   ├── __init__.py
│   ├── rdf_graph_loader.py    # RDF graph management
│   ├── query_builder.py        # SPARQL query templates
│   ├── agent.py                # AI agent (NL → SPARQL)
│   ├── chat_interface.py       # Interactive CLI
│   └── examples.py             # Usage examples
├── notebooks/
│   └── demo.ipynb              # Jupyter notebook demo
└── README.md
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Clone/Navigate to the project directory**
```bash
cd /Users/mashijia/Desktop/star_wars_graphdb
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up API Key (optional, for full AI capabilities)**

Using OpenAI:
```bash
export OPENAI_API_KEY="sk-your-key-here"
export SWAPI_MODEL="gpt-4"
```

Or using Moonshotai/Kimi:
```bash
export MOONSHOTAI_API_KEY="your-moonshotai-key-here"
export SWAPI_MODEL="kimi-k2.5"
```

If no API key is set, the system will use pattern-based query generation.

## Usage

### Interactive Chat Interface

Start the interactive chat:
```bash
python main.py
```

### Example Queries

Once in the chat, try these questions:

**Character Queries**
- "Who is Luke Skywalker?"
- "Tell me about Yoda"
- "List all Jedi characters"
- "What species is Chewbacca?"

**Statistics & Analytics**
- "How many characters are in the database?"
- "What is the average height of humans?"
- "How many planets are there?"
- "Count all droid characters"

**Relationships**
- "What is Luke's homeworld?"
- "Who appears in Episode IV?"
- "Show all vehicles in the films"
- "List characters from Tatooine"

**Complex Queries**
- "Which characters have the highest height?"
- "What movies feature the most characters?"
- "Find all female characters and their homeworlds"

### Commands in Chat

- `help` - Show help message with examples
- `stats` - Display graph statistics
- `schema` - Show entity types and properties
- `history` - View conversation history
- `clear` - Clear conversation history
- `query <SPARQL>` - Execute raw SPARQL query
- `quit` or `exit` - Exit the application

### Run Examples

Explore the codebase with example queries:
```bash
python -m src.examples
```

### Direct Python API

Use the system programmatically:

```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

# Initialize the database
db = initialize_db("SWAPI-WD-data.ttl")

# Create an agent
agent = StarWarsGraphAgent(db, model="gpt-4")

# Query
sparql_query, results = agent.query("Who is Luke Skywalker?")
print(f"Query: {sparql_query}")
print(f"Results: {results}")
```

## Data Overview

The graph contains:
- **11,914 RDF triples**
- **Characters**: Names, species, height, mass, eye color, skin color, homeworld, films
- **Planets**: Names, climate, terrain, population, diameter
- **Vehicles**: Names, manufacturer, model, class
- **Starships**: Names, manufacturer, model, class
- **Films**: Episode numbers, directors, release dates, opening crawls

### Entity Types
```
Character (70+ entities)
Planet (60+ entities)
Vehicle (30+ entities)
Starship (30+ entities)
Droid (10+ entities)
And 50+ species types (Human, Ewok, Jedi, etc.)
```

## Technical Details

### Components

#### 1. RDF Graph Loader (`rdf_graph_loader.py`)
- Loads TTL files using RDFlib
- Provides graph schema introspection
- Executes SPARQL queries
- Entity search and property extraction

#### 2. Query Builder (`query_builder.py`)
- Pre-built SPARQL query templates
- Dynamic query generation
- Common query patterns

#### 3. AI Agent (`agent.py`)
- Natural language understanding with GPT-4/Claude
- Converts NL questions to SPARQL queries
- Error recovery and query refinement
- Conversation history tracking

#### 4. Chat Interface (`chat_interface.py`)
- Interactive command-line interface
- Rich output formatting
- Help and documentation
- Command support

### SPARQL Prefixes Used

```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX swapi: <https://swapi.co/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```

## Example SPARQL Queries

### Find a character by name
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label WHERE {
    ?entity rdfs:label ?label ;
            a voc:Character .
    FILTER(CONTAINS(LCASE(str(?label)), "luke"))
}
```

### Count characters by species
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>

SELECT ?species (COUNT(?char) as ?count) WHERE {
    ?char a voc:Character ;
          a ?species .
    FILTER(?species != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
}
GROUP BY ?species
ORDER BY DESC(?count)
```

### Find character's homeworld
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?charLabel ?planetLabel WHERE {
    ?char rdfs:label ?charLabel ;
          voc:homeworld ?planet .
    ?planet rdfs:label ?planetLabel .
    FILTER(CONTAINS(LCASE(str(?charLabel)), "luke"))
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - OpenAI API key for GPT models (optional)
- `MOONSHOTAI_API_KEY` - Moonshotai API key for Kimi models (optional)
- `SWAPI_MODEL` - Model to use (default: "gpt-4")
  - OpenAI: "gpt-4", "gpt-3.5-turbo"
  - Moonshotai: "kimi-k2.5"

Set them:
```bash
# Using Moonshotai/Kimi
export MOONSHOTAI_API_KEY="your-key-here"
export SWAPI_MODEL="kimi-k2.5"

# Or using OpenAI
export OPENAI_API_KEY="sk-..."
export SWAPI_MODEL="gpt-4"
```

The system will auto-detect which provider to use based on your configuration.

### Logging

Logging is configured to INFO level by default. Modify in the modules:
```python
logging.basicConfig(level=logging.DEBUG)  # For verbose output
```

## Advanced Usage

### Creating Custom Query Templates

Add new templates to `SPARQLQueryBuilder.TEMPLATES`:

```python
from src.query_builder import SPARQLQueryBuilder

builder = SPARQLQueryBuilder()
# Template already exist - use them:
query = builder.build_find_by_name("Luke")
results = db.execute_sparql(query)
```

### Extending the Agent

Modify `StarWarsGraphAgent` to:
- Use different LLM models
- Add custom prompt engineering
- Implement caching
- Add conversation memory

```python
from src.agent import StarWarsGraphAgent

agent = StarWarsGraphAgent(db, model="gpt-3.5-turbo")
# Customize system prompts, etc.
```

## Troubleshooting

### "TTL file not found"
- Ensure `SWAPI-WD-data.ttl` is in the project root
- Check file path in your code

### "OpenAI API key not found"
- Set `OPENAI_API_KEY` environment variable
- System will fall back to pattern-based queries if not set

### Query returns no results
- Try the `schema` command to see available entity types
- Use `query` command to test SPARQL directly
- Check spelling of entity names

### Slow query execution
- Reduce the LIMIT in SPARQL queries
- Complex queries may take longer - be patient
- Consider caching frequently-used queries

## Performance

- Graph loading: ~2-5 seconds
- Simple queries: <100ms
- Complex queries: 100ms-1s
- Agent query generation (with API): 1-3 seconds

## Future Enhancements

🔮 Planned features:
- [ ] Web interface (Flask/FastAPI)
- [ ] Caching layer for common queries
- [ ] Multi-language support
- [ ] Streaming responses
- [ ] Graph visualization
- [ ] Query result caching
- [ ] More sophisticated error recovery
- [ ] Support for additional LLMs (Ollama, Hugging Face)
- [ ] Entity disambiguation
- [ ] Context-aware follow-up questions

## Contributing

Suggestions and improvements welcome! Areas for contribution:
- Additional query templates
- Better error handling
- Performance optimizations
- Documentation improvements
- New visualization features

## License

This project uses the Star Wars API (SWAPI) data. Check SWAPI's license for usage terms.

## References

- [SWAPI - Star Wars API](https://swapi.dev/)
- [RDFlib Documentation](https://rdflib.readthedocs.io/)
- [SPARQL Tutorial](https://www.w3.org/TR/sparql11-query/)
- [OpenAI API](https://platform.openai.com/)

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review examples in `src/examples.py`
3. Check SPARQL syntax with raw `query` command
4. Review logs for detailed error messages

---

**Happy exploring the Star Wars universe! May the Force be with you! 🌟**
