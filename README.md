# shacl-playground

To install,

`pip3 install requirements.txt`

To run,

`python3 rdf.py`

Operations perfromed in 'rdf.py' are listed as follows.

1. "iff: <https://industry-fusion.com/types/v0.9/>" is the namespace used for RDF.
2. The "shacl.ttl" file defines the shape of the "filter" object in "iff" namespace. It defines that the filter can have two properties "state" and "strength". The "state" property should be IRI (eg. https://industry-fusion.com/types/v0.9/state_ON) as value. The "strength" property must be Literal (eg. 0.9) as value.
3. The JSON-LD variable in "rdf.py" is converted to SHACL turtle format for validation against the "shacl.ttl" file.
4. The "conforms" variable indicates whether the validation is passed or not.
5. The "query_template" variable containing SparQL query is also executed on JSON-LD.
6. The "results" variable shows the errors if "conforms" is false.

To test,

Change the value of "strength" property in JSON-LD inside "rdf.py" file to above 1.0 (eg, 1.1). And then, run the rdf.py. An error with details must be shown.

