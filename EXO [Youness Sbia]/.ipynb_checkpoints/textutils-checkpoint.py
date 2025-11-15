import string

def clean_text(text:str)->str:
    cleanedtext=''.join(char.lower() for char in text if char not in string.punctuation)
    cleanedtext2=[word.strip() for word in cleanedtext.split()]
    return " ".join(cleanedtext2)

def count(text:str)->str:
    return len(text.split())


cleaned=clean_text("Hello World!")
print(count(cleaned))

