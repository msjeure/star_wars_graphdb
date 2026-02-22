# API Reference - Star Wars GraphDB

Complete API documentation for developers integrating the Star Wars GraphDB agent system.

---

## 📦 Module: `src.rdf_graph_loader`

### Class: `SWAPIGraphDB`

Main class for RDF graph management and SPARQL query execution.

#### Constructor

```python
SWAPIGraphDB(ttl_file_path: str)
```

**Parameters:**
- `ttl_file_path` (str): Path to the TTL file

**Example:**
```python
from src.rdf_graph_loader import SWAPIGraphDB

db = SWAPIGraphDB("SWAPI-WD-data.ttl")
```

#### Methods

##### `load_graph()`
Load RDF data from TTL file into the graph.

```python
db.load_graph()
```

**Returns:** None

---

##### `execute_sparql(query: str) -> List[Dict]`
Execute a SPARQL query and return results.

**Parameters:**
- `query` (str): SPARQL query string

**Returns:** List of dictionaries with result bindings

**Example:**
```python
results = db.execute_sparql("""
    PREFIX voc: <https://swapi.co/vocabulary/>
    SELECT ?char WHERE {
        ?char a voc:Character .
    }
    LIMIT 10
""")

for result in results:
    print(result)
```

---

##### `get_graph_schema() -> Dict`
Extract and return schema information from the graph.

**Returns:** Dictionary with:
- `classes`: List of entity types
- `properties`: List of properties
- `sample_data`: Sample entities for each type

**Example:**
```python
schema = db.get_graph_schema()
print(f"Classes: {schema['classes']}")
print(f"Properties: {schema['properties']}")
```

---

##### `find_by_label(label: str) -> List[Tuple]`
Find entities by their label/name (case-insensitive).

**Parameters:**
- `label` (str): Label to search for

**Returns:** List of (entity_uri, entity_label) tuples

**Example:**
```python
results = db.find_by_label("Luke")
for entity_uri, label in results:
    print(f"{label} ({entity_uri})")
```

---

##### `get_entity_properties(entity_uri: str) -> Dict`
Get all properties of a specific entity.

**Parameters:**
- `entity_uri` (str): URI of the entity

**Returns:** Dictionary of properties and values

**Example:**
```python
props = db.get_entity_properties("https://swapi.co/resource/character/5")
print(props)
# {'label': 'Luke Skywalker', 'height': '172.0', ...}
```

---

##### `get_graph_stats() -> Dict`
Get basic statistics about the graph.

**Returns:** Dictionary with:
- `total_triples`: Total RDF triples
- `total_entities`: Total unique entities
- `total_relations`: Total unique relations
- `entity_types`: Count by entity type

**Example:**
```python
stats = db.get_graph_stats()
print(f"Total triples: {stats['total_triples']}")
print(f"Entity types: {stats['entity_types']}")
```

---

### Function: `initialize_db(ttl_path: str) -> SWAPIGraphDB`

Convenience function to initialize the database.

**Parameters:**
- `ttl_path` (str): Path to TTL file

**Returns:** SWAPIGraphDB instance

**Example:**
```python
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")
```

---

## 📦 Module: `src.query_builder`

### Class: `SPARQLQueryBuilder`

Template-based SPARQL query generation.

#### Constructor

```python
SPARQLQueryBuilder()
```

**Example:**
```python
from src.query_builder import SPARQLQueryBuilder

builder = SPARQLQueryBuilder()
```

#### Methods

##### `build_find_by_name(name: str) -> str`
Build a query to find entities by name.

**Parameters:**
- `name` (str): Name to search for

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_find_by_name("Luke")
results = db.execute_sparql(query)
```

---

##### `build_characters_by_species(species: str) -> str`
Build a query to find characters of a specific species.

**Parameters:**
- `species` (str): Species name (e.g., "Human", "Droid")

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_characters_by_species("Droid")
results = db.execute_sparql(query)
```

---

##### `build_characters_by_film(film_name: str) -> str`
Build a query to find characters in a specific film.

**Parameters:**
- `film_name` (str): Film name or episode

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_characters_by_film("A New Hope")
results = db.execute_sparql(query)
```

---

##### `build_count_query(entity_type: str) -> str`
Build a query to count entities of a type.

**Parameters:**
- `entity_type` (str): Entity type (e.g., "Character", "Planet")

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_count_query("Character")
results = db.execute_sparql(query)
# Returns: [{'count': 70}]
```

---

##### `build_homeworld_query(character_name: str) -> str`
Build a query to find character's homeworld.

