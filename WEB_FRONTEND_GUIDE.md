# Star Wars GraphDB - Web Frontend Guide 🌐

## Overview

Your Star Wars GraphDB system now has a **modern web-based frontend** with both an interactive UI and a complete REST API!

```
Web Browser ↔ FastAPI Backend ↔ Agent System ↔ RDF Database
```

---

## Architecture

### Frontend Stack
- **HTML/CSS/JavaScript**: Interactive web interface
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Chat Interface**: Natural language query input
- **Modern UI**: Star Wars themed styling with yellow/gold colors

### Backend Stack
- **FastAPI**: High-performance Python web framework
- **REST API**: Clean, well-documented API endpoints
- **CORS Support**: Cross-origin requests enabled
- **Automatic Documentation**: Swagger UI included

### Data Flow
```
User Types Question
        ↓
Frontend (HTML/JS)
        ↓
FastAPI API (/api/query)
        ↓
Agent System (LLM/Pattern)
        ↓
RDF Database
        ↓
Results → Frontend Display
```

---

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This includes:
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `python-multipart==0.0.6` - Form data support

### 2. Verify Structure

Ensure you have:
```
static/
├── index.html       # Main page
├── styles.css       # Styling
└── script.js        # Frontend logic

api.py              # FastAPI backend
SWAPI-WD-data.ttl   # RDF data
```

---

## Running the Web Server

### Option 1: Direct Python (Simple)

```bash
python api.py
```

Then open your browser to: **http://localhost:8000**

### Option 2: Using Uvicorn (Recommended)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: In Production

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Environment Variables

```bash
export MOONSHOTAI_API_KEY="your-key"
export SWAPI_MODEL="kimi-k2.5"
python api.py
```

---

## Features

### 💬 Chat Interface
- Ask questions in natural language
- Real-time query processing
- Beautiful message display
- SPARQL query viewer

### 🔍 Search & Explore
- Search for entities by name
- View detailed entity properties
- Browse graph statistics
- Explore data schema

### 📊 Information Dashboard
- System capabilities overview
- Graph statistics (triples, entities, types)
- Data schema visualization
- Quick reference guide

### 📱 Responsive Design
- Desktop: Full-featured interface
- Tablet: Optimized layout
- Mobile: Touch-friendly controls

---

## API Endpoints

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "database": "loaded",
  "agent": "ready"
}
```

### Main Query Endpoint
```
POST /api/query
Content-Type: application/json

{
  "question": "Who is Luke Skywalker?"
}
```

Response:
```json
{
  "question": "Who is Luke Skywalker?",
  "sparql_query": "PREFIX voc: <...> SELECT ...",
  "results": [
    {"label": "Luke Skywalker", "height": "172cm", ...}
  ],
  "result_count": 1
}
```

### Statistics
```
GET /api/stats
```

### Schema Information
```
GET /api/schema
```

### System Capabilities
```
GET /api/capabilities
```

### Search Entities
```
GET /api/search/{search_term}
```

Example:
```
GET /api/search/luke
```

### Entity Details
```
GET /api/entity/{entity_id}
```

Example:
```
GET /api/entity/luke_skywalker
```

### Execute SPARQL
```
POST /api/sparql
Content-Type: application/json

{
  "query": "PREFIX voc: <...> SELECT ?x WHERE {...}"
}
```

---

## Using the Web Interface

### Chat Tab
1. **Type a question** in the input field
2. **Press Enter** or click **Send**
3. **View results** in the message area
4. **Click "View SPARQL Query"** to see the generated query

Example questions:
```
Who is Luke Skywalker?
How many planets are there?
List all droids
What species is Yoda?
Who are the Jedi?
```

### Explore Tab
1. **Search**: Find entities by name
2. **Statistics**: View graph statistics
3. **Schema**: Browse available data types

### Info Tab
1. **System Information**: Check API status
2. **Capabilities**: See what the system can do
3. **Quick Guide**: Learn how to use the system

---

## Response Examples

### Character Query
```
Question: "Who is Luke Skywalker?"

Results:
- name: Luke Skywalker
- height: 172cm
- mass: 77kg
- species: Human
- homeworld: Tatooine
```

### Aggregation Query
```
Question: "How many characters are there?"

Results:
- count: 87
```

### List Query
```
Question: "List all droids"

Results:
1. C-3PO
2. R2-D2
3. BB-8
... (showing 5 of 6)
```

### Search Query
```
Search: "luke"

