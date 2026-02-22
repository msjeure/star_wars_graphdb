# Meta-Questions Improvement 🚀

## Problem
Previously, when users asked meta-questions like **"what can you do?"**, the system would try to convert them into SPARQL queries, resulting in irrelevant results about the database instead of answering about the system's capabilities.

## Solution
Added intelligent **meta-question detection** that recognizes when users are asking about the system itself (not the Star Wars data) and responds appropriately.

---

## How It Works

### 1. Meta-Question Detection
The system now recognizes these meta-questions:
- "What can you do?"
- "What can I do?"
- "Who are you?"
- "Tell me about yourself"
- "What is this?"
- "How does this work?"
- "About"
- "Capabilities"

### 2. Smart Response
When a meta-question is detected, instead of generating a SPARQL query, the system:
1. Shows what data it has (all entity types and their counts)
2. Lists types of questions it can answer
3. Explains special commands available
4. Provides helpful tips

### 3. User Flow

**Before (❌ Not useful):**
```
You: What can you do?
System: [Generates SPARQL query...]
System: Returns list of characters instead of capabilities
```

**After (✅ Helpful):**
```
You: What can you do?
System: Shows detailed capabilities
  - What data we have (87 characters, 61 planets, etc.)
  - Types of questions we can answer
  - Available special commands
  - Helpful tips for getting best results
```

---

## Implementation Details

### Code Changes

**File: `src/chat_interface.py`**

#### 1. Added Meta-Question Detection Method
```python
def _is_meta_question(self, user_input: str) -> Optional[str]:
    """
    Detect meta-questions about system capabilities
    Returns the command to execute, or None if it's a regular query
    """
```

#### 2. Added Capabilities Response Method
```python
def _print_capabilities(self):
    """Print system capabilities"""
    # Shows:
    # - Entity types and counts
    # - Available data statistics
    # - Types of questions we can answer
    # - Special commands
    # - Usage tips
```

#### 3. Integrated Into Main Loop
```python
# Check for meta-questions first
meta_command = self._is_meta_question(user_input)
if meta_command == 'capabilities':
    self._print_capabilities()
    continue
```

---

## Sample Responses

### When User Asks: "What can you do?"

```
============================================================
🤖 SYSTEM CAPABILITIES
============================================================

✨ I can help you explore the Star Wars universe!

📚 What I know about:
   ✓ FilmRole: 345 entries
   ✓ Person: 249 entries
   ✓ Character: 87 entries
   ✓ Planet: 61 entries
   ✓ Vehicle: 39 entries
   ✓ Starship: 37 entries
   ... and 45 more entity types

💬 Types of questions I can answer:
   ✓ Character information: 'Who is Luke Skywalker?'
   ✓ Relationships: 'Who is Han Solo married to?'
   ✓ Properties: 'How tall is Chewbacca?'
   ✓ Filtering: 'List all Jedi'
   ✓ Aggregates: 'How many planets are there?'
   ✓ Comparisons: 'Which character is the tallest?'
   ✓ Complex queries: 'Show me characters from Tatooine and their ships'

⚙️  Special commands:
   • help - Show detailed help
   • stats - Show graph statistics
   • schema - Show available data types
   • history - Show conversation history
   • clear - Clear conversation history
   • query <sparql> - Run raw SPARQL queries

💡 Tips:
   • I use natural language processing to convert your questions to queries
   • Ask in plain English - no special syntax needed
   • I can handle follow-ups based on previous questions
   • Type 'quit' or 'exit' to end the conversation
```

---

## User Experience Improvements

### Better Onboarding
- New users can type "what can you do?" to understand the system
- No longer get confused by irrelevant SPARQL results
- Clear list of example queries

### Better Navigation
- Updated welcome message mentions "what can you do"
- Users know how to discover capabilities

### Reduced Friction
- No need to read 10+ documentation files to understand capabilities
- One command shows everything immediately

---

## Pattern Matching Details

The detection system handles:

### Exact Matches
```
Input: "what can you do"
Detected: YES → Show capabilities
```

### Case Insensitivity
```
Input: "WHAT CAN YOU DO?"
Detected: YES → Show capabilities
```

### Extra Punctuation
```
Input: "what can you do???"
Detected: YES → Show capabilities
```

### Variations
```
Input: "who are you"     → YES
Input: "tell me about yourself" → YES
Input: "about"           → YES
```

### Not Meta-Questions
```
Input: "What is Luke?"           → NO (about character)
Input: "How many planets?"       → NO (data query)
Input: "Tell me about Tatooine"  → NO (data query)
```

---

## Benefits

✅ **Better UX**: Users get helpful answers immediately  
✅ **Reduced Confusion**: Meta-questions don't trigger irrelevant queries  
✅ **Better Onboarding**: New users understand capabilities quickly  
✅ **Improved Navigation**: Users know how to explore the system  
✅ **Smart Filtering**: Doesn't interfere with actual data queries  

---

## Technical Quality

- **Type-Safe**: Uses `Optional[str]` for return type
- **Clean Code**: Separate method for capabilities display
- **Maintainable**: Easy to add more meta-question patterns
- **Performant**: Simple string matching (no regex overhead)
- **Robust**: Handles case sensitivity and punctuation variations

---

## Testing

You can test the feature yourself:

```bash
export MOONSHOTAI_API_KEY="your-key"
export SWAPI_MODEL="kimi-k2.5"
python main.py

# Try these questions:
? > what can you do
? > who are you
? > tell me about yourself
? > capabilities

# These still work as data queries:
? > How many characters?
? > Who is Luke?
? > Tell me about Tatooine
```

---

## Future Enhancements

Potential additions:
- Follow-up questions about specific capabilities
- Search examples ("Show me examples of X")
- Tutorial/guided tour mode
- Feedback collection ("Was this helpful?")
- Personalized capabilities based on data available

---

## Summary

The meta-question detection system improves the user experience by:
1. **Recognizing** when users ask about system capabilities
2. **Responding helpfully** with relevant information
3. **Not interfering** with actual data queries
4. **Enabling better onboarding** for new users

Users can now simply type **"what can you do?"** and get a comprehensive overview of the system's capabilities! 🌟
