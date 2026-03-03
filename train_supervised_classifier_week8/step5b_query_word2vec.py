#what words are near "merchant" in the vector space?

from pathlib import Path
from gensim.models import Word2Vec

model_path = Path("models") / "w2v_full.bin"
model = Word2Vec.load(str(model_path))

seed = "merchant"

if seed not in model.wv:
    print(f"'{seed}' not found in the model vocabulary.")
    print("This usually means min_count is too high or the corpus is too small.")
else:
    print(f"Top 30 words similar to '{seed}':")
    for word, score in model.wv.similar_by_word(seed, topn=30):
        print(f"  {word:20s} {score:.3f}")
    
#Result (corpus-specific semantic map for the concept of "merchant")
# Top 30 words similar to 'merchant':
#   marchant             0.745
#   factor               0.699
#   merchants            0.696
#   clothier             0.656
#   purser               0.652
#   adventurer           0.650
#   wholesale            0.646
#   jeweller             0.642
#   tailor               0.639
#   staplers             0.638
#   customer             0.634
#   apprentice           0.633
#   venturer             0.632
#   manufacturer         0.632
#   adventurers          0.630
#   brewer               0.628
#   sailor               0.628
#   banker               0.622
#   tradesman            0.620
#   seller               0.614
#   clothyer             0.611
#   middleborough        0.611
#   journeyman           0.611
#   mariner              0.609
#   retailer             0.608
#   gentleman            0.605
#   importer             0.604
#   farmer               0.602
#   worshipful           0.602
#   marchants            0.602