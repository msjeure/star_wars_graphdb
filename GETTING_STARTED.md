# Getting Started - Star Wars GraphDB Agent

## 🎯 What You're Building

A conversational AI system that lets you ask natural language questions about the Star Wars universe and get answers powered by:
1. **RDF Graph Database** - Structured Star Wars data (11,914 triples)
2. **AI Agent** - GPT-4 converts your questions to SPARQL
3. **Interactive Chat** - User-friendly interface

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies
```bash
cd /Users/mashijia/Desktop/star_wars_graphdb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Run (without OpenAI API - Pattern-Based)
```bash
python main.py
```

Try these questions:
```
How many characters are there?
Who is Luke Skywalker?
List all droid characters
```

### Step 3: Run (with OpenAI API - Better Results)
```bash
export OPENAI_API_KEY="sk-your-key-here"
python main.py
```

Now you can ask more complex questions!

---

## 📚 Complete Question Examples

### Character Queries

**Simple lookups:**
```
"Who is Yoda?"
"Tell me about Darth Vader"
"What is C-3PO?"
```

**Properties and attributes:**
```
"How tall is Luke Skywalker?"
"What color eyes does Leia have?"
"When was Han Solo born?"
"What is Chewbacca's species?"
```

**Lists and filters:**
```
"List all characters from Tatooine"
"Show me all female characters"
"Who are the tallest characters?"
"Name all Jedi in the database"
```

### Statistics & Analytics

**Counts:**
```
"How many characters are in the database?"
"How many planets are there?"
"Count all droid characters"
"How many vehicles exist?"
```

**Averages and comparisons:**
```
"What is the average height of humans?"
"Who is taller, Luke or Yoda?"
"Which species has the most characters?"
"What's the heaviest character?"
```

**Grouping and analysis:**
```
"How many characters per species?"
"Which characters appear in the most films?"
"List all characters and their homeworlds"
```

### Relationship Queries

**Two-entity relationships:**
```
"What is Luke's homeworld?"
"Which characters are from Coruscant?"
"What vehicles appear in Episode IV?"
"Show me characters with same homeworld as Luke"
```

**Complex relationships:**
```
"Which characters share a homeworld with Leia?"
"Show all characters, their species, and homeworlds"
"List films and all characters in each film"
```

### Film Queries

```
"Which characters appeared in A New Hope?"
"Who was in Episode V?"
"List characters from the original trilogy"
"Show me all characters in the prequels"
```

---

## 🔧 Using Different Interfaces

### 1. Interactive Chat (main.py)

```bash
python main.py
```

**Features:**
- Natural language questions
- Live query generation
- Conversation history
- Built-in help system

**Commands in chat:**
```
? > help                  # Show all commands
? > stats                 # Graph statistics
? > schema                # View entity types
? > query [SPARQL]        # Run raw SPARQL
? > history               # See past questions
? > clear                 # Reset conversation
? > quit                  # Exit
```

### 2. Jupyter Notebook (notebooks/demo.ipynb)

```bash
jupyter notebook notebooks/demo.ipynb
```

Great for:
- Learning the system
- Experimenting with queries
- Detailed analysis
- Saving notebooks

### 3. Python API (Programmatic)

```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

# Initialize
db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db)

# Ask questions
sparql_query, results = agent.query("Who is Luke Skywalker?")

# Process results
for result in results:
    print(result)

# View history
print(agent.get_conversation_history())
```

### 4. Run Examples (src/examples.py)

```bash
python -m src.examples
```

Shows:
- Basic RDF queries
- SPARQL examples
- Agent usage
- Schema exploration

---

## 💡 Understanding How It Works

### Example: "How many droids are there?"

**Step 1: User Input**
```
"How many droids are there?"
```

**Step 2: Agent Processes**
- Reads your question
- Extracts key concepts: "count", "droids"
- Checks if "Droid" is a known entity type ✓
- Prepares SPARQL generation

**Step 3: SPARQL Generation**
- Uses GPT-4 (if API available) or pattern matching
- Generates:
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?droid) as ?count) WHERE {
    ?droid a voc:Droid .
}
```

**Step 4: Execute Query**
- RDFlib executes the SPARQL
- Searches the RDF graph
- Finds all entities with type `voc:Droid`
- Returns count: 10

**Step 5: Display Results**
```
✅ Found 1 result(s):
{'count': 10}
```

### Example: "What is Luke's homeworld?"

**Generated SPARQL:**
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?charLabel ?worldLabel WHERE {
    ?char rdfs:label ?charLabel ;
          voc:homeworld ?world .
    ?world rdfs:label ?worldLabel .
    FILTER(CONTAINS(LCASE(str(?charLabel)), "luke"))
}
```

**Results:**
```
✅ Found 1 result(s):
{'charLabel': 'Luke Skywalker', 'worldLabel': 'Tatooine'}
```

---

## 🎓 Learning SPARQL Through Examples

### Basic Pattern 1: Find by Label
```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity WHERE {
    ?entity rdfs:label "Luke Skywalker" .
}
```

### Basic Pattern 2: Find by Type
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>

SELECT ?character WHERE {
    ?character a voc:Character .
}
LIMIT 10
```

### Basic Pattern 3: Get Properties
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?property ?value WHERE {
    ?char rdfs:label "Luke Skywalker" ;
          ?property ?value .
}
```

### Basic Pattern 4: Filter Results
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>

SELECT ?character ?height WHERE {
    ?character voc:height ?height .
    FILTER(?height > 180)
}
```

