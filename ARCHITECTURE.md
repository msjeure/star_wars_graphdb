# Star Wars GraphDB - System Architecture & Design

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION LAYER                          │
│                                                                           │
│  ┌─────────────────┐         ┌──────────────────┐                       │
│  │   Interactive   │         │   Jupyter        │                       │
│  │   CLI Chat      │◄───────►│   Notebook       │                       │
│  │ (chat_interface)│         │   (demo.ipynb)   │                       │
│  └────────┬────────┘         └──────────────────┘                       │
│           │                                                              │
└───────────┼──────────────────────────────────────────────────────────────┘
            │
            │ Natural Language Questions
            │
┌───────────▼──────────────────────────────────────────────────────────────┐
│                      AI AGENT LAYER                                       │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  StarWarsGraphAgent                                              │   │
│  │  - Understands natural language                                  │   │
│  │  - Maintains conversation history                               │   │
│  │  - Uses GPT-4/Claude for query generation                       │   │
│  │  - Falls back to pattern matching                               │   │
│  └──────────┬───────────────────────────────────────────────────────┘   │
│             │                                                             │
└─────────────┼─────────────────────────────────────────────────────────────┘
              │
              │ SPARQL Queries
              │
┌─────────────▼─────────────────────────────────────────────────────────────┐
│                    QUERY BUILDING LAYER                                    │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  SPARQLQueryBuilder                                              │    │
│  │  - Pre-built query templates                                     │    │
│  │  - Dynamic query generation                                      │    │
│  │  - Common patterns (find, count, stats)                          │    │
│  └──────────┬───────────────────────────────────────────────────────┘    │
│             │                                                             │
└─────────────┼─────────────────────────────────────────────────────────────┘
              │
              │ Validated SPARQL
              │
┌─────────────▼─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                                        │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  SWAPIGraphDB (RDFlib)                                           │    │
│  │  - Load RDF from TTL                                             │    │
│  │  - Execute SPARQL queries                                        │    │
│  │  - Schema introspection                                          │    │
│  │  - Entity lookups and analytics                                  │    │
│  └──────────┬───────────────────────────────────────────────────────┘    │
│             │                                                             │
└─────────────┼─────────────────────────────────────────────────────────────┘
              │
              │ Graph Queries
              │
┌─────────────▼─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                            │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐    │
│  │  SWAPI-WD-data.ttl                                               │    │
│  │  ✓ 11,914 RDF triples                                            │    │
│  │  ✓ 70+ Characters                                                 │    │
│  │  ✓ 60+ Planets                                                    │    │
│  │  ✓ 60+ Vehicles & Starships                                       │    │
│  │  ✓ Rich relationships and metadata                                │    │
│  └──────────────────────────────────────────────────────────────────┘    │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## 📦 Module Descriptions

### 1. **rdf_graph_loader.py** - Core RDF Management
**Purpose**: Load, manage, and query RDF data

**Key Classes**:
- `SWAPIGraphDB`: Main class for graph operations
  - `load_graph()`: Load TTL file into RDFlib graph
  - `execute_sparql(query)`: Execute SPARQL queries
  - `get_graph_schema()`: Extract schema information
  - `find_by_label(label)`: Search for entities
  - `get_entity_properties(uri)`: Get all properties of an entity
  - `get_graph_stats()`: Get graph statistics

**Usage**:
```python
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")
results = db.execute_sparql("SELECT ?x WHERE { ?x a voc:Character }")
```

---

### 2. **query_builder.py** - SPARQL Query Generation
**Purpose**: Build SPARQL queries from templates and parameters

**Key Classes**:
- `SPARQLQueryBuilder`: Template-based query builder
  - Pre-built templates for common patterns
  - `build_find_by_name(name)`: Find entities by name
  - `build_characters_by_species(species)`: Find by species
  - `build_characters_by_film(film)`: Find characters in films
  - `build_count_query(type)`: Count entities
  - `get_template_info()`: List available templates

**Available Templates**:
1. `find_by_name` - Search for entities by name
2. `characters_by_type` - Filter by species/type
3. `characters_by_film` - Filter by film appearance
4. `character_properties` - Get entity properties
5. `character_relationships` - Find relationships
6. `count_by_type` - Count entities
7. `homeworld_info` - Find character's origin
8. `species_stats` - Get species statistics

**Usage**:
```python
from src.query_builder import SPARQLQueryBuilder

builder = SPARQLQueryBuilder()
query = builder.build_find_by_name("Luke")
results = db.execute_sparql(query)
```

---

### 3. **agent.py** - AI Agent for NL→SPARQL
**Purpose**: Convert natural language to SPARQL using LLM

