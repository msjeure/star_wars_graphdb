"""
Agent Module - Natural Language to SPARQL Conversion
Uses Claude API to convert natural language questions to SPARQL queries
"""

import os
import json
import logging
from typing import Optional, Dict, List, Tuple
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class StarWarsGraphAgent:
    """
    AI Agent that converts natural language questions to SPARQL queries
    and executes them against the Star Wars knowledge graph
    """
    
    def __init__(self, graph_db, model: str = "gpt-4", api_key: Optional[str] = None, provider: str = "auto"):
        """
        Initialize the agent
        
        Args:
            graph_db: Instance of SWAPIGraphDB
            model: LLM model to use (gpt-4, gpt-3.5-turbo, kimi-k2.5, etc.)
            api_key: API key (if not provided, reads from env)
            provider: LLM provider ("openai", "moonshotai", or "auto" for auto-detection)
        """
        self.graph_db = graph_db
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("MOONSHOTAI_API_KEY")
        self.provider = provider
        self.conversation_history = []
        
        # Get graph schema for context
        self.graph_schema = graph_db.get_graph_schema()
        self.graph_stats = graph_db.get_graph_stats()
        
        # Initialize LLM client
        self._init_llm_client()
    
    def _init_llm_client(self):
        """Initialize the LLM client"""
        # Auto-detect provider if not specified
        if self.provider == "auto":
            if self.model.startswith("kimi"):
                self.provider = "moonshotai"
                self.llm_type = "moonshotai"
            elif self.model.startswith("gpt"):
                self.provider = "openai"
                self.llm_type = "openai"
            else:
                self.provider = "local"
                self.llm_type = "local"
        else:
            self.llm_type = self.provider
        
        # Try Moonshotai first
        if self.provider == "moonshotai" and self.api_key:
            try:
                from openai import OpenAI
                # Moonshotai uses OpenAI-compatible API
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url="https://api.moonshot.cn/v1"
                )
                logger.info(f"Initialized Moonshotai client with model {self.model}")
            except ImportError:
                logger.warning("OpenAI package not installed")
                self.client = None
                self.llm_type = "local"
        # Try OpenAI
        elif self.provider == "openai" and self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"Initialized OpenAI client with model {self.model}")
            except ImportError:
                logger.warning("OpenAI package not installed")
                self.client = None
                self.llm_type = "local"
        else:
            # For local/offline models, we'll implement basic patterns
            self.llm_type = "local"
            self.client = None
            logger.info("Using local pattern-based query generation")
    
    def get_system_prompt(self) -> str:
        """Generate the system prompt with graph schema"""
        schema_info = json.dumps(self.graph_schema, indent=2, default=str)
        stats_info = json.dumps(self.graph_stats, indent=2, default=str)
        
        return f"""You are an expert SPARQL query builder for a Star Wars Knowledge Graph.
        
Your task is to convert natural language questions into SPARQL queries that can be executed against the graph.

GRAPH SCHEMA:
{schema_info}

GRAPH STATISTICS:
{stats_info}

IMPORTANT RULES:
1. Always use these prefixes:
   PREFIX voc: <https://swapi.co/vocabulary/>
   PREFIX swapi: <https://swapi.co/resource/>
   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

2. Entity types are in the voc: namespace (e.g., voc:Character, voc:Planet, voc:Vehicle)

3. Properties are in the voc: namespace (e.g., voc:height, voc:mass, voc:film, voc:homeworld)

4. Labels are accessed via rdfs:label

5. Always include meaningful FILTER clauses when appropriate

6. Return queries in a valid SPARQL format

When responding:
1. First, show your understanding of the question
2. Then provide the SPARQL query in a code block marked with ```sparql
3. Briefly explain what the query will find

Be helpful and try to understand the user's intent even if the question is not perfectly precise."""

    def query(self, question: str) -> Tuple[str, List[Dict]]:
        """
        Convert a natural language question to SPARQL and execute it
        
        Args:
            question: Natural language question about the Star Wars universe
            
        Returns:
            Tuple of (generated_sparql_query, results_list)
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })
        
        # Generate SPARQL query
        sparql_query = self._generate_sparql_query(question)
        
        logger.info(f"Generated query:\n{sparql_query}")
        
        # Execute the query
        try:
            results = self.graph_db.execute_sparql(sparql_query)
            
            # Add to conversation history
            response_text = f"Found {len(results)} results"
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            return sparql_query, results
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            # Try to refine the query
            refined_query = self._refine_query_on_error(question, sparql_query, str(e))
            try:
                results = self.graph_db.execute_sparql(refined_query)
                return refined_query, results
            except:
                return sparql_query, []
    
    def _generate_sparql_query(self, question: str) -> str:
        """Generate SPARQL query from natural language question"""
        
        if self.client and self.llm_type in ["openai", "moonshotai"]:
            return self._generate_with_gpt(question)
        else:
            return self._generate_with_patterns(question)
    
    def _generate_with_gpt(self, question: str) -> str:
        """Generate query using GPT"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": question}
                ],
                temperature=0.2,
                max_tokens=1000
            )
            
            # Extract SPARQL query from response
            content = response.choices[0].message.content
            
            # Try to extract code block
            if "```sparql" in content:
                start = content.find("```sparql") + 9
                end = content.find("```", start)
                query = content[start:end].strip()
            elif "```" in content:
                start = content.find("```") + 3
                end = content.find("```", start)
                query = content[start:end].strip()
            else:
                query = content
            
            return query
        except Exception as e:
            logger.error(f"GPT generation error: {e}")
            return self._generate_with_patterns(question)
    
    def _generate_with_patterns(self, question: str) -> str:
        """Generate query using pattern matching (fallback)"""
        question_lower = question.lower()
        
        # Pattern: Find character by name (who is X, find X, etc)
        if any(word in question_lower for word in ["who is", "find", "tell me about", "character"]):
            # Try to extract a name from the question
            words = question_lower.split()
            potential_names = ["luke", "leia", "han", "yoda", "vader", "c-3po", "r2-d2", "obi-wan", 
                              "anakin", "padme", "palpatine", "dooku", "chewbacca", "bb-8", "rey", "kylo"]
            
            for name in potential_names:
                if name in question_lower:
                    return f"""PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label ?property ?value WHERE {{
    ?entity rdfs:label ?label ;
            ?property ?value .
    FILTER(CONTAINS(LCASE(str(?label)), LCASE("{name}")))
}}
LIMIT 50"""
            
            # If "who is" but no specific name, search for any character mentioned after "who is"
            if "who is" in question_lower:
                parts = question_lower.split("who is")
                if len(parts) > 1:
                    name = parts[1].strip().split()[0].rstrip("?").strip()
                    if name and len(name) > 2:
                        return f"""PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label ?property ?value WHERE {{
    ?entity rdfs:label ?label ;
            ?property ?value .
    FILTER(CONTAINS(LCASE(str(?label)), LCASE("{name}")))
}}
LIMIT 50"""
        
        # Pattern: How many / Count
        if any(word in question_lower for word in ["how many", "count", "total", "how much"]):
            if "planet" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?entity) as ?count) WHERE {
    ?entity a voc:Planet .
}"""
            elif "character" in question_lower or "person" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?entity) as ?count) WHERE {
    ?entity a voc:Character .
}"""
            elif "vehicle" in question_lower or "ship" in question_lower or "starship" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?entity) as ?count) WHERE {
    ?entity a voc:Vehicle .
}"""
            elif "droid" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?entity) as ?count) WHERE {
    ?entity a voc:Droid .
}"""
            # Default count
            return """PREFIX voc: <https://swapi.co/vocabulary/>
SELECT (COUNT(?entity) as ?count) WHERE {
    ?entity a voc:Character .
}"""
        
        # Pattern: List entities (list, show, all, etc)
        if any(word in question_lower for word in ["list", "show", "all", "give me", "what are"]):
            if "planet" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?entity ?label WHERE {
    ?entity a voc:Planet ;
            rdfs:label ?label .
}
LIMIT 50"""
            elif "droid" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?entity ?label WHERE {
    ?entity a voc:Droid ;
            rdfs:label ?label .
}
LIMIT 50"""
            elif "vehicle" in question_lower or "ship" in question_lower or "starship" in question_lower:
                return """PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?entity ?label WHERE {
    ?entity a voc:Vehicle ;
            rdfs:label ?label .
}
LIMIT 50"""
        
        # Default: List all characters (for unknown queries)
        return """PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?entity ?label WHERE {
    ?entity a voc:Character ;
            rdfs:label ?label .
}
LIMIT 20"""
    
    def _refine_query_on_error(self, question: str, failed_query: str, error: str) -> str:
        """Try to refine a failed query"""
        if self.client and self.llm_type in ["openai", "moonshotai"]:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": self.get_system_prompt()},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": f"```sparql\n{failed_query}\n```"},
                        {"role": "user", "content": f"This query failed with error: {error}\n\nPlease fix it and provide a corrected SPARQL query."}
                    ],
                    temperature=0.2,
                    max_tokens=1000
                )
                
                content = response.choices[0].message.content
                if "```sparql" in content:
                    start = content.find("```sparql") + 9
                    end = content.find("```", start)
                    return content[start:end].strip()
                elif "```" in content:
                    start = content.find("```") + 3
                    end = content.find("```", start)
                    return content[start:end].strip()
            except Exception as e:
                logger.error(f"Query refinement error: {e}")
        
        return failed_query
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


def create_agent(graph_db, model: str = "gpt-4") -> StarWarsGraphAgent:
    """Convenience function to create an agent"""
    return StarWarsGraphAgent(graph_db, model=model)
