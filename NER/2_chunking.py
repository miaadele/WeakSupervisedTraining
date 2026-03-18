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

#RESULTS
# Loaded entity mentions: 395666
# Unique entity strings: 70515
# Top 20 entity strings:
#   10511  two
#    9666  one
#    8904  first
#    8260  three
#    5392  four
#    4614  christian
#    4150  indian
#    3609  english
#    3420  five
#    3074  portugal
#    2764  six
#    2722  second
#    2682  england
#    2426  seven
#    2056  eight
#    2042  ten
#    1933  spain
#    1750  twenty
#    1577  china
#    1573  half
# Filtered entity mentions: 216582

# Top 15 ORG:
#     379  constantinople
#     371  tyrone
#     305  parliament
#     227  senate
#     192  banda
#     186  christendom
#     168  cathay
#     167  cortes
#     161  nanquin
#     146  army
#     142  pegu
#     135  caesar
#     135  inca
#     134  connaght
#     127  tigris

# Top 15 GPE:
#    3074  portugal
#    2677  england
#    1933  spain
#    1577  china
#    1371  india
#    1211  egypt
#     958  jerusalem
#     907  rome
#     826  persia
#     739  peru
#     724  france
#     693  italy
#     654  mexico
#     650  ireland
#     633  london

# Top 15 PERSON:
#     800  john
#     625  thomas
#     620  lib
#     581  turk
#     522  alexander
#     452  solomon
#     390  david
#     384  chinois
#     357  henry
#     353  abraham
#     353  bantam
#     348  peter
#     338  fez
#     328  paul
#     317  william

# Top 15 LOC:
#    1162  africa
#     815  asia
#     754  europe
#     391  sea
#     354  the red sea
#     249  the south sea
#     140  east
#     121  south
#     113  west
#     102  the sea coast
#      98  the ocean sea
#      94  north
#      85  mars
#      84  alps
#      76  the north sea

# Top 15 NORP:
#    4614  christian
#    4150  indian
#    1943  english
#    1204  spanish
#    1079  french
#     946  greek
#     851  dutch
#     849  persian
#     726  egyptian
#     633  italian
#     441  latin
#     431  arabian
#     410  jewish
#     401  german
#     373  irish