**Parameters:**
- `character_name` (str): Character name

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_homeworld_query("Luke")
results = db.execute_sparql(query)
```

---

##### `build_species_stats(species: str) -> str`
Build a query to get species statistics.

**Parameters:**
- `species` (str): Species name

**Returns:** SPARQL query string

**Example:**
```python
query = builder.build_species_stats("Human")
results = db.execute_sparql(query)
```

---

##### `get_template_info() -> List[Dict]`
Get information about available templates.

**Returns:** List of dictionaries with template info

**Example:**
```python
templates = builder.get_template_info()
for t in templates:
    print(f"{t['name']}: {t['example']}")
```

---

### Function: `build_simple_sparql(entity_type: str, filters: Optional[Dict] = None) -> str`

Build a simple SPARQL query with optional filters.

**Parameters:**
- `entity_type` (str): Type of entity to query
- `filters` (Dict, optional): Filters to apply

**Returns:** SPARQL query string

**Example:**
```python
from src.query_builder import build_simple_sparql

query = build_simple_sparql("Character")
results = db.execute_sparql(query)
```

---

## 📦 Module: `src.agent`

### Class: `StarWarsGraphAgent`

AI agent for converting natural language to SPARQL.

#### Constructor

```python
StarWarsGraphAgent(graph_db: SWAPIGraphDB, model: str = "gpt-4", api_key: Optional[str] = None)
```

**Parameters:**
- `graph_db` (SWAPIGraphDB): Graph database instance
- `model` (str): LLM model to use (default: "gpt-4")
- `api_key` (str, optional): OpenAI API key

**Example:**
```python
from src.agent import StarWarsGraphAgent

agent = StarWarsGraphAgent(db, model="gpt-4")
# Or with API key
agent = StarWarsGraphAgent(db, api_key="sk-...")
```

#### Methods

##### `query(question: str) -> Tuple[str, List[Dict]]`
Convert natural language question to SPARQL and execute.

**Parameters:**
- `question` (str): Natural language question

**Returns:** Tuple of (SPARQL query, results list)

**Example:**
```python
sparql_query, results = agent.query("Who is Luke Skywalker?")
print(f"Query: {sparql_query}")
print(f"Results: {results}")
```

---

##### `get_system_prompt() -> str`
Generate the system prompt with graph schema.

**Returns:** System prompt string

**Example:**
```python
prompt = agent.get_system_prompt()
print(prompt)
```

---

##### `get_conversation_history() -> List[Dict]`
Get the conversation history.

**Returns:** List of message dictionaries with 'role' and 'content'

**Example:**
```python
history = agent.get_conversation_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

---

##### `clear_history()`
Clear conversation history.

**Returns:** None

**Example:**
```python
agent.clear_history()
```

---

### Function: `create_agent(graph_db: SWAPIGraphDB, model: str = "gpt-4") -> StarWarsGraphAgent`

Convenience function to create an agent.

**Parameters:**
- `graph_db` (SWAPIGraphDB): Graph database instance
- `model` (str): LLM model to use

**Returns:** StarWarsGraphAgent instance

**Example:**
```python
from src.agent import create_agent

agent = create_agent(db, model="gpt-4")
sparql, results = agent.query("Tell me about Yoda")
```

---

## 📦 Module: `src.chat_interface`

### Class: `ChatInterface`

Interactive chat interface for querying the knowledge graph.

#### Constructor

```python
ChatInterface(db_path: str, model: str = "gpt-4")
```

**Parameters:**
- `db_path` (str): Path to TTL file
- `model` (str): LLM model to use

**Example:**
```python
from src.chat_interface import ChatInterface

chat = ChatInterface("SWAPI-WD-data.ttl", model="gpt-4")
```

#### Methods

##### `run()`
Run the interactive chat loop.

**Returns:** None (blocks until user exits)

**Example:**
```python
chat.run()
# User can now type questions interactively
```

---

## 🔍 Common Integration Patterns

### Pattern 1: Basic Query

```python
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")
results = db.execute_sparql("""
    PREFIX voc: <https://swapi.co/vocabulary/>
    SELECT ?char WHERE { ?char a voc:Character . }
    LIMIT 10
""")

print(f"Found {len(results)} characters")
```

### Pattern 2: Natural Language with Agent

```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db)

sparql, results = agent.query("Who is the tallest character?")
print(f"SPARQL: {sparql}")
print(f"Results: {results}")
```

### Pattern 3: Multi-Turn Conversation

