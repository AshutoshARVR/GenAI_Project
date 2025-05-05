from rdflib import Graph
import os

# Step 1: Get file paths
base_dir = os.path.dirname(os.path.dirname(__file__))
rdf_path = os.path.join(base_dir, "graphdb", "generated_data.rdf")
output_path = os.path.join(base_dir, "graphdb", "context.txt")

# Step 2: Load RDF graph
g = Graph()
g.parse(rdf_path, format="xml")


# Step 3: Create human-readable sentences
def format_term(term):
    """Helper to clean up URIs and literals"""
    term = str(term)
    if "#" in term:
        return term.split("#")[-1].replace("_", " ")
    return term


sentences = []

for subj, pred, obj in g:
    subject = format_term(subj)
    predicate = format_term(pred)
    object_ = format_term(obj)

    # Make it human readable
    if predicate == "type":
        sentence = f"{subject} is a {object_}."
    else:
        sentence = f"{subject} has {predicate} {object_}."

    sentences.append(sentence)

# Step 4: Save sentences to context.txt
with open(output_path, "w", encoding="utf-8") as f:
    for s in sentences:
        f.write(s + "\n")

print(f"✅ {len(sentences)} facts written to: {output_path}")
