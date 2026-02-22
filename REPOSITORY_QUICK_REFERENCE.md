# Code Repository - Quick Reference 🎯

## What Does This Code Do?

A **Natural Language Query System** for Star Wars RDF data. Ask questions in English, get answers from the knowledge graph.

```
User: "Who is Luke Skywalker?"
System: Converts to SPARQL → Queries RDF graph → Shows answer
```

---

## Directory Structure at a Glance

```
star_wars_graphdb/
├── main.py                    # START HERE - Entry point
├── SWAPI-WD-data.ttl          # RDF database (68,981 triples)
├── requirements.txt           # pip install -r requirements.txt
│
├── src/
│   ├── chat_interface.py      # 💬 User interaction
│   ├── agent.py               # 🤖 Query generation
│   ├── rdf_graph_loader.py    # 📊 Database management
│   ├── query_builder.py       # 📝 SPARQL templates
│   └── examples.py            # 📖 API usage examples
│
└── docs/
    ├── README.md              # Full documentation
    ├── ARCHITECTURE_EXPLAINED.md   # This explanation
    └── ... (more guides)
```

---

## Core Modules - What They Do

| Module | Responsibility | Key Classes |
|--------|-----------------|-------------|
| **chat_interface.py** | User interaction | `ChatInterface` |
| **agent.py** | Query generation | `StarWarsGraphAgent` |
| **rdf_graph_loader.py** | Database access | `SWAPIGraphDB` |
| **query_builder.py** | Query templates | `SPARQLQueryBuilder` |

---

## How Code Flows

### 1️⃣ User Asks Question
```python
# in chat_interface.py: ChatInterface.run()
user_input = input("? > ")  # "Who is Luke?"
```

### 2️⃣ Check If It's About System
```python
# in chat_interface.py: _is_meta_question()
if "what can you do" in question:
    show_capabilities()  # Not a data query
```

### 3️⃣ Generate SPARQL
```python
# in agent.py: StarWarsGraphAgent.query()
sparql = agent._generate_sparql_query(question)
# Uses LLM or pattern matching
```

### 4️⃣ Execute Query
```python
# in rdf_graph_loader.py: SWAPIGraphDB.execute_sparql()
results = graph.query(sparql)
```

### 5️⃣ Show Results
```python
# in chat_interface.py: _format_results()
display(results)
```

---

## API Providers

### Three Options (Automatic Detection)

```python
export SWAPI_MODEL="kimi-k2.5"      # → Use Moonshotai
export SWAPI_MODEL="gpt-4"          # → Use OpenAI
# No API key?                        # → Use pattern matching
```

**How Detection Works** (in `agent.py: _init_llm_client()`):
```python
if model.startswith("kimi"):
    use Moonshotai at api.moonshot.cn/v1
elif model.startswith("gpt"):
    use OpenAI at api.openai.com/v1
else:
    use local pattern matching
```

---

## Important Classes & Methods

### ChatInterface
```python
class ChatInterface:
    def __init__(db_path, model)     # Initialize with TTL file
    def run()                         # Main interaction loop
    def _is_meta_question()           # Detect "what can you do?"
    def _print_capabilities()         # Show system capabilities
```

### StarWarsGraphAgent
```python
class StarWarsGraphAgent:
    def __init__(graph_db, model)    # Initialize with database
    def query(question)               # Main method: question → results
    def _generate_sparql_query()      # Convert natural language
    def _generate_with_gpt()          # Use LLM
    def _generate_with_patterns()     # Use fallback
    def _refine_query_on_error()      # Fix broken queries
```

### SWAPIGraphDB
```python
class SWAPIGraphDB:
    def __init__(ttl_file_path)      # Load RDF data
    def execute_sparql(query)         # Execute SPARQL query
    def get_graph_schema()            # Get data structure
    def get_graph_stats()             # Get statistics
    def find_by_label(label)          # Search entities
```

---

## Key Code Patterns

### Pattern 1: Using the System as a User
```bash
export MOONSHOTAI_API_KEY="your-key"
export SWAPI_MODEL="kimi-k2.5"
python main.py

? > Who is Luke Skywalker?
? > How many planets?
? > quit
```

### Pattern 2: Using the API in Code
```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

# Initialize
db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db, model="gpt-4")

# Query
sparql_query, results = agent.query("Who is Luke?")

# Use results
for result in results:
    print(result)
```

### Pattern 3: Direct Database Access
```python
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")

# Execute SPARQL directly
results = db.execute_sparql("""
    PREFIX voc: <https://swapi.co/vocabulary/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?label WHERE {
        ?x a voc:Character ;
           rdfs:label ?label .
    }
    LIMIT 10
""")

for row in results:
    print(row['label'])
```

---

## Configuration

### Environment Variables

```bash
# API Provider - Choose ONE
export OPENAI_API_KEY="sk-..."        # For OpenAI
export MOONSHOTAI_API_KEY="your-key"  # For Moonshotai

# Model Selection
export SWAPI_MODEL="gpt-4"             # Which model to use

# Logging (optional)
export LOG_LEVEL="INFO"
```

### .env File
```bash
# Copy from .env.example
cp .env.example .env

# Edit .env with your keys
```

---

## Data Information

### What's in the Graph?

```
Total: 68,981 RDF triples
Entities: 1,388
Relations: 65

Top Entity Types:
  FilmRole: 345
  Person: 249
  Character: 87
  Planet: 61
  Starship: 37
  Species: 38
  Vehicle: 39
```

### RDF Namespaces