**Key Classes**:
- `StarWarsGraphAgent`: Main agent class
  - `query(question)`: Convert NL to SPARQL and execute
  - `get_system_prompt()`: Generate contextual system prompt
  - `get_conversation_history()`: Get chat history
  - `clear_history()`: Clear conversation
  - `_generate_with_gpt()`: Use OpenAI API
  - `_generate_with_patterns()`: Fallback pattern matching

**Features**:
- Contextual prompts with graph schema
- Error recovery and query refinement
- Conversation history tracking
- GPT-4/3.5-turbo support
- Fallback pattern-based generation

**Usage**:
```python
from src.agent import StarWarsGraphAgent

agent = StarWarsGraphAgent(db, model="gpt-4")
sparql_query, results = agent.query("Who is Luke Skywalker?")
```

---

### 4. **chat_interface.py** - Interactive CLI
**Purpose**: Provide interactive chat interface for users

**Key Classes**:
- `ChatInterface`: Main chat interface
  - `run()`: Main chat loop
  - Special commands: help, stats, schema, history, clear, query, quit
  - Pretty-printed results and formatting

**Features**:
- Welcome message with graph info
- Rich terminal output with emojis
- Command history
- Raw SPARQL execution
- Real-time feedback

**Commands**:
- `help` - Show help
- `stats` - Graph statistics
- `schema` - Schema information
- `history` - Conversation history
- `clear` - Clear history
- `query [SPARQL]` - Execute raw query
- `quit`/`exit` - Exit

---

### 5. **examples.py** - Usage Examples
**Purpose**: Demonstrate system capabilities

**Functions**:
- `example_basic_queries()` - Basic RDF operations
- `example_sparql_queries()` - SPARQL examples
- `example_agent_queries()` - NL query examples
- `example_schema_exploration()` - Schema introspection
- `example_query_builder()` - Query templates

---

## 🔄 Data Flow Examples

### Example 1: Simple Character Query

```
User Input
└─ "Who is Luke Skywalker?"
    │
    ├─ [Chat Interface] Receives question
    │
    ├─ [Agent] Generates system prompt with schema:
    │   "You are SPARQL expert. Graph has voc:Character class..."
    │
    ├─ [GPT-4 API] Receives prompt + question
    │   Returns: SELECT ?entity ?label WHERE { ... FILTER Luke ... }
    │
    ├─ [Query Builder] Validates query
    │
    ├─ [RDFlib] Executes SPARQL
    │   Queries RDF graph
    │   Returns: [{'entity': 'swapi:luke/5', 'label': 'Luke Skywalker'}]
    │
    └─ [Chat Interface] Displays results
       ✅ Found 1 result
       Generated SPARQL Query: ...
       Result: {'entity': swapi:luke/5, 'label': 'Luke Skywalker'}
```

### Example 2: Fallback Pattern Matching

```
User Input
└─ "How many droids?"
    │
    ├─ [Chat Interface] Receives question
    │
    ├─ [Agent] Attempts GPT generation
    │   ⚠️ API error or timeout
    │
    ├─ [Agent] Falls back to pattern matching
    │   Detects: "how many" + "droids"
    │   Generates: SELECT (COUNT(?droid) as ?count) WHERE {
    │              ?droid a voc:Droid . }
    │
    ├─ [RDFlib] Executes query
    │   Returns: [{'count': 10}]
    │
    └─ [Chat Interface] Displays results
       ✅ Found 1 result
       Result: {'count': 10}
```

### Example 3: Complex Multi-Step Query

```
User Input
└─ "Which characters are from Tatooine and appear in Episode IV?"
    │
    ├─ [Agent] Understands:
    │   - Character location (homeworld)
    │   - Film appearance
    │   - Filters needed
    │
    ├─ [GPT-4] Generates complex SPARQL:
    │   SELECT ?charLabel WHERE {
    │     ?char rdfs:label ?charLabel ;
    │           voc:homeworld swapi:planet/1 ;  (Tatooine)
    │           voc:film swapi:film/1 .         (A New Hope)
    │   }
    │
    ├─ [RDFlib] Executes, finds matching entities
    │   Returns: [{'charLabel': 'Luke Skywalker'}, {'charLabel': 'C-3PO'}, ...]
    │
    └─ [Chat Interface] Displays formatted results
```

## 🔗 Data Relationships

### Character Properties
```
Character (entity)
├── rdfs:label → "Luke Skywalker"
├── voc:height → 172.0
├── voc:mass → 77.0
├── voc:eyeColor → "blue"
├── voc:hairColor → "blonde"
├── voc:skinColor → "fair"
├── voc:gender → "male"
├── voc:birthYear → "19BBY"
├── voc:homeworld → Planet (reference)
│   └── → "Tatooine"
├── voc:film → [Film 4, 5, 6, ...]  (multiple)
└── voc:species → Species type
    └── → "Human"
```

