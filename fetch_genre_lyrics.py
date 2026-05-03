import lyricsgenius
import json
import os
import time

GENIUS_API_TOKEN = "qekkGUMcGV3kSIY2sSmPl8R4Fi32I8JzWfDJyCGFcBzd-zXJ0NKFMQYZHurDg-6-"
OUTPUT_FILE = "genre_lyrics.json"

GENRE_SONGS = {
    1950: {
        "Pop": [
            ("Patti Page", "Tennessee Waltz"), ("Les Paul & Mary Ford", "How High the Moon"), 
            ("Rosemary Clooney", "Come On-a My House"), ("Jo Stafford", "You Belong to Me"),
            ("Percy Faith", "The Song from Moulin Rouge"), ("Dean Martin", "Memories Are Made of This"),
            ("Perry Como", "Catch a Falling Star"), ("Doris Day", "Whatever Will Be, Will Be"),
            ("Frank Sinatra", "I've Got You Under My Skin"), ("Nat King Cole", "Mona Lisa")
        ],
        "Rock": [
            ("Bill Haley & His Comets", "Rock Around the Clock"), ("Elvis Presley", "Hound Dog"),
            ("Chuck Berry", "Johnny B. Goode"), ("Little Richard", "Tutti Frutti"),
            ("Jerry Lee Lewis", "Great Balls of Fire"), ("Buddy Holly", "Peggy Sue"),
            ("Fats Domino", "Blueberry Hill"), ("The Everly Brothers", "Wake Up Little Susie"),
            ("Eddie Cochran", "Summertime Blues"), ("Gene Vincent", "Be-Bop-A-Lula")
        ],
        "R&B/Soul": [
            ("Ray Charles", "I Got a Woman"), ("Fats Domino", "Ain't That a Shame"),
            ("The Platters", "The Great Pretender"), ("The Drifters", "There Goes My Baby"),
            ("Sam Cooke", "You Send Me"), ("Clyde McPhatter", "A Lover's Question"),
            ("Ruth Brown", "Teardrops from My Eyes"), ("Big Joe Turner", "Shake, Rattle and Roll"),
            ("James Brown", "Please, Please, Please"), ("Jackie Wilson", "Lonely Teardrops")
        ],
        "Country": [
            ("Hank Williams", "Your Cheatin' Heart"), ("Johnny Cash", "I Walk the Line"),
            ("Kitty Wells", "It Wasn't God Who Made Honky Tonk Angels"), ("Webb Pierce", "There Stands the Glass"),
            ("Marty Robbins", "El Paso"), ("Faron Young", "Live Fast, Love Hard, Die Young"),
            ("Ray Price", "Crazy Arms"), ("Patsy Cline", "Walkin' After Midnight"),
            ("Eddy Arnold", "The Cattle Call"), ("Hank Snow", "I'm Moving On")
        ],
        "Hip-Hop": []
    },
    1960: {
        "Pop": [
            ("The Beatles", "Hey Jude"), ("The Monkees", "I'm a Believer"),
            ("Simon & Garfunkel", "The Sound of Silence"), ("The Beach Boys", "Good Vibrations"),
            ("The Archies", "Sugar, Sugar"), ("Frank Sinatra", "Strangers in the Night"),
            ("Tom Jones", "It's Not Unusual"), ("Dusty Springfield", "Son of a Preacher Man"),
            ("Neil Diamond", "Sweet Caroline"), ("The Association", "Windy")
        ],
        "Rock": [
            ("The Rolling Stones", "(I Can't Get No) Satisfaction"), ("Bob Dylan", "Like a Rolling Stone"),
            ("The Jimi Hendrix Experience", "Purple Haze"), ("The Who", "My Generation"),
            ("The Doors", "Light My Fire"), ("The Animals", "House of the Rising Sun"),
            ("Cream", "Sunshine of Your Love"), ("Led Zeppelin", "Whole Lotta Love"),
            ("Steppenwolf", "Born to Be Wild"), ("The Kinks", "You Really Got Me")
        ],
        "R&B/Soul": [
            ("Aretha Franklin", "Respect"), ("Marvin Gaye", "I Heard It Through the Grapevine"),
            ("Otis Redding", "(Sittin' On) The Dock of the Bay"), ("The Supremes", "Stop! In the Name of Love"),
            ("The Temptations", "My Girl"), ("James Brown", "I Got You (I Feel Good)"),
            ("Smokey Robinson", "The Tracks of My Tears"), ("Sam & Dave", "Soul Man"),
            ("Four Tops", "Reach Out I'll Be There"), ("Martha and the Vandellas", "Dancing in the Street")
        ],
        "Country": [
            ("Patsy Cline", "Crazy"), ("Johnny Cash", "Ring of Fire"),
            ("Loretta Lynn", "Don't Come Home A-Drinkin'"), ("Merle Haggard", "Mama Tried"),
            ("Tammy Wynette", "Stand by Your Man"), ("Buck Owens", "I've Got a Tiger By the Tail"),
            ("George Jones", "She Thinks I Still Care"), ("Jim Reeves", "He'll Have to Go"),
            ("Charley Pride", "Kiss an Angel Good Mornin'"), ("Roger Miller", "King of the Road")
        ],
        "Hip-Hop": []
    },
    1970: {
        "Pop": [
            ("Elton John", "Your Song"), ("The Bee Gees", "Stayin' Alive"),
            ("ABBA", "Dancing Queen"), ("Carpenters", "Close to You"),
            ("Olivia Newton-John", "You're the One That I Want"), ("Rod Stewart", "Maggie May"),
            ("Roberta Flack", "Killing Me Softly with His Song"), ("Carly Simon", "You're So Vain"),
            ("Barbra Streisand", "The Way We Were"), ("Eagles", "Hotel California")
        ],
        "Rock": [
            ("Led Zeppelin", "Stairway to Heaven"), ("Queen", "Bohemian Rhapsody"),
            ("Pink Floyd", "Another Brick in the Wall, Pt. 2"), ("Fleetwood Mac", "Go Your Own Way"),
            ("The Rolling Stones", "Brown Sugar"), ("Aerosmith", "Dream On"),
            ("Bruce Springsteen", "Born to Run"), ("Black Sabbath", "Paranoid"),
            ("David Bowie", "Starman"), ("The Who", "Baba O'Riley")
        ],
        "R&B/Soul": [
            ("Stevie Wonder", "Superstition"), ("Marvin Gaye", "What's Going On"),
            ("Earth, Wind & Fire", "September"), ("Al Green", "Let's Stay Together"),
            ("Donna Summer", "I Feel Love"), ("Diana Ross", "Ain't No Mountain High Enough"),
            ("Curtis Mayfield", "Move On Up"), ("Sly & The Family Stone", "Family Affair"),
            ("Kool & The Gang", "Jungle Boogie"), ("The O'Jays", "Love Train")
        ],
        "Country": [
            ("Dolly Parton", "Jolene"), ("Willie Nelson", "Blue Eyes Crying in the Rain"),
            ("Waylon Jennings", "Mammas Don't Let Your Babies Grow Up to Be Cowboys"), ("John Denver", "Take Me Home, Country Roads"),
            ("Kenny Rogers", "The Gambler"), ("Loretta Lynn", "Coal Miner's Daughter"),
            ("Charlie Rich", "The Most Beautiful Girl"), ("Conway Twitty", "Hello Darlin'"),
            ("Tanya Tucker", "Delta Dawn"), ("Ronnie Milsap", "It Was Almost Like a Song")
        ],
        "Hip-Hop": []
    },
    1980: {
        "Pop": [
            ("Michael Jackson", "Billie Jean"), ("Madonna", "Like a Virgin"),
            ("Whitney Houston", "I Wanna Dance with Somebody"), ("Prince", "When Doves Cry"),
            ("George Michael", "Faith"), ("Cyndi Lauper", "Girls Just Want to Have Fun"),
            ("A-ha", "Take On Me"), ("Rick Astley", "Never Gonna Give You Up"),
            ("The Police", "Every Breath You Take"), ("Culture Club", "Karma Chameleon")
        ],
        "Rock": [
            ("Guns N' Roses", "Sweet Child O' Mine"), ("Bon Jovi", "Livin' on a Prayer"),
            ("AC/DC", "Back In Black"), ("Def Leppard", "Pour Some Sugar on Me"),
            ("Journey", "Don't Stop Believin'"), ("Van Halen", "Jump"),
            ("U2", "With or Without You"), ("Dire Straits", "Money for Nothing"),
            ("The Clash", "Should I Stay or Should I Go"), ("Bruce Springsteen", "Born in the U.S.A.")
        ],
        "R&B/Soul": [
            ("Rick James", "Super Freak"), ("Lionel Richie", "All Night Long"),
            ("Diana Ross", "I'm Coming Out"), ("Luther Vandross", "Never Too Much"),
            ("Kool & The Gang", "Celebration"), ("Chaka Khan", "I Feel for You"),
            ("Earth, Wind & Fire", "Let's Groove"), ("Marvin Gaye", "Sexual Healing"),
            ("Anita Baker", "Sweet Love"), ("Stevie Wonder", "Part-Time Lover")
        ],
        "Country": [
            ("George Strait", "Amarillo by Morning"), ("Randy Travis", "Forever and Ever, Amen"),
            ("Dolly Parton", "9 to 5"), ("Kenny Rogers", "Lady"),
            ("Reba McEntire", "Whoever's in New England"), ("The Judds", "Grandpa (Tell Me 'Bout the Good Old Days)"),
            ("Hank Williams Jr.", "A Country Boy Can Survive"), ("Alan Jackson", "Here in the Real World"),
            ("Garth Brooks", "The Dance"), ("Clint Black", "Killin' Time")
        ],
        "Hip-Hop": [
            ("Grandmaster Flash", "The Message"), ("Run-D.M.C.", "Walk This Way"),
            ("Sugarhill Gang", "Rapper's Delight"), ("Public Enemy", "Fight the Power"),
            ("N.W.A.", "Straight Outta Compton"), ("LL Cool J", "I Need Love"),
            ("Salt-N-Pepa", "Push It"), ("Slick Rick", "Children's Story"),
            ("Eric B. & Rakim", "Paid in Full"), ("Beastie Boys", "(You Gotta) Fight for Your Right (To Party!)")
        ]
    },
    1990: {
        "Pop": [
            ("Britney Spears", "...Baby One More Time"), ("Backstreet Boys", "I Want It That Way"),
            ("Spice Girls", "Wannabe"), ("Celine Dion", "My Heart Will Go On"),
            ("N'Sync", "Tearin' up My Heart"), ("Christina Aguilera", "Genie in a Bottle"),
            ("Mariah Carey", "Fantasy"), ("Ricky Martin", "Livin' la Vida Loca"),
            ("TLC", "Waterfalls"), ("Savage Garden", "Truly Madly Deeply")
        ],
        "Rock": [
            ("Nirvana", "Smells Like Teen Spirit"), ("Pearl Jam", "Alive"),
            ("Oasis", "Wonderwall"), ("Red Hot Chili Peppers", "Under the Bridge"),
            ("Green Day", "Basket Case"), ("Radiohead", "Creep"),
            ("The Smashing Pumpkins", "1979"), ("Metallica", "Enter Sandman"),
            ("Foo Fighters", "Everlong"), ("Blink-182", "All the Small Things")
        ],
        "R&B/Soul": [
            ("Boyz II Men", "End of the Road"), ("Whitney Houston", "I Will Always Love You"),
            ("TLC", "No Scrubs"), ("Destiny's Child", "Say My Name"),
            ("Mariah Carey", "Always Be My Baby"), ("Lauryn Hill", "Doo Wop (That Thing)"),
            ("R. Kelly", "I Believe I Can Fly"), ("Toni Braxton", "Un-Break My Heart"),
            ("Aaliyah", "Are You That Somebody?"), ("En Vogue", "My Lovin' (You're Never Gonna Get It)")
        ],
        "Country": [
            ("Garth Brooks", "Friends in Low Places"), ("Shania Twain", "Man! I Feel Like a Woman!"),
            ("Tim McGraw", "Don't Take the Girl"), ("George Strait", "Carrying Your Love with Me"),
            ("Alan Jackson", "Chattahoochee"), ("Faith Hill", "This Kiss"),
            ("Brooks & Dunn", "Boot Scootin' Boogie"), ("Dixie Chicks", "Wide Open Spaces"),
            ("Martina McBride", "Independence Day"), ("Vince Gill", "I Still Believe in You")
        ],
        "Hip-Hop": [
            ("2Pac", "California Love"), ("The Notorious B.I.G.", "Juicy"),
            ("Dr. Dre", "Nuthin' but a 'G' Thang"), ("Snoop Dogg", "Gin and Juice"),
            ("Coolio", "Gangsta's Paradise"), ("Wu-Tang Clan", "C.R.E.A.M."),
            ("Nas", "N.Y. State of Mind"), ("Eminem", "My Name Is"),
            ("Jay-Z", "Hard Knock Life"), ("Outkast", "Rosa Parks")
        ]
    },
    2000: {
        "Pop": [
            ("Kelly Clarkson", "Since U Been Gone"), ("Lady Gaga", "Poker Face"),
            ("Rihanna", "Umbrella"), ("Justin Timberlake", "Cry Me a River"),
            ("Katy Perry", "I Kissed a Girl"), ("Coldplay", "Viva La Vida"),
            ("Beyoncé", "Crazy in Love"), ("Shakira", "Hips Don't Lie"),
            ("Avril Lavigne", "Complicated"), ("Black Eyed Peas", "I Gotta Feeling")
        ],
        "Rock": [
            ("The Killers", "Mr. Brightside"), ("Linkin Park", "In the End"),
            ("Green Day", "Boulevard of Broken Dreams"), ("The White Stripes", "Seven Nation Army"),
            ("Kings of Leon", "Sex on Fire"), ("Foo Fighters", "Best of You"),
            ("Evanescence", "Bring Me to Life"), ("Fall Out Boy", "Sugar, We're Goin Down"),
            ("My Chemical Romance", "Welcome to the Black Parade"), ("Red Hot Chili Peppers", "Californication")
        ],
        "R&B/Soul": [
            ("Alicia Keys", "Fallin'"), ("Usher", "Yeah!"),
            ("Mario", "Let Me Love You"), ("Beyoncé", "Irreplaceable"),
            ("Ne-Yo", "So Sick"), ("John Legend", "Ordinary People"),
            ("Mary J. Blige", "Family Affair"), ("Aaliyah", "Try Again"),
            ("Destiny's Child", "Survivor"), ("Chris Brown", "Run It!")
        ],
        "Country": [
            ("Carrie Underwood", "Before He Cheats"), ("Taylor Swift", "Love Story"),
            ("Brad Paisley", "Whiskey Lullaby"), ("Kenny Chesney", "The Good Stuff"),
            ("Toby Keith", "Courtesy of the Red, White and Blue"), ("Zac Brown Band", "Chicken Fried"),
            ("Tim McGraw", "Live Like You Were Dying"), ("Dixie Chicks", "Not Ready to Make Nice"),
            ("Rascal Flatts", "What Hurts the Most"), ("Keith Urban", "Somebody Like You")
        ],
        "Hip-Hop": [
            ("Eminem", "Lose Yourself"), ("50 Cent", "In Da Club"),
            ("Outkast", "Hey Ya!"), ("Kanye West", "Gold Digger"),
            ("Jay-Z", "99 Problems"), ("Snoop Dogg", "Drop It Like It's Hot"),
            ("T.I.", "Whatever You Like"), ("Lil Wayne", "A Milli"),
            ("Nelly", "Hot In Herre"), ("Missy Elliott", "Get Ur Freak On")
        ]
    },
    2010: {
        "Pop": [
            ("Adele", "Rolling in the Deep"), ("Ed Sheeran", "Shape of You"),
            ("Mark Ronson", "Uptown Funk"), ("Taylor Swift", "Blank Space"),
            ("Justin Bieber", "Sorry"), ("Katy Perry", "Roar"),
            ("Pharrell Williams", "Happy"), ("Ariana Grande", "thank u, next"),
            ("Sia", "Chandelier"), ("Dua Lipa", "New Rules")
        ],
        "Rock": [
            ("Arctic Monkeys", "Do I Wanna Know?"), ("Imagine Dragons", "Radioactive"),
            ("Twenty One Pilots", "Stressed Out"), ("The Black Keys", "Lonely Boy"),
            ("Hozier", "Take Me to Church"), ("Paramore", "Ain't It Fun"),
            ("Foo Fighters", "Walk"), ("Mumford & Sons", "I Will Wait"),
            ("Panic! At The Disco", "High Hopes"), ("Muse", "Madness")
        ],
        "R&B/Soul": [
            ("The Weeknd", "Can't Feel My Face"), ("Bruno Mars", "That's What I Like"),
            ("Frank Ocean", "Thinkin Bout You"), ("Childish Gambino", "Redbone"),
            ("SZA", "The Weekend"), ("Daniel Caesar", "Get You"),
            ("Miguel", "Adorn"), ("Beyoncé", "Formation"),
            ("Khalid", "Location"), ("Rihanna", "Needed Me")
        ],
        "Country": [
            ("Florida Georgia Line", "Cruise"), ("Luke Bryan", "Play It Again"),
            ("Sam Hunt", "Body Like a Back Road"), ("Chris Stapleton", "Tennessee Whiskey"),
            ("Kacey Musgraves", "Follow Your Arrow"), ("Jason Aldean", "Dirt Road Anthem"),
            ("Thomas Rhett", "Die a Happy Man"), ("Miranda Lambert", "The House That Built Me"),
            ("Eric Church", "Springsteen"), ("Little Big Town", "Girl Crush")
        ],
        "Hip-Hop": [
            ("Drake", "God's Plan"), ("Kendrick Lamar", "HUMBLE."),
            ("Kanye West", "POWER"), ("Future", "Mask Off"),
            ("Migos", "Bad and Boujee"), ("Cardi B", "Bodak Yellow"),
            ("Post Malone", "rockstar"), ("Travis Scott", "SICKO MODE"),
            ("J. Cole", "No Role Modelz"), ("Lil Uzi Vert", "XO Tour Llif3")
        ]
    },
    2020: {
        "Pop": [
            ("The Weeknd", "Blinding Lights"), ("Dua Lipa", "Levitating"),
            ("Harry Styles", "As It Was"), ("Olivia Rodrigo", "drivers license"),
            ("Taylor Swift", "Anti-Hero"), ("Miley Cyrus", "Flowers"),
            ("Billie Eilish", "bad guy"), ("Doja Cat", "Say So"),
            ("Glass Animals", "Heat Waves"), ("Ed Sheeran", "Bad Habits")
        ],
        "Rock": [
            ("Måneskin", "Beggin'"), ("Machine Gun Kelly", "my ex's best friend"),
            ("Linkin Park", "Lost"), ("Paramore", "This Is Why"),
            ("Bring Me The Horizon", "Teardrops"), ("YUNGBLUD", "fleabag"),
            ("Foo Fighters", "Rescued"), ("Blink-182", "EDGING"),
            ("Greta Van Fleet", "Heat Above"), ("Falling In Reverse", "Popular Monster")
        ],
        "R&B/Soul": [
            ("SZA", "Kill Bill"), ("Silk Sonic", "Leave the Door Open"),
            ("Giveon", "Heartbreak Anniversary"), ("Steve Lacy", "Bad Habit"),
            ("The Weeknd", "Save Your Tears"), ("Chloe x Halle", "Do It"),
            ("Brent Faiyaz", "Wasting Time"), ("Victoria Monét", "On My Mama"),
            ("Jazmine Sullivan", "Pick Up Your Feelings"), ("Daniel Caesar", "Always")
        ],
        "Country": [
            ("Morgan Wallen", "Last Night"), ("Luke Combs", "Fast Car"),
            ("Zach Bryan", "Something in the Orange"), ("Lainey Wilson", "Heart Like A Truck"),
            ("Bailey Zimmerman", "Rock and A Hard Place"), ("Chris Stapleton", "White Horse"),
            ("Jelly Roll", "Need A Favor"), ("Kane Brown", "Thank God"),
            ("Cody Johnson", "'Til You Can't"), ("Cole Swindell", "She Had Me At Heads Carolina")
        ],
        "Hip-Hop": [
            ("Jack Harlow", "First Class"), ("Drake", "Rich Flex"),
            ("Future", "Wait For U"), ("Gunna", "fukumean"),
            ("Lil Baby", "The Bigger Picture"), ("Cardi B", "WAP"),
            ("Megan Thee Stallion", "Savage Remix"), ("Ice Spice", "Munch (Feelin' U)"),
            ("Lil Nas X", "INDUSTRY BABY"), ("Kendrick Lamar", "N95")
        ]
    }
}