```
voc:   https://swapi.co/vocabulary/     # Types & properties
swapi: https://swapi.co/resource/       # Entities
rdfs:  http://www.w3.org/2000/01/rdf-schema#  # Labels
rdf:   http://www.w3.org/1999/02/22-rdf-syntax-ns#  # Types
```

### Example Entities

```
Character:
  URI: swapi:luke_skywalker
  Label: Luke Skywalker
  Properties: height, mass, species, homeworld, ...

Planet:
  URI: swapi:tatooine
  Label: Tatooine
  Properties: diameter, climate, gravity, ...

Starship:
  URI: swapi:x_wing_fighter
  Label: X-Wing Fighter
  Properties: model, manufacturer, length, ...
```

---

## Special Commands

In the interactive chat:

```
? > help              # Show help
? > stats             # Show graph statistics
? > schema            # Show data structure
? > history           # Show conversation history
? > clear             # Clear conversation history
? > query <sparql>    # Execute raw SPARQL
? > what can you do   # Show capabilities
? > quit              # Exit
```

---

## Common Tasks

### Task 1: Ask About Star Wars Data
```bash
python main.py
? > Who is Yoda?
? > How many planets are there?
? > List all droids
```

### Task 2: Query via Python API
```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db, model="gpt-4")

query, results = agent.query("How many characters?")
print(f"SPARQL: {query}")
print(f"Results: {results}")
```

### Task 3: Execute Custom SPARQL
```bash
python main.py
? > query SELECT ?label WHERE { ?x a <https://swapi.co/vocabulary/Character> ; <http://www.w3.org/2000/01/rdf-schema#label> ?label . } LIMIT 5
```

### Task 4: Get System Info
```bash
python main.py
? > what can you do   # Show capabilities
? > stats             # Show statistics
? > schema            # Show data types
```

---

## Error Handling

### If Query Fails
1. System logs error
2. System tries to refine query using LLM
3. If still fails, returns empty results
4. User is notified

### If API Unavailable
1. System falls back to pattern matching
2. Pattern-based SPARQL generation
3. No API key needed

### If Data File Missing
1. System checks for SWAPI-WD-data.ttl
2. Shows error if not found
3. Exits gracefully

---

## Performance Notes

```
RDF Load Time:         2-3 seconds (once on startup)
SPARQL Execution:      <100ms (typical)
LLM API Call:          1-3 seconds
Pattern Matching:      <50ms
Total Response Time:   2-5 seconds (LLM) or <500ms (pattern)
```

---

## Extension Points

### Add a New Command
```python
# in chat_interface.py: run()
elif user_input.lower() == "mynewcommand":
    self._handle_mynewcommand()
    continue
```

### Add a New SPARQL Template
```python
# in query_builder.py: TEMPLATES
"my_template": QueryTemplate(
    name="my_template",
    description="What it does",
    template="PREFIX ... SELECT ...",
    example="Example usage"
)
```

### Add Support for New API Provider
```python
# in agent.py: _init_llm_client()
elif self.provider == "new_provider" and self.api_key:
    from new_sdk import NewClient
    self.client = NewClient(api_key=self.api_key)
```

---

## Testing

### Quick Test
```bash
python -c "
from src.rdf_graph_loader import initialize_db
db = initialize_db('SWAPI-WD-data.ttl')
print(f'Graph loaded: {len(db.graph)} triples')
"
```

### Full Integration Test
```bash
export SWAPI_MODEL="gpt-3.5-turbo"
python main.py
# Type: "how many characters?"
# Type: "quit"
```

---

## Dependencies

```python
rdflib==7.0.0              # RDF graph management
openai==1.3.0              # OpenAI API client
python-dotenv==1.0.0       # Environment variable loading
langchain==0.1.0           # Optional: LLM orchestration
langchain-openai==0.0.6    # Optional: OpenAI integration
```

Install with:
```bash
pip install -r requirements.txt
```

---

## File Sizes & Line Counts

```
src/rdf_graph_loader.py    ~178 lines    Core RDF operations
src/agent.py               ~296 lines    Query generation
src/chat_interface.py      ~329 lines    User interface
src/query_builder.py       ~234 lines    SPARQL templates
src/examples.py            ~150 lines    Usage examples
SWAPI-WD-data.ttl          ~1000 lines   RDF data (68,981 triples)
```

---

## Documentation Map

```
Start Here:
  ├─ README.md              (Full overview)
  ├─ QUICKSTART.md          (5-min setup)
  └─ This file              (Quick reference)

Deep Dives:
  ├─ ARCHITECTURE_EXPLAINED.md (How it works)
  ├─ ARCHITECTURE_DIAGRAMS.md  (Visual flows)
  ├─ API_REFERENCE.md          (API docs)
  └─ GETTING_STARTED.md        (Detailed guide)

Specific Topics:
  ├─ MOONSHOTAI_SETUP.md       (Moonshotai setup)
  ├─ META_QUESTIONS_IMPROVEMENT.md (System features)
  └─ MOONSHOTAI_INTEGRATION.md     (Integration)
```

---

## Summary

✅ **What it is**: Natural language query engine for Star Wars RDF data  
✅ **How it works**: LLM converts English to SPARQL → Queries graph  
✅ **Where to start**: `python main.py`  
✅ **Key files**: `main.py`, `src/` folder, `SWAPI-WD-data.ttl`  
✅ **API support**: OpenAI and Moonshotai (auto-detected)  
✅ **Fallback**: Pattern matching if no API key  

**Ready to explore the Star Wars universe!** 🌟
