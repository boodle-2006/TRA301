import os
import zipfile
import urllib.request
import pickle
import numpy as np

GLOVE_URL = "http://nlp.stanford.edu/data/glove.6B.zip"
ZIP_FILE = "glove.6B.zip"
TXT_FILE = "glove.6B.300d.txt"
OUT_VOCAB = "sgns/modern-vocab.pkl"
OUT_W = "sgns/modern-w.npy"

def download_glove():
    if not os.path.exists(ZIP_FILE) and not os.path.exists(TXT_FILE):
        print(f"Downloading {GLOVE_URL} (this may take a while)...")
        urllib.request.urlretrieve(GLOVE_URL, ZIP_FILE)
        print("Download complete.")

    if not os.path.exists(TXT_FILE):
        print(f"Extracting {TXT_FILE}...")
        with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
            zf.extract(TXT_FILE)
        print("Extraction complete.")

def parse_glove():
    print(f"Parsing {TXT_FILE}...")
    vocab = []
    vectors = []
    
    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            word = parts[0]
            try:
                vec = np.array(parts[1:], dtype=np.float32)
                # Ensure it's 300d
                if len(vec) == 300:
                    vocab.append(word)
                    vectors.append(vec)
            except Exception as e:
                continue

    print(f"Loaded {len(vocab)} words.")
    
    vectors_array = np.array(vectors)
    
    print(f"Saving to {OUT_VOCAB} and {OUT_W}...")
    with open(OUT_VOCAB, 'wb') as f:
        pickle.dump(vocab, f)
        
    np.save(OUT_W, vectors_array)
    print("Done!")

if __name__ == "__main__":
    download_glove()
    parse_glove()
