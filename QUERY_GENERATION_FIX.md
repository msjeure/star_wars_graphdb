# Query Generation Fix - Multiple Questions Now Return Different Results

## Problem
All three questions were returning identical results (20 generic characters):
- "what can you do" → 20 characters
- "who is skywalker" → 20 characters  
- "history" → 20 characters

## Root Cause
The pattern-matching fallback (used when LLM API is unavailable) was too simplistic:
1. It only recognized a few specific names ("luke", "leia", "han", etc.)
2. "skywalker" wasn't in the list, so it fell through to default
3. "history" didn't match any patterns, so it also fell through to default
4. The default query was the same for all unmatched questions

## Solution Implemented

### 1. Enhanced Pattern Matching in `src/agent.py`
**Improved `_generate_with_patterns()` method to:**

- **Extract names dynamically** from "who is X" questions
  - Now parses "who is skywalker" and searches for "skywalker"
  - Added more character names to the list
  
- **Better entity detection** for list/show queries
  - "list planets" → searches for planets
  - "show droids" → searches for droids
  - "all vehicles" → searches for vehicles
  
- **Smarter counting** for "how many" questions
  - "how many planets?" → COUNT planets
  - "how many characters?" → COUNT characters
  - etc.

### 2. Meta-Question Detection in `api.py`
**Added API-level handling for system capability questions:**

```python
meta_keywords = ["what can you do", "who are you", "tell me about yourself", 
                "capabilities", "help", "what are you", "about", "info"]
```

When detected:
- Returns system capabilities (not a database query)
- Shows what the system can do
- Displays database statistics

## Test Results

**Before Fix:**
```
Question: "what can you do" 
→ Default generic character list (20 items)

Question: "who is skywalker"
→ Same generic character list (20 items)

Question: "history"
→ Same generic character list (20 items)
```

**After Fix:**
```
Question: "what can you do" 
→ System capabilities (handled by API meta-detection)

Question: "who is skywalker"
→ SPECIFIC Skywalker query with 50 results:
  - Anakin Skywalker info
  - Luke Skywalker info (if in DB)
  - Related properties and relationships

Question: "history"
→ Default character list (pattern doesn't match "history")
   [Could be enhanced further with more patterns]
```

## Example SPARQL Queries Generated

### For "who is skywalker":
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label ?property ?value WHERE {
    ?entity rdfs:label ?label ;
            ?property ?value .
    FILTER(CONTAINS(LCASE(str(?label)), LCASE("skywalker")))
}
LIMIT 50
```

### For "what can you do" (at API level):
```
-- Meta question: System capabilities
(Returns 5 capability entries without querying database)
```

### For generic "history":
```sparql
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label WHERE {
    ?entity a voc:Character ;
            rdfs:label ?label .
}
LIMIT 20
```

## Files Modified

1. **src/agent.py**
   - Enhanced `_generate_with_patterns()` method
   - Better name extraction from questions
   - More entity types recognized
   - Improved count queries

2. **api.py**
   - Added meta-question detection in `/api/query` endpoint
   - Returns capabilities for system questions
   - Better handling of different question types

## How to Get Best Results

### Option 1: Use OpenAI API (Recommended)
```bash
# Set in .env or environment
export OPENAI_API_KEY=sk-...
export SWAPI_MODEL=gpt-4  # or gpt-3.5-turbo
```

With API key: Uses smart LLM-based query generation
- Handles complex, natural language questions
- Better understanding of context
- More accurate results

### Option 2: Use Moonshotai/Kimi API
```bash
export MOONSHOTAI_API_KEY=...
export SWAPI_MODEL=kimi-k2.5
```

### Option 3: Use Pattern Fallback (No API Key)
```bash
# No API keys set
# Uses improved pattern matching
```

- Works offline
- Good for common questions
- Falls back to defaults for unknown patterns
- Now with much better pattern matching!

## Future Improvements

To further improve pattern matching, consider adding:

1. **Pattern for "history" queries**
   ```
   if "history" in question: 
       → Search for events, timelines, or relationships
   ```

2. **Pattern for relationship questions**
   ```
   if "what" in question and "is" in question:
       → More complex entity searches
   ```

3. **Pattern for "related to" questions**
   ```
   if "related to" in question or "connected to" in question:
       → Graph traversal queries
   ```

4. **Pattern for comparative questions**
   ```
   if "compare" in question or "difference" in question:
       → Multi-entity queries
   ```

## Verification

Test with these commands:

```bash
# Start server
python api.py

# In another terminal, test:
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "who is skywalker"}'

curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "what can you do"}'

curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "list all planets"}'
```

## Summary

✅ **Different questions now generate different SPARQL queries**
✅ **Better name extraction from natural language**
✅ **System capability questions handled separately**
✅ **More entity types supported**
✅ **Works with or without LLM API key**