```python
agent = StarWarsGraphAgent(db)

# First question
q1, r1 = agent.query("Who is Luke?")
print(f"Luke: {r1}")

# Follow-up question
q2, r2 = agent.query("What's his homeworld?")
print(f"Homeworld: {r2}")

# View conversation
history = agent.get_conversation_history()
```

### Pattern 4: Schema Exploration

```python
db = initialize_db("SWAPI-WD-data.ttl")

# Get schema
schema = db.get_graph_schema()
print(f"Available classes: {schema['classes']}")
print(f"Available properties: {schema['properties']}")

# Get statistics
stats = db.get_graph_stats()
print(f"Total triples: {stats['total_triples']}")
print(f"Entity breakdown: {stats['entity_types']}")
```

### Pattern 5: Entity Lookup

```python
# Search by name
results = db.find_by_label("Luke")
for uri, label in results:
    print(f"Found: {label}")

# Get properties
props = db.get_entity_properties(uri)
for key, value in props.items():
    print(f"  {key}: {value}")
```

### Pattern 6: Query Building

```python
from src.query_builder import SPARQLQueryBuilder

builder = SPARQLQueryBuilder()

# Use templates
query = builder.build_count_query("Character")
results = db.execute_sparql(query)
print(f"Total characters: {results[0]['count']}")

# List templates
templates = builder.get_template_info()
for t in templates:
    print(f"- {t['name']}: {t['example']}")
```

---

## 🔧 Configuration

### Environment Variables

```python
import os

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Model to use
model = os.getenv("SWAPI_MODEL", "gpt-4")

# Logging level
log_level = os.getenv("LOG_LEVEL", "INFO")
```

### Using .env File

```python
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SWAPI_MODEL = os.getenv("SWAPI_MODEL")
```

---

## ⚡ Performance Considerations

### Query Performance

- Simple queries: <100ms
- Complex queries: 100ms-1s
- Graph loading: 2-5 seconds
- API calls: 1-3 seconds

### Optimization Tips

```python
# Use LIMIT for large result sets
query = "SELECT ... WHERE { ... } LIMIT 50"

# Use FILTER for specific matches
query = "FILTER(CONTAINS(LCASE(...), 'luke'))"

# Cache frequent queries
@cache.cached(timeout=3600)
def get_characters():
    return db.execute_sparql(query)
```

---

## 🐛 Error Handling

### Common Exceptions

```python
try:
    results = db.execute_sparql(invalid_query)
except Exception as e:
    print(f"Query error: {e}")
    # Agent will attempt to refine the query
```

### Fallback Behavior

```python
# Without API key: Pattern-based generation
# Without results: Refined query generation
# With timeout: Fallback query

agent = StarWarsGraphAgent(db)  # Works even without API key!
```

---

## 📚 Data Types

### SPARQL Result Row

```python
{
    'char': URIRef('https://swapi.co/resource/character/5'),
    'label': Literal('Luke Skywalker'),
    'height': Literal('172.0'),
}
```

### Graph Schema

```python
{
    'classes': ['Character', 'Planet', 'Vehicle', ...],
    'properties': ['height', 'mass', 'homeworld', ...],
    'sample_data': {
        'Character': ['swapi:char/1', 'swapi:char/2', ...],
        ...
    }
}
```

### Graph Statistics

```python
{
    'total_triples': 11914,
    'total_entities': 500,
    'total_relations': 50,
    'entity_types': {
        'Character': 70,
        'Droid': 10,
        'Planet': 60,
        ...
    }
}
```

---

## 🔗 Namespace Prefixes

```python
PREFIX voc:   <https://swapi.co/vocabulary/>
PREFIX swapi: <https://swapi.co/resource/>
PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
```

---

## 📖 Quick Reference

| Task | Module | Function |
|------|--------|----------|
| Load graph | `rdf_graph_loader` | `initialize_db()` |
| Execute SPARQL | `rdf_graph_loader` | `db.execute_sparql()` |
| Find by name | `rdf_graph_loader` | `db.find_by_label()` |
| Get statistics | `rdf_graph_loader` | `db.get_graph_stats()` |
| Get schema | `rdf_graph_loader` | `db.get_graph_schema()` |
| Build query | `query_builder` | `builder.build_*()` |
| Natural language | `agent` | `agent.query()` |
| Chat interface | `chat_interface` | `ChatInterface.run()` |

---

## Version Info

**API Version**: 1.0  
**Last Updated**: February 2026  
**Compatible With**: Python 3.8+

---

For more information, see README.md or ARCHITECTURE.md
