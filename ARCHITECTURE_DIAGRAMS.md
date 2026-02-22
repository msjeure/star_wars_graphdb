# System Architecture - Visual Diagrams 🎯

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│                  (ChatInterface)                            │
│  - Interactive CLI chat                                    │
│  - Command processing                                      │
│  - Meta-question detection                                 │
│  - Results formatting                                      │
└────────────────────────┬────────────────────────────────────┘
                         │ (user_input)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  INTELLIGENCE LAYER                         │
│              (StarWarsGraphAgent)                           │
│  - LLM Provider Detection (OpenAI/Moonshotai)              │
│  - System Prompt Generation                                │
│  - Natural Language → SPARQL Conversion                    │
│  - Error Recovery & Query Refinement                       │
│  - Conversation History Management                         │
└────────────────────────┬────────────────────────────────────┘
                         │ (sparql_query)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA ACCESS LAYER                         │
│              (SWAPIGraphDB + QueryBuilder)                  │
│  - RDF Graph Management                                    │
│  - SPARQL Template Engine                                  │
│  - Schema Extraction                                       │
│  - Query Execution                                         │
│  - Result Conversion                                       │
└────────────────────────┬────────────────────────────────────┘
                         │ (sparql_results)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  STORAGE LAYER                              │
│              (RDF Knowledge Graph)                          │
│  - 68,981 RDF Triples                                      │
│  - 1,388 Entities                                          │
│  - 51 Entity Types                                         │
│  - Star Wars Universe Data                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Complete User Query Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ USER TYPES: "Who is Luke Skywalker?"                             │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────────────────────────┐
│ ChatInterface.run()                                              │
│  1. Get user input                                              │
│  2. Check if meta-question? → No                               │
│  3. Check if special command? → No                             │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────────────────────────┐
│ StarWarsGraphAgent.query(question)                              │
│  1. Get graph schema                                            │
│  2. Build system prompt with schema info                        │
│  3. Send to LLM API                                             │
└──────────────┬───────────────────────────────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ↓             ↓
    ┌────────┐   ┌─────────────┐
    │ OpenAI │   │ Moonshotai  │
    │ API    │   │ API         │
    └───┬────┘   └──────┬──────┘
        │               │
        └───────┬───────┘
                ↓
     ┌─────────────────────────┐
     │ LLM Response (SPARQL)   │
     │ ```sparql               │
     │ SELECT ?label ?property │
     │ WHERE {...}             │
     │ ```                     │
     └────────┬────────────────┘
              │
              ↓
     ┌─────────────────────────┐
     │ Parse SPARQL from       │
     │ LLM response            │
     └────────┬────────────────┘
              │
              ↓
     ┌─────────────────────────┐
     │ SWAPIGraphDB.           │
     │ execute_sparql(query)   │
     └────────┬────────────────┘
              │
              ↓
     ┌─────────────────────────┐
     │ RDFlib executes query   │
     │ against RDF graph       │
     │ (68,981 triples)        │
     └────────┬────────────────┘
              │
              ↓
     ┌─────────────────────────┐
     │ Convert results to      │
     │ dictionaries            │
     │ [{label: 'Luke', ...}]  │
     └────────┬────────────────┘
              │
              ↓
┌──────────────────────────────────────────────────────────────────┐
│ ChatInterface._format_results(results)                           │
│  Format and display results nicely                              │
└──────────────┬───────────────────────────────────────────────────┘
               │
               ↓
     ┌─────────────────────────┐
     │ USER SEES:              │
     │ Found 1 result:         │
     │ Luke Skywalker          │
     │ - Height: 172cm         │
     │ - Mass: 77kg            │
     │ - Species: Human        │
     └─────────────────────────┘
