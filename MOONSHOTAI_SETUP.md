# Using Moonshotai/Kimi with Star Wars GraphDB

## Quick Setup

The system now fully supports **Moonshotai/Kimi-K2.5** API! Here's how to get started:

### 1. Set Your Moonshotai API Key

```bash
export MOONSHOTAI_API_KEY="your-moonshotai-key-here"
export SWAPI_MODEL="kimi-k2.5"
```

Or create a `.env` file in the project directory:
```
MOONSHOTAI_API_KEY=your-moonshotai-key-here
SWAPI_MODEL=kimi-k2.5
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the System

```bash
python main.py
```

### 4. Start Asking Questions

```
? > Who is Luke Skywalker?
? > How many characters are there?
? > List all droids
```

---

## Configuration

### Environment Variables

| Variable | Value | Required |
|----------|-------|----------|
| `MOONSHOTAI_API_KEY` | Your Kimi API key | Yes (if using Kimi) |
| `SWAPI_MODEL` | `kimi-k2.5` | Yes (if using Kimi) |
| `OPENAI_API_KEY` | OpenAI key | No (if using Kimi) |

### Setting via Command Line

**On macOS/Linux:**
```bash
export MOONSHOTAI_API_KEY="your-key"
export SWAPI_MODEL="kimi-k2.5"
python main.py
```

**On Windows (PowerShell):**
```powershell
$env:MOONSHOTAI_API_KEY="your-key"
$env:SWAPI_MODEL="kimi-k2.5"
python main.py
```

### Setting via .env File

Create `.env` in the project root:
```
MOONSHOTAI_API_KEY=your-key-here
SWAPI_MODEL=kimi-k2.5
```

Then run:
```bash
python main.py
```

---

## How It Works

The system automatically detects your LLM provider:

```python
# Moonshotai is detected when:
# 1. Model name starts with "kimi" (e.g., "kimi-k2.5")
# 2. MOONSHOTAI_API_KEY environment variable is set

# It uses the OpenAI-compatible API endpoint:
# Base URL: https://api.moonshot.cn/v1
```

### Supported Models

**Moonshotai:**
- `kimi-k2.5` - Latest Kimi model (recommended)

**OpenAI (still supported):**
- `gpt-4` - GPT-4
- `gpt-3.5-turbo` - GPT-3.5 Turbo

**Fallback:**
- If no API key is provided, system uses pattern-based query generation

---

## Using Both APIs

You can switch between providers:

```bash
# Use Moonshotai
export MOONSHOTAI_API_KEY="your-kimi-key"
export SWAPI_MODEL="kimi-k2.5"
python main.py

# Switch to OpenAI
export OPENAI_API_KEY="sk-your-key"
export SWAPI_MODEL="gpt-4"
python main.py

# Use pattern matching (no API needed)
unset MOONSHOTAI_API_KEY
unset OPENAI_API_KEY
python main.py
```

---

## Python API Integration

Use Moonshotai in your own code:

```python
from src.rdf_graph_loader import initialize_db
from src.agent import StarWarsGraphAgent

# Initialize with Moonshotai
db = initialize_db("SWAPI-WD-data.ttl")
agent = StarWarsGraphAgent(
    db, 
    model="kimi-k2.5",
    api_key="your-moonshotai-key",
    provider="moonshotai"
)

# Or let it auto-detect
agent = StarWarsGraphAgent(db, model="kimi-k2.5")

# Query
sparql, results = agent.query("Who is Luke Skywalker?")
print(results)
```

---

## Troubleshooting

### "API key not found"
```bash
# Check if key is set
echo $MOONSHOTAI_API_KEY

# Set it
export MOONSHOTAI_API_KEY="your-key"
```

### "Connection error"
- Verify your Moonshotai API key is valid
- Check your internet connection
- Verify the endpoint is accessible

### "Model not found"
- Ensure `SWAPI_MODEL` is set to `kimi-k2.5`
- Check Moonshotai documentation for current model names

### "Falling back to pattern matching"
- System is working fine without API
- Queries will use pattern-based generation
- Results should still be accurate for common questions

---

## Features

✅ **Full Moonshotai/Kimi-K2.5 Support**
✅ **Auto-detection of API provider**
✅ **Seamless switching between providers**
✅ **Fallback to pattern matching**
✅ **OpenAI API still supported**
✅ **Works without any API key**

---

## Example Session

```bash
$ export MOONSHOTAI_API_KEY="your-key"
$ export SWAPI_MODEL="kimi-k2.5"
$ python main.py

📚 Initializing Star Wars Knowledge Graph...
🤖 Initializing AI Agent...
✅ System ready!

? > Who is Luke Skywalker?
🔄 Processing your question...

🔍 Generated SPARQL Query:
──────────────────────────
PREFIX voc: <https://swapi.co/vocabulary/>
...
──────────────────────────

✅ Found 1 result(s):
[{'entity': '...', 'label': 'Luke Skywalker', ...}]
```

---

## Performance

With Moonshotai/Kimi-K2.5:
- **Query generation**: 1-3 seconds
- **SPARQL execution**: <100ms
- **Total response time**: 1-4 seconds

---

## Support

For Moonshotai API issues:
- Check [Moonshotai Documentation](https://platform.moonshot.cn/)
- Verify your API key and billing
- Check API rate limits

For Star Wars GraphDB issues:
- See README.md
- Check GETTING_STARTED.md
- Review src/examples.py

---

**Ready to explore? Set your key and run `python main.py`! 🚀**