Results:
1. Luke Skywalker (https://swapi.co/resource/luke_skywalker)
2. Luke's Tatooine Homestead (location)
```

---

## Frontend Tabs Explained

### 💬 Chat Tab
- **Purpose**: Main query interface
- **Features**:
  - Natural language input
  - Real-time processing
  - Message history
  - SPARQL query viewer
  - Result formatting

### 🔍 Explore Tab
- **Purpose**: Discover data
- **Features**:
  - Entity search
  - Statistical overview
  - Schema browser
  - Entity details

### ℹ️ Info Tab
- **Purpose**: System information
- **Features**:
  - System status
  - Capabilities overview
  - Usage guide
  - Example queries

---

## Styling & Customization

### Change Theme Colors
Edit `static/styles.css`:

```css
:root {
    --primary-color: #ffd700;      /* Gold */
    --secondary-color: #1a1a1a;    /* Dark */
    --text-light: #e0e0e0;
    --success-color: #4caf50;
    /* ... more colors ... */
}
```

### Customize Welcome Message
Edit `static/index.html`:

```html
<p>Custom welcome message here...</p>
```

### Add New Features
1. Add HTML to `static/index.html`
2. Add CSS to `static/styles.css`
3. Add JavaScript to `static/script.js`
4. Add API endpoint to `api.py`

---

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
uvicorn api:app --port 8001
```

### Database Not Loading
```bash
# Check TTL file location
ls -la SWAPI-WD-data.ttl

# Ensure correct path in api.py
current_dir = Path(__file__).parent
ttl_path = current_dir / "SWAPI-WD-data.ttl"
```

### API Not Responding
```bash
# Check API is running
curl http://localhost:8000/health

# Check logs for errors
# Response should be:
# {"status":"healthy","database":"loaded","agent":"ready"}
```

### CORS Errors
The API already has CORS enabled for all origins. If you still get errors:

```python
# In api.py, CORS middleware is already configured:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Slow Responses
- **First query**: May take 1-3 seconds (LLM API call)
- **Subsequent queries**: Cached responses are faster
- **Pattern matching**: If no API key, responses are instant

---

## Performance Tips

### 1. Enable Database Caching
The graph is loaded once at startup and reused for all queries.

### 2. Use Pattern Matching
If API is slow, the system falls back to pattern matching automatically.

### 3. Optimize Your Queries
```
❌ Bad:  "Tell me everything about Luke"
✅ Good: "Who is Luke Skywalker?"
```

### 4. Monitor Performance
Check browser console (F12) for request times.

---

## Integration Examples

### Using the API in Python
```python
import requests

# Query endpoint
response = requests.post('http://localhost:8000/api/query', json={
    'question': 'Who is Luke Skywalker?'
})
results = response.json()
print(results['results'])

# Search endpoint
response = requests.get('http://localhost:8000/api/search/luke')
entities = response.json()['results']
```

### Using the API in JavaScript
```javascript
// Already built into the frontend!
// But you can also use it standalone:

fetch('http://localhost:8000/api/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: 'How many planets?' })
})
.then(r => r.json())
.then(data => console.log(data.results))
```

### Using the API in cURL
```bash
# Query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is Luke?"}'

# Search
curl http://localhost:8000/api/search/luke

# Statistics
curl http://localhost:8000/api/stats
```

---

## Deployment

### Local Development
```bash
python api.py
```

### Docker (Coming Soon)
Create a `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "api.py"]
```

Build and run:
```bash
docker build -t star-wars-graphdb .
docker run -p 8000:8000 star-wars-graphdb
```

### Cloud Deployment
Can be deployed to:
- **Heroku** (free tier available)
- **Railway** (easy FastAPI deployment)
- **Render** (fast and reliable)
- **AWS** (EC2, Lambda)
- **Google Cloud** (App Engine, Run)
- **Azure** (App Service)

---

## File Structure

```
star_wars_graphdb/
├── api.py                      # FastAPI backend (NEW)
├── main.py                     # CLI entry point (existing)
├── SWAPI-WD-data.ttl          # RDF data
├── requirements.txt            # Updated with FastAPI
│
├── static/                     # Frontend files (NEW)
│   ├── index.html             # Main page
│   ├── styles.css             # Styling
│   └── script.js              # JavaScript logic
│
├── src/
│   ├── chat_interface.py      # CLI interface (existing)
│   ├── agent.py               # Query generation (existing)
│   ├── rdf_graph_loader.py    # Database (existing)
│   └── query_builder.py       # Templates (existing)
```

---

## Next Steps

### 1. Start the Server
```bash
python api.py
```

### 2. Open Browser
```
http://localhost:8000
```

### 3. Start Querying!
Ask a question in the chat interface.

### 4. Explore Features
- Try different questions
- Search for entities
- View statistics
- Check the schema

### 5. Integrate
- Use the REST API in your own applications
- Build mobile apps using the API
- Create custom interfaces
- Deploy to production

---

## Summary

You now have:

✅ **Web-based UI** - Beautiful, responsive interface  
✅ **REST API** - Clean, documented endpoints  
✅ **Chat Interface** - Conversational query system  
✅ **Search & Explore** - Data discovery tools  
✅ **Statistics** - System insights and metrics  
✅ **Star Wars Theme** - Engaging, iconic design  

**All built on top of your existing agent system!** 🚀

---

## Support

For issues:
1. Check the browser console (F12)
2. Check the server logs
3. Verify the database loaded correctly
4. Ensure API key is set (if using LLM)

Enjoy exploring the Star Wars universe! 🌟
