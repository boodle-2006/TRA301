import json
import os
import time
import re
import lyricsgenius

GENIUS_TOKEN = "qekkGUMcGV3kSIY2sSmPl8R4Fi32I8JzWfDJyCGFcBzd-zXJ0NKFMQYZHurDg-6-"

TOP_SONGS = {
    1900: [
        ("Haydn Quartet", "In the Good Old Summertime"),
        ("Billy Murray", "Give My Regards to Broadway"),
        ("Billy Murray", "Yankee Doodle Boy"),
        ("Billy Murray", "You're a Grand Old Flag"),
        ("Haydn Quartet", "Take Me Out to the Ball Game"),
        ("Harry MacDonough", "Shine On Harvest Moon"),
        ("Arthur Collins", "Bill Bailey Won't You Please Come Home"),
        ("Haydn Quartet", "Sweet Adeline"),
        ("Billy Murray", "Meet Me in St. Louis Louis"),
        ("Scott Joplin", "The Entertainer"),
    ],
    1910: [
        ("Arthur Collins", "Alexander's Ragtime Band"),
        ("Peerless Quartet", "Let Me Call You Sweetheart"),
        ("Al Jolson", "You Made Me Love You"),
        ("American Quartet", "Over There"),
        ("Billy Murray", "By the Light of the Silvery Moon"),
        ("American Quartet", "Moonlight Bay"),
        ("Original Dixieland Jazz Band", "Tiger Rag"),
        ("Sophie Tucker", "Some of These Days"),
        ("Marion Harris", "After You've Gone"),
        ("Al Jolson", "Rock-a-Bye Your Baby with a Dixie Melody"),
    ],
    1920: [
        ("Al Jolson", "Swanee"),
        ("Bessie Smith", "St. Louis Blues"),
        ("Gene Austin", "My Blue Heaven"),
        ("Fats Waller", "Ain't Misbehavin'"),
        ("Paul Whiteman", "Whispering"),
        ("Al Jolson", "April Showers"),
        ("Marion Harris", "Tea for Two"),
        ("Vernon Dalhart", "The Prisoner's Song"),
        ("Ben Selvin", "Dardanella"),
        ("Isham Jones", "It Had to Be You"),
    ],
    1930: [
        ("Judy Garland", "Over the Rainbow"),
        ("Glenn Miller", "In the Mood"),
        ("Fred Astaire", "Night and Day"),
        ("Fred Astaire", "Cheek to Cheek"),
        ("Artie Shaw", "Begin the Beguine"),
        ("Ethel Waters", "Stormy Weather"),
        ("Fred Astaire", "The Way You Look Tonight"),
        ("Bing Crosby", "Silent Night"),
        ("Ella Fitzgerald", "A-Tisket A-Tasket"),
        ("Tommy Dorsey", "All the Things You Are"),
    ],
    1940: [
        ("Bing Crosby", "White Christmas"),
        ("Frank Sinatra", "I'll Never Smile Again"),
        ("The Andrews Sisters", "Boogie Woogie Bugle Boy"),
        ("Nat King Cole", "Nature Boy"),
        ("Vera Lynn", "We'll Meet Again"),
        ("The Ink Spots", "If I Didn't Care"),
        ("Glenn Miller", "Chattanooga Choo Choo"),
        ("Bing Crosby", "Swinging on a Star"),
        ("Doris Day", "Sentimental Journey"),
        ("Frank Sinatra", "All or Nothing at All"),
    ],
    1950: [
        ("Bill Haley & His Comets", "Rock Around the Clock"),
        ("Elvis Presley", "Heartbreak Hotel"),
        ("Bobby Darin", "Mack the Knife"),
        ("Chuck Berry", "Johnny B. Goode"),
        ("Elvis Presley", "Hound Dog"),
        ("Little Richard", "Tutti Frutti"),
        ("The Platters", "The Great Pretender"),
        ("Fats Domino", "Blueberry Hill"),
        ("Buddy Holly", "Peggy Sue"),
        ("Ray Charles", "I Got a Woman"),
    ],
    1960: [
        ("The Beatles", "Hey Jude"),
        ("The Rolling Stones", "(I Can't Get No) Satisfaction"),
        ("Aretha Franklin", "Respect"),
        ("Bob Dylan", "Like a Rolling Stone"),
        ("The Beach Boys", "Good Vibrations"),
        ("Marvin Gaye", "I Heard It Through the Grapevine"),
        ("Otis Redding", "(Sittin' On) The Dock of the Bay"),
        ("Simon & Garfunkel", "Bridge Over Troubled Water"),
        ("The Supremes", "Stop! In the Name of Love"),
        ("Sam Cooke", "A Change Is Gonna Come"),
    ],
    1970: [
        ("The Bee Gees", "Stayin' Alive"),
        ("Queen", "Bohemian Rhapsody"),
        ("Fleetwood Mac", "Dreams"),
        ("Led Zeppelin", "Stairway to Heaven"),
        ("Stevie Wonder", "Superstition"),
        ("Eagles", "Hotel California"),
        ("John Lennon", "Imagine"),
        ("Marvin Gaye", "What's Going On"),
        ("Donna Summer", "I Feel Love"),
        ("The Bee Gees", "How Deep Is Your Love"),
    ],
    1980: [
        ("Michael Jackson", "Billie Jean"),
        ("The Police", "Every Breath You Take"),
        ("Bon Jovi", "Livin' on a Prayer"),
        ("Prince", "When Doves Cry"),
        ("Whitney Houston", "I Wanna Dance with Somebody"),
        ("a-ha", "Take On Me"),
        ("Guns N' Roses", "Sweet Child O' Mine"),
        ("Michael Jackson", "Thriller"),
        ("Cyndi Lauper", "Girls Just Want to Have Fun"),
        ("U2", "With or Without You"),
    ],
    1990: [
        ("Bryan Adams", "(Everything I Do) I Do It for You"),
        ("Whitney Houston", "I Will Always Love You"),
        ("Mariah Carey", "One Sweet Day"),
        ("Nirvana", "Smells Like Teen Spirit"),
        ("TLC", "Waterfalls"),
        ("Coolio", "Gangsta's Paradise"),
        ("Backstreet Boys", "I Want It That Way"),
        ("Alanis Morissette", "You Oughta Know"),
        ("Celine Dion", "My Heart Will Go On"),
        ("R. Kelly", "I Believe I Can Fly"),
    ],
    2000: [
        ("Faith Hill", "Breathe"),
        ("Santana", "Smooth"),
        ("Eminem", "The Real Slim Shady"),
        ("Destiny's Child", "Say My Name"),
        ("N'Sync", "Bye Bye Bye"),
        ("Macy Gray", "I Try"),
        ("Sisqo", "Thong Song"),
        ("Coldplay", "Yellow"),
        ("Britney Spears", "Oops!... I Did It Again"),
        ("Outkast", "Ms. Jackson"),
    ],
    2005: [
        ("Mariah Carey", "We Belong Together"),
        ("Gwen Stefani", "Hollaback Girl"),
        ("Mario", "Let Me Love You"),
        ("Kelly Clarkson", "Since U Been Gone"),
        ("Kanye West", "Gold Digger"),
        ("Green Day", "Boulevard of Broken Dreams"),
        ("The Killers", "Mr. Brightside"),
        ("50 Cent", "Candy Shop"),
        ("Gorillaz", "Feel Good Inc."),
        ("Rihanna", "Pon de Replay"),
    ],
    2010: [
        ("Ke$ha", "TiK ToK"),
        ("Eminem", "Love the Way You Lie"),
        ("Katy Perry", "California Gurls"),
        ("Usher", "OMG"),
        ("B.o.B", "Airplanes"),
        ("Train", "Hey, Soul Sister"),
        ("Taio Cruz", "Dynamite"),
        ("Lady Gaga", "Bad Romance"),
        ("Justin Bieber", "Baby"),
        ("Bruno Mars", "Just the Way You Are"),
    ],
    2015: [
        ("Mark Ronson", "Uptown Funk"),
        ("Ed Sheeran", "Thinking Out Loud"),
        ("Wiz Khalifa", "See You Again"),
        ("The Weeknd", "The Hills"),
        ("Omi", "Cheerleader"),
        ("Fetty Wap", "Trap Queen"),
        ("Justin Bieber", "Sorry"),
        ("Adele", "Hello"),
        ("Drake", "Hotline Bling"),
        ("Silo", "Watch Me (Whip/Nae Nae)"),
    ],
    2020: [
        ("The Weeknd", "Blinding Lights"),
        ("Post Malone", "Circles"),
        ("Roddy Ricch", "The Box"),
        ("Dua Lipa", "Don't Start Now"),
        ("DaBaby", "ROCKSTAR"),
        ("Harry Styles", "Watermelon Sugar"),
        ("Billie Eilish", "bad guy"),
        ("Megan Thee Stallion", "Savage Remix"),
        ("Cardi B", "WAP"),
        ("Doja Cat", "Say So"),
    ],
    2025: [
        ("Miley Cyrus", "Flowers"),
        ("Morgan Wallen", "Last Night"),
        ("SZA", "Kill Bill"),
        ("Taylor Swift", "Anti-Hero"),
        ("Rema", "Calm Down"),
        ("PinkPantheress", "Boy's a Liar Pt. 2"),
        ("Drake", "Rich Flex"),
        ("Ice Spice", "Munch (Feelin' U)"),
        ("The Weeknd", "Die For You"),
        ("Bizarrap", "Shakira: Bzrp Music Sessions, Vol. 53"),
    ],
}



