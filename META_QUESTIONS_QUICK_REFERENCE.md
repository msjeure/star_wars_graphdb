# Quick Reference: Meta-Questions Feature

## What's New?

When you ask about the system itself, you get helpful information instead of a data query!

## Meta-Questions (Questions About The System)

These questions now get special handling:

| Question | Response |
|----------|----------|
| "What can you do?" | Shows system capabilities |
| "Who are you?" | Shows system capabilities |
| "Tell me about yourself" | Shows system capabilities |
| "What is this?" | Shows system capabilities |
| "How does this work?" | Shows system capabilities |
| "Capabilities" | Shows system capabilities |
| "About" | Shows system capabilities |
| "What are you?" | Shows system capabilities |

## Data Queries (Questions About Star Wars Data)

These still work normally:

```
You: How many characters are there?
System: [Generates SPARQL query and returns count]

You: Who is Luke Skywalker?
System: [Generates query and shows Luke's details]

You: List all Jedi
System: [Generates query and shows all Jedi characters]
```

## The Difference

### Meta-Question
```
You: What can you do?
System: [Shows capabilities, available data types, examples, commands]
```

### Data Query
```
You: What can I find about characters?
System: [Treats as a data query about character entities]
```

## Try It!

```bash
python main.py

# Try asking about the system:
? > what can you do
? > who are you
? > about

# Or ask about the data:
? > How many planets?
? > Who is Yoda?
```

## System Auto-Detects

✅ Smart detection means:
- No special syntax needed
- Works with different phrasings
- Case-insensitive
- Handles extra punctuation
- Doesn't interfere with data queries

---

**Result: Better UX! Users get helpful answers instead of confused SPARQL queries.** 🎉
