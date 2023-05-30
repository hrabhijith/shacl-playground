import json
from rdflib import Graph, plugin
from rdflib.serializer import Serializer

def jsonld_to_shacl(jsonld_data):
    # Load JSON-LD data
    graph = Graph().parse(data=jsonld_data, format='json-ld')

    # Serialize the graph to SHACL TTL (Turtle) format
    shacl_ttl = graph.serialize(format='turtle')

    return shacl_ttl

# # Example JSON-LD data
# jsonld_data = '''
# {
#     "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld",
#     "id": "urn:filter:1",
#     "type": "https://industry-fusion.com/types/v0.9/filter",
#     "https://industry-fusion.com/types/v0.9/state": [
#       {
#         "type": "Property",
#         "value": {
#           "@id": "https://industry-fusion.com/types/v0.9/state_ON"
#         }
#       },
#       {
#         "type": "Property",
#         "value": {
#           "@id": "https://industry-fusion.com/types/v0.9/state_ON"
#         }
#       }
#     ],
#     "https://industry-fusion.com/types/v0.9/strength": {
#       "type": "Property",
#       "value": "0.9"
#     }
# }
# '''

# # Convert JSON-LD to SHACL TTL
# shacl_ttl = jsonld_to_shacl(jsonld_data)

# # Print the resulting SHACL TTL
# print(shacl_ttl)