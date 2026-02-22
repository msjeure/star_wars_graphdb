# Star Wars GraphDB - Architecture & Workflow Guide 🚀

## Overview

This is a **Natural Language Query System** for exploring the Star Wars universe using RDF (Resource Description Framework) data. Users can ask questions in plain English, and the system converts them to SPARQL queries to search the knowledge graph.

```
User Question (English)
    ↓
Natural Language to SPARQL Conversion (LLM)
    ↓
SPARQL Query
    ↓
RDF Graph Database (68,981 triples)
    ↓
Results
    ↓
Formatted Response to User
```

---

## Repository Structure

```
star_wars_graphdb/
├── main.py                          # Entry point
├── SWAPI-WD-data.ttl               # RDF data (68,981 triples)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
│
├── src/                            # Core system modules
│   ├── __init__.py
│   ├── rdf_graph_loader.py        # RDF database management
│   ├── agent.py                    # LLM-based query conversion
│   ├── query_builder.py            # SPARQL template engine
│   ├── chat_interface.py           # Interactive CLI interface
│   └── examples.py                 # API usage examples
│
├── notebooks/                      # Jupyter notebooks
│   └── demo.ipynb                  # Interactive demonstration
│
└── Documentation/
    ├── README.md                   # Full documentation
    ├── QUICKSTART.md               # 5-minute setup guide
    ├── MOONSHOTAI_SETUP.md         # Moonshotai API setup
    ├── ARCHITECTURE.md             # System design details
    ├── API_REFERENCE.md            # API documentation
    ├── META_QUESTIONS_IMPROVEMENT.md # Meta-question handling
    └── ... other guides
```

---

## Core Modules

### 1. **rdf_graph_loader.py** - Data Layer
**Purpose**: Manages the RDF knowledge graph

**Key Class**: `SWAPIGraphDB`

```python
# Initialize database
db = SWAPIGraphDB("SWAPI-WD-data.ttl")

# Core Methods:
db.execute_sparql(query)          # Execute SPARQL query
db.get_graph_schema()             # Get data structure info
db.find_by_label(name)            # Search by entity label
db.get_entity_properties(uri)     # Get all properties of entity
db.get_graph_stats()              # Get statistics
```

**What It Does**:
- Loads RDF data from TTL file (Turtle format)
- Provides SPARQL query interface
- Manages RDF namespaces and prefixes
- Returns results as Python dictionaries

**Data Format**:
- 68,981 RDF triples
- 1,388 entities total
- 51 entity types (Character, Planet, Starship, etc.)
- Properties extracted from the knowledge graph

---

### 2. **query_builder.py** - Template Engine
**Purpose**: Provides SPARQL query templates

**Key Class**: `SPARQLQueryBuilder`

```python
# Access pre-built templates
templates = SPARQLQueryBuilder.TEMPLATES

# Available templates:
- find_by_name              # Search by entity name
- character_properties      # Get properties of character
- characters_by_type        # Filter by species/type
- characters_by_film        # Filter by film appearance
- character_relationships   # Find character connections
- count_by_type            # Count entities of type
- average_property         # Calculate averages
```

**Example Template**:
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?character ?label WHERE {
    ?character a voc:Character ;
               rdfs:label ?label .
}
LIMIT 20
```

---

### 3. **agent.py** - Intelligence Layer
**Purpose**: Converts natural language to SPARQL queries using LLM

**Key Class**: `StarWarsGraphAgent`

```python
# Initialize agent
agent = StarWarsGraphAgent(graph_db, model="gpt-4")

# Core Method:
sparql_query, results = agent.query("Who is Luke Skywalker?")
```

**How It Works**:

1. **LLM Client Initialization** (`_init_llm_client`)
   - Detects API provider (OpenAI, Moonshotai)
   - Falls back to pattern-matching if no API key
   - Three provider levels:
     ```python
     if model.startswith("kimi"):
         use Moonshotai at api.moonshot.cn/v1
     elif model.startswith("gpt"):
         use OpenAI at api.openai.com/v1
     else:
         use pattern-matching (local)
     ```

2. **Query Generation** (`_generate_sparql_query`)
   - Sends user question + graph schema to LLM
   - LLM returns SPARQL query
   - Falls back to pattern matching if LLM fails

3. **Query Execution**
   - Executes SPARQL against RDF graph
   - Returns structured results
   - Handles errors and refinement

**System Prompt Structure**:
```
You are a SPARQL query builder for Star Wars RDF data.
Here is the schema:
- Classes: Character, Planet, Vehicle, etc.
- Properties: height, mass, homeworld, etc.
- Sample data for each class