```

---

## LLM Provider Detection Flow

```
┌─────────────────────────────────────┐
│ User specifies model via env var    │
│ export SWAPI_MODEL="kimi-k2.5"      │
└──────────────┬──────────────────────┘
               │
               ↓
     ┌─────────────────────────┐
     │ StarWarsGraphAgent      │
     │ __init__(model=...)     │
     └────────┬────────────────┘
              │
              ↓
     ┌─────────────────────────┐
     │ _init_llm_client()      │
     │ auto-detection logic    │
     └────────┬────────────────┘
              │
        ┌─────┴──────────────┐
        │                    │
        ↓                    ↓
   ┌────────────┐      ┌──────────────┐
   │startswith  │      │startswith    │
   │("kimi")?   │      │("gpt")?      │
   └─────┬──────┘      └───────┬──────┘
         │YES                  │YES
         ↓                     ↓
   ┌────────────┐      ┌──────────────┐
   │Moonshotai  │      │OpenAI        │
   │Provider    │      │Provider      │
   └─────┬──────┘      └───────┬──────┘
         │                     │
         ↓                     ↓
   ┌────────────────┐  ┌──────────────────┐
   │OpenAI Client   │  │OpenAI Client     │
   │base_url=       │  │base_url=         │
   │moonshot.cn/v1  │  │openai.com/v1     │
   │api_key=        │  │api_key=          │
   │MOONSHOTAI_KEY  │  │OPENAI_KEY        │
   └────────────────┘  └──────────────────┘
              │                │
              └────────┬───────┘
                       ↓
                ┌─────────────────┐
                │Ready to call    │
                │LLM API          │
                └─────────────────┘
                     
        │NO (None of above)
        ↓
   ┌──────────────────┐
   │Pattern Matching  │
   │(Local mode)      │
   │No API needed     │
   └──────────────────┘
```

---

## Module Dependencies

```
main.py
  │
  ├─→ ChatInterface
  │     │
  │     ├─→ SWAPIGraphDB
  │     │     ├─→ RDFlib
  │     │     └─→ SWAPI-WD-data.ttl
  │     │
  │     ├─→ StarWarsGraphAgent
  │     │     ├─→ OpenAI SDK
  │     │     ├─→ RDFlib (for querying)
  │     │     └─→ .env (config)
  │     │
  │     └─→ QueryBuilder
  │           └─→ SPARQL Templates
  │
  └─→ os, sys, logging (stdlib)
```

---

## Data Flow: Query Generation

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: COLLECT CONTEXT                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Graph Schema:                                             │
│  {                                                         │
│    "classes": ["Character", "Planet", "Vehicle", ...],    │
│    "properties": ["height", "mass", "homeworld", ...],    │
│    "sample_data": {                                        │
│      "Character": [                                        │
│        "https://swapi.co/resource/luke_skywalker",        │
│        "https://swapi.co/resource/leia_organa",          │
│      ]                                                     │
│    }                                                       │
│  }                                                         │
│                                                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: BUILD SYSTEM PROMPT                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  "You are a SPARQL query builder for Star Wars data.       │
│                                                             │
│   SCHEMA:                                                  │
│   - Classes: Character, Planet, Vehicle, ...               │
│   - Properties: height, mass, homeworld, ...               │
│   - Sample URIs: https://swapi.co/resource/luke...         │
│                                                             │
│   RULES:                                                   │
│   - Use these prefixes: voc:, swapi:, rdfs:, rdf:          │
│   - Entity types: voc:Character, voc:Planet, etc.         │
│   - Properties: voc:height, voc:mass, etc.                │
│   - Labels: rdfs:label                                     │
│                                                             │
│   TASK:                                                    │
│   Convert natural language to valid SPARQL."              │
│                                                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: SEND TO LLM                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  client.chat.completions.create(                          │
│    model="gpt-4",                  # or "kimi-k2.5"       │
│    messages=[                                              │
│      {"role": "system", "content": system_prompt},         │
│      {"role": "user", "content": "Who is Luke?"}          │
│    ],                                                      │
│    temperature=0.2,  # Low for deterministic queries      │
│    max_tokens=1000                                         │
│  )                                                         │
│                                                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: PARSE RESPONSE                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Response from LLM:                                        │
│  "To find Luke Skywalker, I'll search for characters      │
│   with 'Luke' in their label.                             │
│                                                             │
│   ```sparql                                               │
│   PREFIX voc: <https://swapi.co/vocabulary/>              │
│   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>   │
│                                                             │
│   SELECT ?entity ?label WHERE {                           │
│     ?entity a voc:Character ;                             │
│              rdfs:label ?label .                          │
│     FILTER(CONTAINS(LCASE(str(?label)), "luke"))         │
│   }                                                        │
│   ```"                                                     │
│                                                             │
│  Extract between ```sparql and ```                        │
│                                                             │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: EXECUTE QUERY                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  db.execute_sparql(sparql_query)                          │
│    → Call RDFlib.query()                                  │
│    → Get results from RDF graph                           │
│    → Convert to dictionary format                         │
│    → Return to user interface                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Handling Flow

```
                    Query Execution
                          │
                          ↓
                   ┌─────────────┐
                   │Query fails? │
                   └──────┬──────┘
                          │
                    ┌─────┴─────┐
                    │YES        │NO
                    ↓           ↓
         ┌──────────────────┐ Success!
         │Log error message │ Return results
         └────────┬─────────┘
                  │
                  ↓
         ┌──────────────────────────┐
         │_refine_query_on_error()  │
         │                          │
         │Send to LLM:              │
         │- Original question       │
         │- Failed query            │
         │- Error message           │
         │                          │
         │Ask to fix and regenerate │
         └────────┬─────────────────┘
                  │
                  ↓
         ┌──────────────────┐
         │Try new query     │
         └────────┬─────────┘
                  │
            ┌─────┴─────┐
            │YES   │NO  │
            ↓      ↓    
        Success  Return
        Return   empty
        results  results
