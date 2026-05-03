import pickle
import json
import re
import csv
import numpy as np
from collections import defaultdict

SGNS_DIR = "sgns"
LYRICS_FILE = "genre_lyrics.json"
OUTPUT_FILE = "weat_genre_results.csv"

STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
    "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
    'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
    'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
    'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
    'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
    'with', 'about', 'against', 'between', 'through', 'during', 'before',
    'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
    'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't',
    'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now',
    'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
    'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',
    "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't",
    'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
    "weren't", 'won', "won't", 'wouldn', "wouldn't",
    'oh', 'yeah', 'ya', 'na', 'la', 'da', 'ooh', 'ah', 'hey', 'uh',
    'gonna', 'wanna', 'gotta', 'em', 'cause', "'cause", 'got', 'get',
    'go', 'come', 'let', 'like', 'know', 'say', 'see', 'want', 'take',
    'make', 'give', 'tell', 'think', 'look', 'way', 'could', 'would',
    'back', 'well', 'also', 'into', 'one', 'two',
}

EA_NAMES = [
    'adam', 'chip', 'harry', 'josh', 'roger',
    'alan', 'frank', 'justin', 'ryan', 'stephen',
    'brad', 'greg', 'jack', 'matthew', 'todd',
]

AA_NAMES = [
    'darnell', 'tyrone', 'darius', 'lamar', 'malik',
    'leroy', 'jerome', 'jamal', 'cedric', 'terrell',
    'lionel', 'alonzo', 'lamont', 'desmond', 'andre',
]

PLEASANT = [
    'joy', 'love', 'peace', 'wonderful', 'pleasure',
    'glorious', 'laughter', 'happy', 'beautiful', 'paradise',
    'cheerful', 'excellent', 'fortunate', 'magnificent',
]

UNPLEASANT = [
    'agony', 'terrible', 'horrible', 'nasty', 'evil',
    'murder', 'failure', 'war', 'ugly', 'poverty',
    'sickness', 'tragedy', 'hatred', 'filthy',
]


def load_embeddings(decade, base_path=SGNS_DIR):
    effective_decade = min(decade, 1990)
    vocab_path = f"{base_path}/{effective_decade}-vocab.pkl"
    vectors_path = f"{base_path}/{effective_decade}-w.npy"

    with open(vocab_path, 'rb') as f:
        vocab = pickle.load(f, encoding='latin1')

    vectors = np.load(vectors_path)

    word2idx = {word: i for i, word in enumerate(vocab)}

    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1 
    vectors_normed = vectors / norms

    return word2idx, vectors_normed

def get_vector(word, word2idx, vectors):
    idx = word2idx.get(word)
    if idx is not None:
        return vectors[idx]
    return None


def cosine_sim(v1, v2):
    return float(np.dot(v1, v2))

def mean_cos_similarity(word_vec, target_words, word2idx, vectors):
    sims = []
    for tw in target_words:
        tv = get_vector(tw, word2idx, vectors)
        if tv is not None:
            sims.append(cosine_sim(word_vec, tv))
    if not sims:
        return None
    return np.mean(sims)

def weat_single_word_association(word_vec, attr_A, attr_B, word2idx, vectors):
    mean_a = mean_cos_similarity(word_vec, attr_A, word2idx, vectors)
    mean_b = mean_cos_similarity(word_vec, attr_B, word2idx, vectors)
    if mean_a is None or mean_b is None:
        return None
    return mean_a - mean_b

def weat_effect_size(target_X, target_Y, attr_A, attr_B, word2idx, vectors):
    s_X = []
    for word in target_X:
        wv = get_vector(word, word2idx, vectors)
        if wv is not None:
            assoc = weat_single_word_association(wv, attr_A, attr_B, word2idx, vectors)
            if assoc is not None:
                s_X.append(assoc)

    s_Y = []
    for word in target_Y:
        wv = get_vector(word, word2idx, vectors)
        if wv is not None:
            assoc = weat_single_word_association(wv, attr_A, attr_B, word2idx, vectors)
            if assoc is not None:
                s_Y.append(assoc)

    if not s_X or not s_Y:
        return None, None, None

    mean_X = np.mean(s_X)
    mean_Y = np.mean(s_Y)
    
    all_s = s_X + s_Y
    std_all = np.std(all_s, ddof=0)
    if std_all == 0:
        return None, None, None

    effect_size = (mean_X - mean_Y) / std_all
    return effect_size, mean_X, mean_Y

def compute_lyric_racial_association(lyric_words, word2idx, vectors):
    associations = []
    words_used = []

    for word in lyric_words:
        wv = get_vector(word, word2idx, vectors)
        if wv is None:
            continue

        mean_ea = mean_cos_similarity(wv, EA_NAMES, word2idx, vectors)
        mean_aa = mean_cos_similarity(wv, AA_NAMES, word2idx, vectors)

        if mean_ea is not None and mean_aa is not None:
            associations.append(mean_ea - mean_aa)
            words_used.append(word)

    if not associations:
        return None, [], 0

    return np.mean(associations), words_used, len(associations)

def tokenize_lyrics(lyrics_text):
    if not lyrics_text:
        return []
    text = lyrics_text.lower()
    words = re.findall(r'[a-z]+', text)
    content_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    unique_words = list(set(content_words))
    return unique_words

def run_analysis():
    print("Loading genre lyrics...")
    try:
        with open(LYRICS_FILE, 'r') as f:
            all_lyrics = json.load(f)
    except FileNotFoundError:
        print(f"Error: {LYRICS_FILE} not found. Run fetch_genre_lyrics.py first.")
        return

    results = []
    
    for decade_str in sorted(all_lyrics.keys()):
        decade = int(decade_str)
        genres = all_lyrics[decade_str]

        print(f"\n{'='*60}")
        print(f"  Decade: {decade}s")
        print(f"{'='*60}")

        word2idx, vectors = load_embeddings(decade)
        
        baseline_effect, _, _ = weat_effect_size(
            EA_NAMES, AA_NAMES, PLEASANT, UNPLEASANT, word2idx, vectors
        )

        for genre, songs in genres.items():
            if not songs:
                continue
                
            print(f"  --- {genre} ---")
            
            for song in songs:
                title = song["title"]
                artist = song["artist"]
                lyrics = song.get("lyrics", "")

                if not lyrics or song.get("word_count", 0) == 0:
                    results.append({
                        "decade": decade,
                        "genre": genre,
                        "title": title,
                        "artist": artist,
                        "racial_name_association": None,
                        "weat_effect_size": baseline_effect,
                        "status": "no_lyrics",
                    })
                    continue

                content_words = tokenize_lyrics(lyrics)
                racial_assoc, words_used, n_words = compute_lyric_racial_association(
                    content_words, word2idx, vectors
                )

                status = "ok" if racial_assoc is not None else "no_vocab_match"

                results.append({
                    "decade": decade,
                    "genre": genre,
                    "title": title,
                    "artist": artist,
                    "racial_name_association": racial_assoc,
                    "weat_effect_size": baseline_effect,
                    "status": status,
                })

    print(f"\nSaving results to {OUTPUT_FILE}")
    fieldnames = [
        "decade", "genre", "title", "artist", 
        "racial_name_association", "weat_effect_size", "status"
    ]
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print("Done!")

if __name__ == "__main__":
    run_analysis()