### Basic Pattern 5: Aggregate (COUNT)
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>

SELECT (COUNT(?character) as ?count) WHERE {
    ?character a voc:Character .
}
```

### Basic Pattern 6: Navigate Relationships
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?characterLabel ?planetLabel WHERE {
    ?character rdfs:label ?characterLabel ;
               voc:homeworld ?planet .
    ?planet rdfs:label ?planetLabel .
}
```

### Advanced Pattern 7: Multiple Filters
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?characterLabel WHERE {
    ?character rdfs:label ?characterLabel ;
               voc:homeworld ?homeworld ;
               voc:film ?film .
    ?homeworld rdfs:label "Tatooine" .
    ?film rdfs:label "A New Hope" .
}
```

---

## 📊 Query Testing Workflow

### Step 1: Check Schema
```
? > schema
```
See what entity types and properties are available

### Step 2: Test Simple Query
```
? > query PREFIX voc: <https://swapi.co/vocabulary/> SELECT (COUNT(?x) as ?count) WHERE { ?x a voc:Character . }
```

### Step 3: Use Agent
```
? > How many characters are there?
```
Agent generates and executes query automatically

### Step 4: Review Generated Query
The system shows you the SPARQL it generated!

### Step 5: Check History
```
? > history
```
See what queries were generated for your questions

---

## 🐛 Troubleshooting

### Issue: "No OpenAI API key found"
**Solution:** Either:
1. Set the key: `export OPENAI_API_KEY="sk-..."`
2. Or use pattern-based queries (system falls back automatically)

### Issue: "Query returns no results"
**Try:**
1. Check the schema: `schema` command
2. Try a simple count: `How many characters are there?`
3. Check exact spelling of names
4. Try `query` command with raw SPARQL

### Issue: "Query takes too long"
**Try:**
1. Reduce LIMIT in SPARQL queries
2. Use more specific filters
3. Break into smaller queries

### Issue: "Module not found error"
**Fix:**
```bash
# Make sure you're in the right directory
cd /Users/mashijia/Desktop/star_wars_graphdb

# And activated venv
source venv/bin/activate

# Check installation
pip list | grep rdflib
```

---

## 🚀 Advanced Usage

### Custom Query Builder

```python
from src.query_builder import SPARQLQueryBuilder

builder = SPARQLQueryBuilder()

# See available templates
templates = builder.get_template_info()
for t in templates:
    print(f"{t['name']}: {t['example']}")

# Build specific queries
query = builder.build_find_by_name("Yoda")
query = builder.build_count_query("Character")
query = builder.build_homeworld_query("Luke")
```

### Direct Graph Operations

```python
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")

# Find by name
results = db.find_by_label("Luke")
for entity, label in results:
    print(f"{entity}: {label}")

# Get entity properties
entity_uri = "https://swapi.co/resource/character/5"
props = db.get_entity_properties(entity_uri)
print(props)

# Get graph stats
stats = db.get_graph_stats()
print(f"Total entities: {stats['total_entities']}")
```

### Multi-turn Conversation

```python
from src.agent import StarWarsGraphAgent
from src.rdf_graph_loader import initialize_db

db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(db)

# Question 1
q1, r1 = agent.query("Who is Luke Skywalker?")
print("Luke info:", r1)

# Question 2 (agent remembers context!)
q2, r2 = agent.query("What's his homeworld?")
print("Luke's homeworld:", r2)

# See conversation flow
history = agent.get_conversation_history()
for msg in history:
    print(f"{msg['role']}: {msg['content'][:50]}...")
```

---

## 📋 Common Query Patterns

### By File
- **Count by Type**: How many [type] are there?
- **Find by Name**: Who is [name]?
- **Find by Property**: Characters from [planet]?
- **Statistics**: Average [property] of [type]?
- **Relationships**: Show [entity1]'s [relationship]?

### By Category

**Characters:**
- "Who is [name]?"
- "List all [species] characters"
- "Characters from [planet]"
- "How many [gender] characters?"

**Planets:**
- "What is [planet] like?"
- "Characters from [planet]"
- "How many planets?"

**Films:**
- "Who appeared in [film]?"
- "Characters in [film]"
- "How many films?"

**Statistics:**
- "Average height of [type]"
- "Count of [type]"
- "Tallest/shortest character"

---

## 🎯 Success Criteria

You'll know it's working when:

✅ System starts and loads the graph (shows statistics)  
✅ Simple count query works: "How many characters?"  
✅ Chat interface accepts commands: `help`, `stats`, `schema`  
✅ Natural language questions generate SPARQL  
✅ SPARQL queries return results  
✅ Conversation history is maintained  
✅ Error handling works gracefully  

---

## 📚 Next Steps

1. **Explore Data**
   - Start chat
   - Type `schema` to see what's available
   - Try example questions

2. **Learn SPARQL**
   - Use `query` command to test SPARQL
   - Modify queries to understand patterns
   - Check architecture docs for query examples

3. **Integrate into Your App**
   - Use the Python API from `src/` modules
   - Build custom interfaces (web, mobile, etc.)
   - Add caching and optimization

4. **Extend Functionality**
   - Add more query templates
   - Integrate additional LLMs
   - Build web interface
   - Add visualization

---

## 🔗 Resources

- **Quick Start**: QUICKSTART.md
- **Full README**: README.md
- **Architecture**: ARCHITECTURE.md
- **Examples**: src/examples.py
- **Notebook**: notebooks/demo.ipynb

---

**Ready to explore the Star Wars universe? Type `python main.py` and start asking! 🚀**