```

---

## File I/O & Configuration

```
┌─────────────────────────────────────┐
│ Application Startup                 │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
        ↓             ↓
   ┌─────────┐   ┌──────────────┐
   │Load     │   │Load          │
   │.env     │   │RDF Data      │
   │file     │   │(TTL)         │
   └────┬────┘   └────┬─────────┘
        │             │
        ↓             ↓
   ┌─────────┐   ┌──────────────┐
   │Environment  │Parse triples │
   │Variables    │(68,981)      │
   │API keys,    │Create        │
   │model,       │RDFlib graph  │
   │log level    └─────┬────────┘
   └────┬────────────┬──┘
        │            │
        └─────┬──────┘
              │
              ↓
    ┌─────────────────────┐
    │Ready for queries    │
    └─────────────────────┘
```

---

## Performance Timeline

```
User Types Question (t=0)
              │
              ↓ (t=0-100ms)
     Chat Interface Processing
              │
              ├─→ Meta-question check
              ├─→ Command check
              └─→ Route to agent
              │
              ↓ (t=100-500ms, if pattern matching)
     Agent: Generate SPARQL (Pattern)
              │
              ↓ (t=100-3000ms, if LLM)
     Agent: Get LLM response
     Agent: Parse response
              │
              ↓ (t=3000-3100ms)
     Graph: Execute SPARQL
              │
              ↓ (t=3100-3200ms)
     Format results
              │
              ↓ (t=3200ms)
    User sees results

TOTAL TIME:
- With LLM: ~3-5 seconds
- With Pattern: ~200-500ms
```

---

## Query Builder Template Selection

```
User Question: "List all Jedi"
              │
              ↓
    Check against patterns:
    ├─ "all X" → Use "characters_by_type"
    │
    ├─ Template parameters:
    │  └─ entity_type = "Jedi"
    │
    ├─ Apply template:
    │  └─ SELECT ?character WHERE {
    │       ?character a voc:Jedi;
    │       rdfs:label ?label.
    │     }
    │
    └─→ Execute
```

---

## Summary

**Architecture Characteristics:**
- ✅ **Layered**: UI → Logic → Data → Storage
- ✅ **Modular**: Clear separation of concerns
- ✅ **Extensible**: Easy to add providers, commands, templates
- ✅ **Resilient**: Fallback mechanisms at each layer
- ✅ **Type-safe**: Full type hints throughout
- ✅ **Well-documented**: System prompts and logging

**Key Flows:**
1. User Question → Chat Interface
2. Chat Interface → Agent (LLM or Pattern)
3. Agent → SPARQL Query
4. SPARQL Query → Graph Database
5. Results → Formatted Output

This architecture enables easy querying of the Star Wars RDF knowledge graph using natural language! 🌟