def fetch_lyrics():
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN, timeout=15, retries=3)
    genius.remove_section_headers = True

    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            all_lyrics = json.load(f)
    else:
        all_lyrics = {}

    for decade, genres in GENRE_SONGS.items():
        decade_str = str(decade)
        if decade_str not in all_lyrics:
            all_lyrics[decade_str] = {}

        print(f"\n{'='*60}\n  Decade: {decade}s\n{'='*60}")
        
        for genre, songs in genres.items():
            if genre not in all_lyrics[decade_str]:
                all_lyrics[decade_str][genre] = []
                
            print(f"\n  --- Genre: {genre} ---")
            
            # Identify already fetched songs for this genre
            fetched_titles = [s["title"].lower() for s in all_lyrics[decade_str][genre]]
            
            for i, (artist, title) in enumerate(songs):
                if title.lower() in fetched_titles:
                    print(f"  [{i+1}/{len(songs)}] {title} — already cached")
                    continue
                    
                print(f"  [{i+1}/{len(songs)}] Fetching: {artist} - {title}...", end=" ", flush=True)
                
                try:
                    song = genius.search_song(title, artist)
                    if song and song.lyrics:
                        # Clean lyrics
                        raw_lyrics = song.lyrics
                        if "Lyrics" in raw_lyrics:
                            raw_lyrics = raw_lyrics.split("Lyrics", 1)[1]
                        if raw_lyrics.endswith("Embed"):
                            raw_lyrics = raw_lyrics[:-5]
                        
                        clean_lyrics = raw_lyrics.strip()
                        word_count = len(clean_lyrics.split())
                        
                        all_lyrics[decade_str][genre].append({
                            "title": title,
                            "artist": artist,
                            "lyrics": clean_lyrics,
                            "word_count": word_count
                        })
                        print(f"✓ ({word_count} words)")
                    else:
                        all_lyrics[decade_str][genre].append({
                            "title": title,
                            "artist": artist,
                            "lyrics": None,
                            "word_count": 0
                        })
                        print("✗ (not found)")
                except Exception as e:
                    print(f"✗ (error: {e})")
                    
                # Save progress after every song
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(all_lyrics, f, indent=4)
                    
                time.sleep(1.5)  # Rate limiting

    print("\nFetch complete!")

if __name__ == "__main__":
    fetch_lyrics()
