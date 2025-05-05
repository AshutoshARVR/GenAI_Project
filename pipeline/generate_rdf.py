import pandas as pd
import json
import os
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD

# 🧠 Step 1: Load ontology file (TTL format)
base_dir = os.path.dirname(os.path.dirname(__file__))  # Go up to project root
ontology_path = os.path.join(base_dir, "ontology", "TestOntology.ttl")
g = Graph()
g.parse(ontology_path, format="turtle")

# 🧠 Step 2: Bind the ontology namespace
EX = Namespace("http://example.org/ontology#")
g.bind("ex", EX)

# 🧠 Step 3: Load the JSON mapping
map_path = os.path.join(base_dir, "mappings", "field_map.json")
with open(map_path) as f:
    mapping = json.load(f)

# 🧠 Step 4: Loop through each class in the mapping
for class_name, field_map in mapping.items():
    # Dynamically get the correct file path
    if class_name == "TestAsset":
        file_path = os.path.join(base_dir, "data_sources", "test_assets.xlsx")
        df = pd.read_excel(file_path)
    elif class_name == "Engineer":
        file_path = os.path.join(base_dir, "data_sources", "Engineers.csv")
        df = pd.read_csv(file_path)
    else:
        continue

    for _, row in df.iterrows():
        # Identify the subject URI using the designated 'individual_name'
        subject = None
        for field, ont_prop in field_map.items():
            if ont_prop == "individual_name":
                subject = URIRef(f"http://example.org/ontology#{str(row[field]).replace(' ', '_')}")
                g.add((subject, RDF.type, EX[class_name]))
        if not subject:
            continue

        # Add RDF triples for each property
        for field, ont_prop in field_map.items():
            if ont_prop == "individual_name":
                continue
            value = row[field]
            if pd.isna(value):
                continue
            g.add((subject, EX[ont_prop], Literal(value)))

# 🧠 Step 5: Save combined graph to RDF file
output_path = os.path.join(base_dir, "graphdb", "generated_data.rdf")
g.serialize(output_path, format="xml")
print(f"✅ Ontology + data saved to {output_path}")
