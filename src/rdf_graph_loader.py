"""
RDF Graph Loader Module
Handles loading and querying the Star Wars RDF data
"""

from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef
from typing import List, Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SWAPIGraphDB:
    """Main class for managing Star Wars RDF Graph Database"""

    def __init__(self, ttl_file_path: str):
        """
        Initialize the graph database by loading RDF data
        
        Args:
            ttl_file_path: Path to the SWAPI TTL file
        """
        self.graph = Graph()
        self.ttl_file = Path(ttl_file_path)
        
        # Load namespaces
        self.voc = Namespace("https://swapi.co/vocabulary/")
        self.swapi = Namespace("https://swapi.co/resource/")
        
        # Bind common prefixes
        self.graph.bind("voc", self.voc)
        self.graph.bind("swapi", self.swapi)
        
        self.load_graph()
        
    def load_graph(self):
        """Load RDF data from TTL file"""
        if not self.ttl_file.exists():
            raise FileNotFoundError(f"TTL file not found: {self.ttl_file}")
        
        logger.info(f"Loading RDF graph from {self.ttl_file}")
        self.graph.parse(str(self.ttl_file), format='turtle')
        logger.info(f"Graph loaded successfully. Triples count: {len(self.graph)}")
        
    def get_graph_schema(self) -> Dict:
        """
        Extract schema information from the graph
        Returns information about classes and properties
        """
        schema = {
            "classes": set(),
            "properties": set(),
            "sample_data": {}
        }
        
        # Extract all classes (rdf:type)
        from rdflib import RDF
        for s, o in self.graph.subject_objects(RDF.type):
            class_name = str(o).replace(str(self.voc), "")
            schema["classes"].add(class_name)
            
            # Sample data
            if class_name not in schema["sample_data"]:
                schema["sample_data"][class_name] = []
            if len(schema["sample_data"][class_name]) < 3:
                schema["sample_data"][class_name].append(str(s))
        
        # Extract all properties
        for s, p, o in self.graph.triples((None, None, None)):
            prop_name = str(p).replace(str(self.voc), "")
            if prop_name not in ["type", "label", "description"]:
                schema["properties"].add(prop_name)
        
        return {
            "classes": sorted(list(schema["classes"])),
            "properties": sorted(list(schema["properties"])),
            "sample_data": schema["sample_data"]
        }
    
    def execute_sparql(self, query: str) -> List[Dict]:
        """
        Execute a SPARQL query and return results
        
        Args:
            query: SPARQL query string
            
        Returns:
            List of result dictionaries
        """
        try:
            results = self.graph.query(query)
            result_list = []
            for row in results:
                # Convert RDFlib Row to dictionary by iterating over variable names
                row_dict = {}
                for var in results.vars:
                    value = row[var]
                    if value is not None:
                        row_dict[str(var)] = str(value)
                    else:
                        row_dict[str(var)] = None
                result_list.append(row_dict)
            return result_list
        except Exception as e:
            logger.error(f"SPARQL query error: {e}")
            raise
    
    def find_by_label(self, label: str) -> List[Tuple]:
        """
        Find entities by their label/name
        
        Args:
            label: The label to search for (case-insensitive)
            
        Returns:
            List of (entity_uri, entity_label) tuples
        """
        from rdflib import RDFS
        results = []
        
        for s, o in self.graph.subject_objects(RDFS.label):
            if label.lower() in str(o).lower():
                results.append((str(s), str(o)))
        
        return results
    
    def get_entity_properties(self, entity_uri: str) -> Dict:
        """
        Get all properties of a specific entity
        
        Args:
            entity_uri: URI of the entity
            
        Returns:
            Dictionary of properties and their values
        """
        properties = {}
        entity = URIRef(entity_uri)
        
        for p, o in self.graph.predicate_objects(entity):
            prop_key = str(p).split("/")[-1]
            
            # Handle multiple values
            if prop_key not in properties:
                properties[prop_key] = []
            
            properties[prop_key].append(str(o))
        
        # Convert single-item lists to strings
        return {k: v[0] if len(v) == 1 else v for k, v in properties.items()}
    
    def get_graph_stats(self) -> Dict:
        """Get basic statistics about the graph"""
        from rdflib import RDF
        
        num_entities = len(set([s for s, p, o in self.graph]))
        num_relations = len(set([p for s, p, o in self.graph]))
        
        # Count entity types
        type_counts = {}
        for s, o in self.graph.subject_objects(RDF.type):
            type_name = str(o).replace(str(self.voc), "")
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_triples": len(self.graph),
            "total_entities": num_entities,
            "total_relations": num_relations,
            "entity_types": type_counts
        }


def initialize_db(ttl_path: str) -> SWAPIGraphDB:
    """Convenience function to initialize the database"""
    return SWAPIGraphDB(ttl_path)
