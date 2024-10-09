# Lyrical Comments

### WARNING: Since these comments are scraped directly off of a YouTube video, these comments may contain offensive/contraversial elements


## How It Works

First, we need to define what exactly makes up a lyric? What structure of lines should we follow to make a lyric?

### What Makes Up A Lyric?

There are many ways to define what makes up the lyrics of a song, however, the common feature among most songs are that the lines should have a rhyme scheme or follow a rhyme.

There's many types of rhyme schemes in literature such as ABAB or ABCABC but this project won't go into that depth. 

This program only composes a basic rhyme scheme in which the previous line will rhyme with the next line. (plus it sound better that way, at least for me personally)

### Determining Rhyme

In this case, we'll define a rhyme as having at least the same last vowel sound and any following consonant sounds.

Ex: Try/Lie or Shape/Cake

Using ```cmudict```, we can break down these words into phonemes (their pronunciations)

```
'try' = /T R AY1/
'lie' = /L AY1/
```

```
'shape' = /SH EY1 P/
'cake' = /K EY1 K/
```

For try/lie, because the last vowel sounds (AY1) are matching, try/lie rhyme. Same goes for shape/cake

### How To Determine Rhyme In Code?
1. Extract the last word of a sentence
2. Get the phonemes of the word via cmudict
3. Check if the phonemes of the word match
4. If phonemes match then the words rhyme

### Handling Non-Strict Rhyme

The issue with the previous method of determining rhyme is that the rhyme checking relies on the exact matching of phonemes. However, there are many words that also rhyme that don't necessarily have the same last vowel pronunciation (i.e byte/light)

### How To Solve?

This is going to sound a little trippy but, since fun and one do rhyme and are close in pronunciation and length. We can therefore transform each character in 'byte' to eventually turn it into 'light' in a short amount of transformations.

We can use nltk's ```edit_distance``` function to apply a maximum threshold of transformations that can allow a word to be considered a rhyme. A more relaxed check.








