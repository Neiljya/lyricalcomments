import nltk
from nltk.corpus import cmudict
from nltk.metrics import edit_distance
import re
from comment_scraper import Comment_Scraper
import json

pronouncing_dict = cmudict.dict()

# Youtube API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = ""
video_id = "tXEPbotEjZE" # KSI's new song

num_comments = 100

##########################SET UP SCRAPER ###################################

comment_scraper = Comment_Scraper(api_service_name=api_service_name,
                                  api_version=api_version,
                                  DEVELOPER_KEY=DEVELOPER_KEY,
                                  video_id=video_id,
                                  num_comments=num_comments
                                  )

#############################################################################

def get_phonemes(word):
    word = word.lower()
    word = re.sub(r'[^a-z]', '', word)

    if word in pronouncing_dict:
        return pronouncing_dict[word][0]
    else:
        return None

def get_last(string):
    # Removes punctuation and splits words into list
    words = re.findall(r'\b\w+\b', string.lower())

    if words:
        return words[-1]
    return '' # or return a blank

# Function to check if two phonetic lists rhyme (strict)
def check_phonetic_rhyme(phonemes1, phonemes2):
    """
    In this case, we'll define something that rhymes as having at least the same
    last vowel sound and any following consonant sounds

    ex: try/lie or shape/cake

    ------------------------------------------------------
    The method of identifying a rhyme in the context of cmudict:
    ------------------------------------------------------

    'try' = /T R AY1/ where the ending vowel sound is AY1
    'lie' = /L AY1/ so the ending vowel sound is also AY1

    Therefore, try/lie rhyme

    'shape' = /SH EY1 P/ where the ending vowel sound is EY1
    'cake' = /K EY1 K/ ending vowel sound is also EY1

    Therefore, shape/cake rhyme
    """

    # Check if the last character in the extracted phoneme is a digit = a vowel sound
    vowels1 = [phoneme for phoneme in phonemes1 if phoneme[-1].isdigit()]
    vowels2 = [phoneme for phoneme in phonemes2 if phoneme[-1].isdigit()]


    if vowels1 and vowels2:
        last_idx1 = phonemes1.index(vowels1[-1])
        last_idx2 = phonemes2.index(vowels2[-1])

        return phonemes1[last_idx1:] == phonemes2[last_idx2:]

    return False


"""
####################################################################################################################################################

    - Due to the way that the main check works, some lyrical rhymes that do not adhere to a strict rhyme format may be interpreted as not rhyming
    
    - The `check_phonetic_rhyme_relax()` method is used to circumvent it a little by checking the minimum amount of transformations needed to turn one string into another
    
    - If the rhymes are close enough within a certain threshold then we can consider it as a rhyme
    
####################################################################################################################################################
"""

def check_phonetic_rhyme_relax(phonemes1, phonemes2, threshold):
    distance = edit_distance(phonemes1, phonemes2)

    return distance <= threshold

def check_string_rhyme(string1, string2, threshold=5):
    last1 = get_last(string1)
    last2 = get_last(string2)

    phonemes1 = get_phonemes(last1)
    phonemes2 = get_phonemes(last2)

    if phonemes1 is None or phonemes2 is None:
        return False

    if check_phonetic_rhyme(phonemes1, phonemes2):
        return True

    return check_phonetic_rhyme_relax(phonemes1, phonemes2, threshold)


# Examples - from Rap God by Eminem
# string1 = "Got a fat knot from that rap profit"
# string2 = "Made a livin' and a killin' off it"
# print(check_string_rhyme(string1, string2))


# Group each comment by rhymes to form its own 'verse'
# The comments are checked by comparisons of 2 comments and if their phonemes 'rhyme' then group them
def group_rhymes(comments):
    rhyme_groups = []
    used = set()

    for i, (commenter1, comment1) in enumerate(comments.items()):
        if i in used:
            continue

        comment1 = clean_comments(comment1)

        print(comment1)

        group = [comment1]
        used.add(i)
        last_word1 = get_last(comment1)
        phonemes1 = get_phonemes(last_word1)

        for j, (commenter2, comment2) in enumerate(comments.items()):
            if j <= i or j in used:
                continue

            last_word2 = get_last(comment2)
            phonemes2 = get_phonemes(last_word2)

            if phonemes1 and phonemes2 and check_phonetic_rhyme(phonemes1, phonemes2):
                group.append(comment2)
                used.add(j)

        if group:
            rhyme_groups.append(group)

    return rhyme_groups

def write_lyrics(rhyme_groups, filename):
    with open(filename, 'w') as f:
        for i, group in enumerate(rhyme_groups):
            f.write(f"Verse {i+1}:\n")
            for line in group:
                f.write(f"{line}\n")
            f.write("\n")

def create_lyrics(data, output_filename="lyricalcomments.txt"):
    rhyme_groups = group_rhymes(data)
    write_lyrics(rhyme_groups, output_filename)

def clean_comments(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

if __name__ == '__main__':
    # Use built-in comment scraper to scrape comments:
    # comments = comment_scraper.get_comments(pull_all=False, pages=1)
    # comment_scraper.export_comments(comments)

    with open("sample.json", "r") as f:
        data = json.load(f)

    create_lyrics(data)













