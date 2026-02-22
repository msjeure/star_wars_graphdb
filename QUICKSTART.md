# Quick Start Guide - Star Wars GraphDB Agent

## 30-Second Setup

```bash
# 1. Navigate to project
cd /Users/mashijia/Desktop/star_wars_graphdb

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the chat interface
python main.py
```

## Try These Questions Immediately

Once the chat starts, copy-paste these:

```
How many characters are in the database?
Who is Luke Skywalker?
List all Droid characters
What is the average height of humans?
Show me characters from Tatooine
How many planets are there?
What species is Yoda?
List vehicles in the films
```

## With Moonshotai/Kimi (Better Results)

```bash
# Set your Moonshotai key
export MOONSHOTAI_API_KEY="your-kimi-key-here"
export SWAPI_MODEL="kimi-k2.5"

# Then run
python main.py
```

Or use OpenAI:

```bash
# Set your OpenAI key
export OPENAI_API_KEY="sk-your-key-here"
export SWAPI_MODEL="gpt-4"

# Then run
python main.py
```

For detailed Moonshotai setup, see [MOONSHOTAI_SETUP.md](MOONSHOTAI_SETUP.md)

## Understanding the System

### What happens when you ask a question:

1. **You ask** → "Who is Luke Skywalker?"
2. **Chat Interface** → Receives your question
3. **AI Agent** → Converts to SPARQL query using GPT-4
4. **Query Builder** → Refines the query if needed
5. **RDF Database** → Executes SPARQL against the graph
6. **Results** → Formatted and displayed to you

### Example Flow:

```
You: "How many droids are there?"
     ↓
Agent generates:
PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?droid) as ?count) WHERE {
    ?droid a voc:Droid .
}
     ↓
Database returns: ?count = 10
     ↓
You see: "Found 1 result(s): {'count': 10}"
```

## Available Commands in Chat

| Command | Purpose |
|---------|---------|
| `help` | Show all available commands |
| `stats` | View graph statistics |
| `schema` | See available entity types and properties |
| `history` | View conversation history |
| `clear` | Clear conversation history |
| `query [SPARQL]` | Execute raw SPARQL query |
| `quit` / `exit` | Exit the application |

## Data You Can Query

### Characters
- 70+ characters (Luke, Leia, Han, Yoda, etc.)
- Properties: name, species, height, mass, eye color, homeworld, films

### Planets  
- 60+ planets (Tatooine, Alderaan, Coruscant, etc.)
- Properties: name, climate, terrain, population, diameter

### Vehicles & Starships
- 60+ vehicles and starships
- Properties: name, manufacturer, model, class

### Relationships
- Character → Film appearances
- Character → Homeworld
- Character → Species
- Vehicle → Manufacturer

## Example Queries to Try

### Character Queries
```
Tell me about Darth Vader
What is C-3PO?
Who is the tallest character?
List all female characters
```

### Statistics
```
How many species are there?
Average height of all characters?
Count characters by species
How many characters appear in multiple films?
```

### Relationships
```
Which characters are from Tatooine?
Who appeared in Episode IV?
What vehicles does Luke use?
Show me characters from the same homeworld
```

## Troubleshooting

### Chat won't start
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check if TTL file exists
ls -la SWAPI-WD-data.ttl

# Check dependencies
pip list | grep rdflib
```

### Queries return no results
```bash
# Try checking the schema first
In chat: schema

# Try a simple count
In chat: query PREFIX voc: <https://swapi.co/vocabulary/> SELECT (COUNT(?x) as ?count) WHERE { ?x a voc:Character . }
```

### OpenAI errors
```bash
# Verify API key
echo $OPENAI_API_KEY

# Set it if not found
export OPENAI_API_KEY="sk-..."
```

## Working With Raw SPARQL

To execute SPARQL directly:

```
query PREFIX voc: <https://swapi.co/vocabulary/> PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?entity ?label WHERE { ?entity a voc:Character ; rdfs:label ?label . } LIMIT 5
```

## Under the Hood

### Architecture Components:

```
chat_interface.py       ← Your interface here
      ↓
   agent.py             ← AI converts NL to SPARQL
      ↓
query_builder.py        ← SPARQL templates
      ↓
rdf_graph_loader.py     ← RDF database operations
      ↓
SWAPI-WD-data.ttl       ← The data
```

### File Purposes:

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `rdf_graph_loader.py` | Loads and queries RDF data |
| `query_builder.py` | SPARQL template generation |
| `agent.py` | NL → SPARQL conversion with LLM |
| `chat_interface.py` | User interaction layer |
| `examples.py` | Usage examples |

## Next Steps

1. **Basic Usage** → Run `python main.py` and try the example queries
2. **Explore Schema** → Type `schema` to see what data is available
3. **Learn SPARQL** → Use `query` command to test SPARQL directly
4. **API Integration** → Use the Python API in your own code:

```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db)
sparql, results = agent.query("Who is Luke Skywalker?")
print(results)
```

## Key Concepts

- **RDF**: Resource Description Framework - a way to represent data as triples (subject-predicate-object)
- **SPARQL**: Query language for RDF data
- **Graph DB**: Database that stores and queries relationships between entities
- **Agent**: AI system that understands natural language and converts it to database queries

## Advanced Tips

### Performance
- Start with specific queries (filter by name)
- Use LIMIT to reduce results
- Complex queries may take 1-2 seconds

### Better Results  
- Be specific with names and terms
- Follow-up questions can refine results
- Check schema if unsure of entity types

### Debugging
- Use `query` command to test SPARQL
- Check `history` to see what was generated
- Review the printed SPARQL queries

---

**You're ready! Run `python main.py` and start exploring! 🚀**

Questions? Check README.md for more details.