### Query Pattern Examples

**1. Find with filter**
```sparql
?char rdfs:label ?label .
FILTER(CONTAINS(LCASE(str(?label)), "luke"))
```

**2. Navigate relationships**
```sparql
?char voc:homeworld ?world .
?world rdfs:label ?worldLabel .
```

**3. Aggregate operations**
```sparql
?char voc:height ?height .
FILTER(?height > 0)
(COUNT/AVG/SUM/MIN/MAX)
```

**4. Filter by type**
```sparql
?entity a voc:Character .
?entity a voc:Droid .
```

## 🎯 Design Patterns Used

### 1. **Factory Pattern**
```python
db = initialize_db("file.ttl")  # Factory function
agent = create_agent(db)         # Convenience creation
```

### 2. **Template Method Pattern**
Query builder uses templates with parameter substitution:
```python
template = "SELECT ?x WHERE { ?x a voc:{type} }"
query = template.format(type="Character")
```

### 3. **Strategy Pattern**
Agent has multiple strategies:
- GPT-4 strategy (when API available)
- Pattern matching strategy (fallback)
- Direct SPARQL strategy (user-provided)

### 4. **Decorator Pattern**
Results are formatted and decorated:
- Raw query results
- Pretty-printed output
- Conversation history tracking

### 5. **Facade Pattern**
`ChatInterface` hides complexity of underlying components:
```python
chat = ChatInterface(db_path)
chat.run()  # Everything abstracted
```

## 📊 Graph Schema Structure

### Classes (Entity Types)
- `Character` - People/sentient beings
- `Droid` - Robots/droids
- `Vehicle` - Ground/air vehicles
- `Starship` - Space vessels
- `Planet` - Celestial bodies
- `Species` - Species classifications

### Properties (Relationships)
- `rdfs:label` - Entity name
- `voc:height` - Physical height
- `voc:mass` - Physical mass
- `voc:homeworld` - Origin planet
- `voc:film` - Film appearances
- `voc:vehicle` - Vehicles used
- `voc:eyeColor`, `voc:skinColor`, `voc:hairColor` - Appearance
- `voc:gender` - Gender
- `voc:birthYear` - Birth date (BBY/ABY)

## 🚀 Deployment Considerations

### Performance
- Graph loading: ~2-5 seconds (one-time)
- Simple queries: <100ms
- Complex queries: 100ms-1s
- API calls: 1-3 seconds

### Scalability
- Current: ~12K triples - excellent performance
- RDFlib can handle millions of triples with proper indexing
- For larger graphs: Consider SPARQL endpoints (GraphDB, Virtuoso)

### Error Handling
- Missing API key → fallback to pattern matching ✓
- Invalid SPARQL → query refinement with GPT ✓
- No results → fallback query generation ✓
- Malformed input → pattern detection ✓

## 🔌 Integration Points

### 1. Custom LLM Integration
```python
# Modify agent.py to use different LLM
from langchain import LLMChain, LLMMixin

class CustomAgent(StarWarsGraphAgent):
    def _init_llm_client(self):
        # Use local Ollama, Hugging Face, etc.
        pass
```

### 2. Web API Integration
```python
# Could be wrapped in FastAPI/Flask
from fastapi import FastAPI

@app.post("/query")
def query_endpoint(question: str):
    return agent.query(question)
```

### 3. Database Connection Pooling
```python
# For multiple agents
db_pool = [initialize_db(path) for _ in range(num_workers)]
```

### 4. Caching Layer
```python
# Add Redis for common queries
@cache.cached(timeout=3600)
def query(sparql):
    return db.execute_sparql(sparql)
```

---

## 🎓 Learning Resources

### For SPARQL:
- [SPARQL Tutorial](https://www.w3.org/TR/sparql11-query/)
- [RDFlib Documentation](https://rdflib.readthedocs.io/)
- [Common Patterns](https://www.w3.org/TR/sparql11-query/#basicPatterns)

### For Graph Databases:
- [RDF Concepts](https://www.w3.org/TR/rdf11-concepts/)
- [Linked Data](https://www.w3.org/DesignIssues/LinkedData.html)

### For LLMs:
- [OpenAI API](https://platform.openai.com/docs)
- [LangChain Documentation](https://docs.langchain.com/)

---

## 📋 Checklist for Extensions

- [ ] Add web interface (Flask/FastAPI)
- [ ] Implement caching (Redis)
- [ ] Add graph visualization (Cytoscape)
- [ ] Support more LLMs (Ollama, HuggingFace)
- [ ] Add entity disambiguation
- [ ] Implement context-aware follow-ups
- [ ] Add batch query support
- [ ] Create REST API
- [ ] Add authentication/authorization
- [ ] Implement query result streaming

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Complete ✅
