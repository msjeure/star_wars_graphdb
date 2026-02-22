"""
Query Builder and SPARQL Template Engine
Converts natural language to SPARQL queries
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class QueryTemplate:
    """Template for common SPARQL query patterns"""
    name: str
    description: str
    template: str
    example: str


class SPARQLQueryBuilder:
    """Builds SPARQL queries from templates and parameters"""
    
    # Common SPARQL prefixes
    PREFIXES = """
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX swapi: <https://swapi.co/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
"""
    
    # Query templates for common patterns
    TEMPLATES = {
        "find_by_name": QueryTemplate(
            name="find_by_name",
            description="Find characters/planets/vehicles by name",
            template="""
{PREFIXES}
SELECT ?entity ?label WHERE {{
    ?entity rdfs:label ?label .
    FILTER(CONTAINS(LCASE(str(?label)), LCASE("{name}")))
}}
LIMIT 10
""",
            example="Find Luke Skywalker"
        ),
        
        "character_properties": QueryTemplate(
            name="character_properties",
            description="Get properties of a character",
            template="""
{PREFIXES}
SELECT ?property ?value WHERE {{
    swapi:{char_id} ?property ?value .
}}
""",
            example="What are the properties of Luke Skywalker"
        ),
        
        "characters_by_type": QueryTemplate(
            name="characters_by_type",
            description="Find all characters of a specific species/type",
            template="""
{PREFIXES}
SELECT ?character ?label WHERE {{
    ?character a voc:{species} ;
               rdfs:label ?label .
}}
LIMIT 20
""",
            example="List all Jedi characters"
        ),
        
        "characters_by_film": QueryTemplate(
            name="characters_by_film",
            description="Find characters in a specific film",
            template="""
{PREFIXES}
SELECT ?character ?label WHERE {{
    ?character rdfs:label ?label ;
               voc:film swapi:{film_id} .
}}
LIMIT 20
""",
            example="Who appeared in A New Hope"
        ),
        
        "character_relationships": QueryTemplate(
            name="character_relationships",
            description="Find relationships between characters",
            template="""
{PREFIXES}
SELECT ?character1 ?label1 ?relation ?character2 ?label2 WHERE {{
    ?character1 rdfs:label ?label1 ;
                ?relation ?character2 .
    ?character2 rdfs:label ?label2 .
    FILTER(?relation != rdf:type)
}}
LIMIT 20
""",
            example="Show relationships between characters"
        ),
        
        "count_by_type": QueryTemplate(
            name="count_by_type",
            description="Count entities of a specific type",
            template="""
{PREFIXES}
SELECT (COUNT(?entity) as ?count) WHERE {{
    ?entity a voc:{type} .
}}
""",
            example="How many Droid characters are there"
        ),
        
        "homeworld_info": QueryTemplate(
            name="homeworld_info",
            description="Get information about a character's homeworld",
            template="""
{PREFIXES}
SELECT ?character ?charLabel ?homeworld ?worldLabel WHERE {{
    ?character rdfs:label ?charLabel ;
               voc:homeworld ?homeworld .
    ?homeworld rdfs:label ?worldLabel .
    FILTER(CONTAINS(LCASE(str(?charLabel)), LCASE("{name}")))
}}
""",
            example="What is Luke's homeworld"
        ),
        
        "species_stats": QueryTemplate(
            name="species_stats",
            description="Get statistics about a species",
            template="""
{PREFIXES}
SELECT (COUNT(?char) as ?count) (AVG(?height) as ?avg_height) WHERE {{
    ?char a voc:{species} ;
           voc:height ?height .
}}
""",
            example="What is the average height of Ewoks"
        ),
    }
    
    def __init__(self):
        """Initialize the query builder"""
        self.templates = self.TEMPLATES
    
    def build_find_by_name(self, name: str) -> str:
        """Build a query to find entities by name"""
        return self._fill_template("find_by_name", {"name": name})
    
    def build_characters_by_species(self, species: str) -> str:
        """Build a query to find characters of a specific species"""
        return self._fill_template("characters_by_type", {"species": species})
    
    def build_characters_by_film(self, film_name: str) -> str:
        """Build a query to find characters in a specific film"""
        film_id = self._map_film_name_to_id(film_name)
        return self._fill_template("characters_by_film", {"film_id": film_id})
    
    def build_count_query(self, entity_type: str) -> str:
        """Build a query to count entities of a type"""
        return self._fill_template("count_by_type", {"type": entity_type})
    
    def build_homeworld_query(self, character_name: str) -> str:
        """Build a query to find character's homeworld"""
        return self._fill_template("homeworld_info", {"name": character_name})
    
    def build_species_stats(self, species: str) -> str:
        """Build a query to get species statistics"""
        return self._fill_template("species_stats", {"species": species})
    
    def _fill_template(self, template_name: str, params: Dict[str, str]) -> str:
        """Fill a template with parameters"""
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name].template
        filled = template.format(**params)
        return filled
    
    def _map_film_name_to_id(self, film_name: str) -> str:
        """Map film names to their IDs"""
        film_map = {
            "a new hope": "1",
            "empire strikes back": "2",
            "return of the jedi": "3",
            "phantom menace": "4",
            "attack of the clones": "5",
            "revenge of the sith": "6",
            "force awakens": "7",
            "last jedi": "8",
        }
        return film_map.get(film_name.lower(), "1")
    
    def get_template_info(self) -> List[Dict]:
        """Get information about available templates"""
        return [
            {
                "name": t.name,
                "description": t.description,
                "example": t.example
            }
            for t in self.templates.values()
        ]


def build_simple_sparql(entity_type: str, filters: Optional[Dict] = None) -> str:
    """
    Build a simple SPARQL query with optional filters
    
    Args:
        entity_type: The type of entity to query (e.g., "Character", "Planet")
        filters: Optional dictionary of filters
    
    Returns:
        SPARQL query string
    """
    prefixes = """
PREFIX voc: <https://swapi.co/vocabulary/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""
    
    query = f"""
{prefixes}
SELECT ?entity ?label WHERE {{
    ?entity a voc:{entity_type} ;
            rdfs:label ?label .
}}
LIMIT 50
"""
    
    return query
