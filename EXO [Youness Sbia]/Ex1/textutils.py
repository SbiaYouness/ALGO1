import string

def clean_text(text:str)->str:
    cleanedtext=''.join(char.lower() for char in text if char not in string.punctuation)
    cleanedtext2=[word.strip() for word in cleanedtext.split()]
    return " ".join(cleanedtext2)

def count_words(text:str)->str:
    return len(text.split())


cleaned=clean_text("Hello World!")
print(count_words(cleaned))


def most_common_words(text:str,top=5):
    freq={} #dict
    mots=clean_text(text).split()
    for mot in mots:
        if mot in freq:
            freq[mot]+=1
        else:
            freq[mot]=1
    
    l= list(freq.items()) # [(,),(,),...]
    l.sort(key=lambda x: x[1], reverse=True) #sort doesnt return anything it changes the current list
    return [x[0] for x in l][:top]


print(most_common_words("hello world! world wo W g g D o l"))

def save_report(filename:str, content:str):
    cleaned = clean_text(content)
    word_count = count_words(cleaned)
    top_words = most_common_words(cleaned, 5)
    with open(filename, 'w') as file:
        file.write(f"Nombre de mots: {word_count}\n\n")
        file.write(f"Top 5 mots les plus frequents:{top_words}\n")
        file.write(f"\nTexte nettoye:\n{cleaned}\n")

save_report(r"report.txt",
            "hello world! world wo W g g D o l")