from rdflib import Graph, Namespace
import os

# Load RDF file
base_dir = os.path.dirname(os.path.dirname(__file__))
rdf_path = os.path.join(base_dir, "graphdb", "generated_data.rdf")

g = Graph()
g.parse(rdf_path, format="xml")

# Define namespace (must match your ontology!)
EX = Namespace("http://example.org/ontology#")
g.bind("ex", EX)

# Run SPARQL query: Get all test assets and their productive time
query = """
PREFIX ex: <http://example.org/ontology#>
SELECT ?asset ?time
WHERE {
  ?asset a ex:TestAsset ;
         ex:ProductiveOperatingTime ?time .
}
"""

results = g.query(query)

# Print the results
print("🧠 Productive Operating Time of Test Assets:\n")
for row in results:
    asset = row.asset.split("#")[-1].replace("_", " ")
    time = row.time
    print(f"- {asset} → {time} hours")
