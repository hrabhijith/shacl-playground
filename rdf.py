from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF
from rdflib.plugins.sparql import prepareQuery
from pyshacl import validate
from util import jsonld_to_shacl
from rdflib import BNode

# Define the SHACL shape
shape_url = "./shacl.ttl"
shape_graph = Graph().parse(shape_url, format="turtle")
shape = (Namespace("http://www.w3.org/ns/shacl#").Shape)

# Define the text prompt
text_prompt = "The example jsonld_data is valid against the example SHACL shape."

# Define the query template
query_template = """
PREFIX iff: <https://industry-fusion.com/types/v0.9/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ngsi-ld: <https://uri.etsi.org/ngsi-ld/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?strength
WHERE {
  <urn:filter:1> iff:strength ?strength .
  FILTER (?strength = "0.9")
}
"""

# Example JSON-LD data
jsonld_data = '''
{
    "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
    "id": "urn:filter:1",
    "type": "https://industry-fusion.com/types/v0.9/filter",
    "https://industry-fusion.com/types/v0.9/state": [
      {
        "type": "Property",
        "value": {
          "@id": "https://industry-fusion.com/types/v0.9/state_ON"
        }
      },
      {
        "type": "Property",
        "value": {
          "@id": "https://industry-fusion.com/types/v0.9/state_ON"
        }
      }
    ],
    "https://industry-fusion.com/types/v0.9/strength": {
      "type": "Property",
      "value": "0.9"
    }
}
'''

# Load the data graph
g = Graph()

# Convert JSON-LD to SHACL TTL
shacl_ttl = jsonld_to_shacl(jsonld_data)

# Save the SHACL TTL to a file
with open('output.ttl', 'w') as file:
    file.write(shacl_ttl)

g.parse("./output.ttl", format="turtle")


# Validate the data graph against the shape
conforms, results_graph, results = validate(g, shacl_graph=shape_graph, shacl_graph_format="turtle", ont_graph=g, inference='rdfs')

# Print the results
if conforms:
    print(text_prompt + " - PASSED")

    # Execute the query on the data graph
    queryResults = g.query(query_template)
    print(queryResults)
    
else:
    print(text_prompt + " - FAILED")
    print(results_graph.serialize(format="turtle"))
    print(results)

