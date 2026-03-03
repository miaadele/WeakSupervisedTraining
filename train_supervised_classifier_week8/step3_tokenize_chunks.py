from pathlib import Path
import nltk
from gensim.utils import simple_preprocess

nltk.download("punkt", quiet = True)
nltk.download("punkt_tab", quiet = True)

cwd = Path.cwd()
parent = cwd.parent
TEXT_DIR = parent / "Train_Test_Documents"
txt_paths = sorted(TEXT_DIR.glob("*.txt"))

sample_path = TEXT_DIR / "A00419.txt"

with open(sample_path, "r", encoding="utf-8", errors = "ignore") as f:
    text = f.read()

#split text into sentences
sentences = nltk.sent_tokenize(text)

TARGET_WORDS = 120

chunks = []
current = []
current_len = 0

for sent in sentences:
    words = sent.split()
    if not words:
        continue
    if current_len + len(words) > TARGET_WORDS and current:
        chunks.append(" ".join(current))
        current = []
        current_len = 0
    current.append(sent)
    current_len += len(words)

if current:
    chunks.append(" ".join(current))

#tokenize each chunk
token_lists = [simple_preprocess(c, deacc = True) for c in chunks]

print("File:", sample_path)
print("Chunks (strings):", len(chunks))
print("Chunks (token lists):", len(token_lists))

print("\n--- Token preview (first 60 tokens of first chunk) ---")
print(token_lists[0][:60])

print("\n--- Token count of first chunk ---")
print(len(token_lists[0]))