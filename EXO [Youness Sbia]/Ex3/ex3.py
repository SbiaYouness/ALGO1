from pathlib import Path
import string
import unicodedata

def list_text_files(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.txt"))

current_dir = Path(__file__).parent #current directory
text_files = list_text_files(current_dir)

occ={}
unique_words_all=set()
for file_path in text_files:
    with open(file_path,'rt') as file:
        data=file.read()
        lowered = data.lower()
        decomposed = unicodedata.normalize("NFD", lowered)
        no_accents = ''.join(ch for ch in decomposed if unicodedata.category(ch) != 'Mn')
        cleanedtext=''.join(char.lower() for char in no_accents if char not in string.punctuation)
        for word in cleanedtext.split():
            if word in occ:
                occ[word]+=1
            else:
                occ[word] = 1
        unique_words = {word for word in cleanedtext.split() if word}
        unique_words_all.update(unique_words)  # accumulate across files

with open(current_dir / 'glossary.txt', 'wt') as file2:
    for word in sorted(unique_words_all):
        file2.write(f"{word}:{occ[word]}\n")