Convert natural language questions to valid SPARQL queries.
```

---

### 4. **chat_interface.py** - User Interaction
**Purpose**: Interactive CLI for conversational queries

**Key Class**: `ChatInterface`

```python
# Initialize and run
chat = ChatInterface("SWAPI-WD-data.ttl", model="gpt-4")
chat.run()
```

**Key Features**:

1. **Welcome Screen**: Shows graph statistics and capabilities

2. **Meta-Question Detection** (`_is_meta_question`)
   ```python
   # Detects questions about system, not data:
   "what can you do?"        → Show capabilities
   "who are you?"            → Show capabilities
   "How many characters?"    → Regular data query
   ```

3. **Special Commands**:
   - `help` - Show help message
   - `stats` - Show graph statistics
   - `schema` - Show data structure
   - `history` - Show conversation history
   - `clear` - Clear history
   - `query <sparql>` - Execute raw SPARQL
   - `quit`/`exit` - Exit program

4. **Main Loop**:
   ```
   User Input
   ↓
   Check if meta-question → Show capabilities
   ↓
   Check if special command → Execute command
   ↓
   Send to agent for SPARQL conversion
   ↓
   Execute SPARQL query
   ↓
   Format and display results
   ```

---

## Data Flow: Complete User Query

### Step 1: User Input
```
You: "Who is Luke Skywalker?"
```

### Step 2: Input Processing
```python
# In ChatInterface.run()
# Check if it's a meta-question
meta = self._is_meta_question(user_input)
# → None (it's a data query)

# Check if it's a special command
# → Not a command, continue
```

### Step 3: Query Generation
```python
# In StarWarsGraphAgent.query()
# Prepare system prompt with schema
system_prompt = self.get_system_prompt()
# Shows: classes, properties, sample data, rules

# Send to LLM
response = client.chat.completions.create(
    model="gpt-4" or "kimi-k2.5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Who is Luke Skywalker?"}
    ],
    temperature=0.2,  # Low temp for deterministic results
)
```

### Step 4: SPARQL Query Generation
```
LLM Response:
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label ?property ?value WHERE {
    ?entity rdfs:label ?label ;
            ?property ?value .
    FILTER(CONTAINS(LCASE(str(?label)), LCASE("luke")))
}
LIMIT 50
```
```

### Step 5: Query Execution
```python
# In SWAPIGraphDB.execute_sparql()
results = self.graph.query(sparql_query)

# Convert RDFlib results to dictionaries
for row in results:
    for var in results.vars:
        row_dict[str(var)] = str(row[var])
```

### Step 6: Results Formatting
```python
# In ChatInterface._format_results()
# Display formatted results with nice table/list formatting
```

### Step 7: User Sees
```
Found 5 results:
- Luke Skywalker: height=172cm, mass=77kg, ...
```

---

## API Provider System

### Three-Tier Provider Detection

```
┌─────────────────────┐
│  User Input         │
│  model = "kimi-k2.5"│
└──────────┬──────────┘
           ↓
    ┌─────────────────┐
    │ Auto-Detection  │
    │ .startswith()   │
    └─────────┬───────┘
              ↓
    ┌─────────────────────────────────┐
    │ if "kimi" → moonshotai          │
    │ elif "gpt" → openai             │
    │ else → local (pattern matching) │
    └─────────────────────────────────┘
              ↓
    ┌──────────────────────────────────────┐
    │ Initialize appropriate client       │
    │ Moonshotai: base_url=moonshot.cn/v1 │
    │ OpenAI: base_url=openai.com/v1      │
    │ Local: Pattern matching only        │
    └──────────────────────────────────────┘
```

### Environment Variables
```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."
export SWAPI_MODEL="gpt-4"

# For Moonshotai
export MOONSHOTAI_API_KEY="your-key"
export SWAPI_MODEL="kimi-k2.5"

# Model auto-detection
python main.py  # Will use SWAPI_MODEL env var
```

---

## Key Design Patterns

### 1. **Layered Architecture**
```
ChatInterface (UI)
    ↓
StarWarsGraphAgent (Logic)
    ↓
SWAPIGraphDB (Data)
    ↓
RDF Graph (Storage)
```

### 2. **Fallback Strategy**
```python
# If LLM API fails
if api_available:
    use_llm_for_query_generation()
else:
    use_pattern_matching_templates()
```

