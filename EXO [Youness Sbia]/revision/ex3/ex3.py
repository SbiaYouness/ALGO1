from pathlib import Path
import string
import unicodedata

def list_text_files(directory:Path)->list[Path]:
    listf=[]
    for file in directory.iterdir:
        if file.is_file() and file.suffix=='.txt':
            listf.append(file)
    
    return sorted(listf)  

dirc= Path(__file__).parent
text_files=list_text_files(dirc)

occ={}

unique_words_all=set()
for filep in text_files:
    with open(filep,'rt') as file:
        data=file.read()
        lowered = data.lower()
        decomposed= unicodedata.normalize("NFD", lowered)
        no_accents=''.join(ch for ch in decomposed if unicodedata.category(ch)!='Mn')
        cleanedtext=''.join(ch.lower for ch in no_accents if ch not in string.punctuation)
        for word in cleanedtext.split():
            if word in occ:
                occ[word]+=1
            else:
                occ[word]=1
        unique_words = {word for word in cleanedtext.split() if word}
        unique_words_all.update(unique_words) #extend for list does same, ADDS THE VALUES TO THE LIST ONE BY ONE

with open(dirc/'glossary.txt','wt') as f3:
    for word in unique_words_all:
        f3.write(f"{word}:{occ[word]}\n")