def clean_lyrics(lyrics_text):
    if not lyrics_text:
        return ""
    lines = lyrics_text.split('\n')
    cleaned_lines = []
    for line in lines:
        if re.match(r'^\d*Embed$', line.strip()):
            continue
        if 'Contributors' in line and 'Translations' in line:
            continue
        if line.strip().startswith('You might also like'):
            continue
        cleaned_lines.append(line)

    text = '\n'.join(cleaned_lines)

    text = re.sub(r'\[.*?\]', '', text)

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text


def fetch_all_lyrics(output_file="song_lyrics.json"):

    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing = json.load(f)
        print(f"Found existing {output_file} with {sum(len(v) for v in existing.values())} songs.")
        print("Delete it to re-fetch, or we'll only fetch missing songs.")
    else:
        existing = {}

    # Initialize Genius client
    genius = lyricsgenius.Genius(
        GENIUS_TOKEN,
        verbose=False,
        remove_section_headers=True,
        skip_non_songs=True,
        retries=3,
        timeout=15,
    )

    results = existing.copy()

    for decade, songs in sorted(TOP_SONGS.items()):
        decade_key = str(decade)
        if decade_key not in results:
            results[decade_key] = []
        existing_titles = {s["title"].lower() for s in results[decade_key]}

        print(f"\n{'='*60}")
        print(f"  Decade: {decade}s")
        print(f"{'='*60}")

        for i, (artist, title) in enumerate(songs):
            if title.lower() in existing_titles:
                print(f"  [{i+1}/10] {title} — already cached")
                continue

            print(f"  [{i+1}/10] Fetching: {artist} - {title}...", end=" ")

            try:
                song = genius.search_song(title, artist)
                if song and song.lyrics:
                    cleaned = clean_lyrics(song.lyrics)
                    word_count = len(cleaned.split())
                    results[decade_key].append({
                        "artist": artist,
                        "title": title,
                        "lyrics": cleaned,
                        "word_count": word_count,
                        "genius_title": song.title,
                        "genius_artist": song.artist,
                    })
                    print(f"✓ ({word_count} words)")
                else:
                    print("✗ (not found)")
                    results[decade_key].append({
                        "artist": artist,
                        "title": title,
                        "lyrics": "",
                        "word_count": 0,
                        "genius_title": None,
                        "genius_artist": None,
                        "error": "not_found",
                    })
            except Exception as e:
                print(f"✗ (error: {e})")
                results[decade_key].append({
                    "artist": artist,
                    "title": title,
                    "lyrics": "",
                    "word_count": 0,
                    "genius_title": None,
                    "genius_artist": None,
                    "error": str(e),
                })
            time.sleep(1.5)

        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"  → Saved progress to {output_file}")
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    total_songs = 0
    total_with_lyrics = 0
    for decade_key in sorted(results.keys()):
        songs = results[decade_key]
        with_lyrics = sum(1 for s in songs if s["word_count"] > 0)
        total_songs += len(songs)
        total_with_lyrics += with_lyrics
        print(f"  {decade_key}s: {with_lyrics}/{len(songs)} songs with lyrics")

    print(f"\n  Total: {total_with_lyrics}/{total_songs} songs with lyrics")
    print(f"  Saved to: {output_file}")


if __name__ == "__main__":
    fetch_all_lyrics()