### 3. **Separation of Concerns**
- **rdf_graph_loader.py**: Only database operations
- **agent.py**: Only query generation
- **query_builder.py**: Only SPARQL templates
- **chat_interface.py**: Only user interaction

### 4. **Error Handling**
```python
try:
    # Execute SPARQL
    results = db.execute_sparql(query)
except Exception as e:
    # Try to refine query
    refined = agent._refine_query_on_error(question, query, error)
    # If still fails, return empty results
```

---

## Query Execution Pipeline

### Pattern 1: LLM-Based Query (With API)
```
User Question
    ↓
Load graph schema from database
    ↓
Create system prompt
    ↓
Call LLM API (OpenAI/Moonshotai)
    ↓
Parse SPARQL from response
    ↓
Execute against RDF graph
    ↓
Return results
```

### Pattern 2: Pattern-Based Query (Fallback)
```
User Question
    ↓
Analyze question for keywords
    ↓
Match against templates
    ↓
Use template to generate SPARQL
    ↓
Execute against RDF graph
    ↓
Return results
```

---

## Configuration

### Environment Files

**`.env.example`**:
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Moonshotai Configuration
MOONSHOTAI_API_KEY=your-key

# Model Selection
SWAPI_MODEL=gpt-4          # or kimi-k2.5

# Logging
LOG_LEVEL=INFO
```

### Model Configuration
```python
# main.py reads from environment
model = os.getenv("SWAPI_MODEL", "gpt-4")

# Supported models:
- gpt-4              (OpenAI)
- gpt-3.5-turbo      (OpenAI)
- kimi-k2.5          (Moonshotai)
- local              (Pattern matching)
```

---

## Data Statistics

```
Total Data Points:
├── Triples: 68,981
├── Entities: 1,388
└── Relations: 65

Entity Types (51 total):
├── FilmRole: 345
├── Person: 249
├── Character: 87
├── Planet: 61
├── Starship: 37
├── Species: 38
└── ... and 45 more types
```

---

## Extension Points

### 1. Add New Templates
```python
# In query_builder.py
TEMPLATES["new_pattern"] = QueryTemplate(
    name="new_pattern",
    template="...",
    example="..."
)
```

### 2. Add New Commands
```python
# In chat_interface.py
elif user_input.lower() == "newcommand":
    self._handle_new_command()
    continue
```

### 3. Add New Meta-Questions
```python
# In chat_interface.py _is_meta_question()
meta_patterns = {
    "new question": "handler_name",
    # ...
}
```

### 4. Support New LLM Providers
```python
# In agent.py _init_llm_client()
elif self.provider == "new_provider" and self.api_key:
    self.client = NewProviderClient(api_key=self.api_key)
```

---

## Testing & Validation

### Quick Test
```bash
python -c "
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

db = initialize_db('SWAPI-WD-data.ttl')
agent = StarWarsGraphAgent(db, model='gpt-4')
query, results = agent.query('How many characters?')
print(f'Query: {query}')
print(f'Results: {results}')
"
```

### Full Integration Test
```bash
export SWAPI_MODEL="gpt-3.5-turbo"
python main.py
# Type: "who is luke"
# Type: "quit"
```

---

## Performance Characteristics

- **RDF Graph Load Time**: ~2-3 seconds (68,981 triples)
- **SPARQL Query Execution**: <100ms (typical)
- **LLM API Call**: 1-3 seconds
- **Total Response Time**: 2-5 seconds (LLM) or <500ms (pattern matching)

---

## Security Considerations

1. **API Keys**
   - Store in `.env` file (not in code)
   - Never commit `OPENAI_API_KEY` or `MOONSHOTAI_API_KEY`
   - Use environment variables for CI/CD

2. **SPARQL Injection**
   - LLM generates queries (not user input directly)
   - Queries are validated before execution
   - Templates provide safe patterns

3. **Rate Limiting**
   - OpenAI/Moonshotai handle rate limiting
   - Pattern matching provides fallback
   - No hardcoded limits in system

---

## Summary

**The system is a knowledge graph query engine that:**

1. ✅ Loads RDF data (Star Wars universe)
2. ✅ Converts English questions to SPARQL using LLM
3. ✅ Falls back to pattern matching if no API available
4. ✅ Executes queries against RDF graph
5. ✅ Displays results in user-friendly format
6. ✅ Supports OpenAI and Moonshotai APIs
7. ✅ Handles meta-questions about system capabilities
8. ✅ Provides interactive CLI interface

**Architecture: Clean, modular, extensible** 🎯
