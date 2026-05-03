import json
import pickle
import re

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

def tokenize_lyrics(lyrics_text):
    text = lyrics_text.lower()
    words = re.findall(r'[a-z]+', text)
    content_words = [w for w in words if w not in STOPWORDS and len(w) > 2]
    return list(set(content_words))

with open('song_lyrics.json', 'r') as f:
    data = json.load(f)

shakira_lyrics = ""
for song in data["2025"]:
    if "Shakira" in song["title"]:
        shakira_lyrics = song["lyrics"]
        break

content_words = tokenize_lyrics(shakira_lyrics)

with open('sgns/1990-vocab.pkl', 'rb') as f:
    vocab = pickle.load(f, encoding='latin1')
vocab_set = set(vocab)

found_words = [w for w in content_words if w in vocab_set]
print("Found 57 Words:", sorted(found_words))

