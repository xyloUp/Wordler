from httpx import get

text = get("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt").text

# selects all words that are 5 characters long and don't contain sybols
filtered = (word.strip() for word in 
    filter(lambda i: len(i) == 5 and all(
        ['.' not in i and '-' not in i and '_' not in i]), 
            text.split("\n")))

with open("words.txt", "w") as f:
    for filtered_word in filtered:
        f.write(f"{filtered_word}\n")