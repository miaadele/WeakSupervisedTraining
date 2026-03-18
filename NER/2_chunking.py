import spacy
import json
import re
from pathlib import Path

# Load the English model
nlp = spacy.load("en_core_web_sm") 

print("spaCy model loaded.")
MERCHANT_PATH = Path.cwd() / "NER"/"merchant_texts_for_spacy.json"

with open(MERCHANT_PATH, "r", encoding="utf-8") as f:
    merchant_records = json.load(f)

print("Number of merchant texts:", len(merchant_records))

sample_text = merchant_records[0]["text"]

doc = nlp(sample_text) #passes raw text into a processing pipeline that
#tokenizes the text
#splits sentences
#assigns part-of-speech tag
#computes syntactic dependencies
#identifies named entities

#doc is a structured spaCy Doc object that contains:
#the original text
#a sequence of tokens
#sentence boundaries
#POS tags
#dependency relations
#named entities
#character offsets

print("Processed one document.")
print("Number of tokens:", len(doc))

#extract the named entities for doc and inspect them
#doc.ents is a list of entity span objects, where each ent has attributes
for ent in doc.ents:
    print(ent.text, "|", ent.label_)

from collections import Counter

#create a dictionary-like object that counts the frequency of each entity
Counter([ent.label_ for ent in doc.ents]) 

all_entities = []
all_entities = []

CHUNK_SIZE = 50000  # characters per chunk

for record in merchant_records:
    text = record["text"]
    
    # Split text into chunks
    for i in range(0, len(text), CHUNK_SIZE):
        chunk = text[i:i + CHUNK_SIZE]
        doc = nlp(chunk)
        
        for ent in doc.ents:
            all_entities.append({
                "doc_id": record["doc_id"],
                "entity_text": ent.text,
                "entity_label": ent.label_
            })

print("Total entities extracted:", len(all_entities)) 

#### IMPORTANT STEP: save all the raw entities

import json
from pathlib import Path
import re
from collections import Counter

OUT_ENTS_RAW = Path.cwd() / "merchant_entities_raw.json"

with open(OUT_ENTS_RAW, "w", encoding="utf-8") as f:
    json.dump(all_entities, f, ensure_ascii=False, indent=2)

print("Saved raw entity mentions:", OUT_ENTS_RAW.resolve())


# SAVE baseline location counts (GPE and LOC) for later comparison with trained 

KEEP_LABELS = {"GPE", "LOC"}

def normalize_ent(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text.lower()

counts_by_label = {lab: Counter() for lab in KEEP_LABELS}

for e in all_entities:
    lab = e["entity_label"]
    if lab in KEEP_LABELS:
        counts_by_label[lab][normalize_ent(e["entity_text"])] += 1

OUT_BASE_COUNTS = Path.cwd() / "merchant_locations_counts_base.json"
counts_out = {lab: dict(c.most_common()) for lab, c in counts_by_label.items()}

with open(OUT_BASE_COUNTS, "w", encoding="utf-8") as f:
    json.dump(counts_out, f, ensure_ascii=False, indent=2)

print("Saved baseline counts:", OUT_BASE_COUNTS.resolve())