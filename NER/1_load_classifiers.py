from pathlib import Path
import joblib

MODEL_DIR = Path("1_load_classifiers.py").resolve().parents[1]/"models"

# Load the SAME TF-IDF vectorizer and classifier you trained in Week 08–09
vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer_L2.joblib")
clf        = joblib.load(MODEL_DIR / "merchant_logreg_L2.joblib")

print("Loaded TF-IDF vectorizer + logistic regression classifier.")

### apply to JSON corpus
import json

with open(Path.cwd() / "new_texts.json", "r", encoding="utf-8") as f:
    records = json.load(f)

texts = [r["text"] for r in records]

X_new = vectorizer.transform(texts)    # IMPORTANT: use transform, not fit_transform
probs = clf.predict_proba(X_new)[:, 1]
preds = (probs >= 0.50).astype(int)

for r, p, yhat in zip(records, probs, preds):
    r["pred_prob_merchant"] = float(p)
    r["pred_merchant"] = int(yhat)

print("Classified:", len(records), "documents")
print("Predicted merchant (threshold .50):", sum(preds))

#save the classified corpus by adding the predictions into the JSON file
import json

OUT_CLASSIFIED = Path.cwd() / "classified_texts.json"

with open(OUT_CLASSIFIED, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
print("Saved classified dataset:", OUT_CLASSIFIED.resolve())

# create a higher confidence subset with threshold of 0,70
THRESH = 0.70
merchant_only = [r for r in records if r["pred_prob_merchant"] >= THRESH]

OUT_MERCHANT = Path.cwd() / "merchant_texts_for_spacy.json"

with open(OUT_MERCHANT, "w", encoding="utf-8") as f:
    json.dump(merchant_only, f, ensure_ascii=False, indent=2)

print(f"High-confidence merchant texts (p >= {THRESH}):", len(merchant_only))
print("Saved:", OUT_MERCHANT.resolve())

### checking how this higher threshold compares with the 0.50 one

top5 = sorted(records, key=lambda r: r["pred_prob_merchant"], reverse=True)[:5]
for r in top5:
    print(r["doc_id"], r["pred_prob_merchant"])