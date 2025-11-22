import string

def clean_text(text:str)->str:
    cleaned_t= ''.join(char.lower() for char in text if char not in string.punctuation) #punctuation
    list_w=[word.strip() for word in cleaned_t.split()]
    return ' '.join(list_w)

def count_words(text):
    # i=0
    # for _ in clean_text(text).split():
    #     i+=1
    # return i
    return len(clean_text(text).split())

def most_common_words(text,top=5):
    dictw={}
    for word in clean_text(text).split():
        if word in dictw:
            dictw[word]+=1
        else:
            dictw[word]=1

    l=list(dictw.items())
    l.sort(key=lambda x: x[1],reverse=True)
    l2=[x[0] for x in l]
    return l2[:top]
 
def save_report(filename,content):
    with open(filename,'w') as f:
        f.write(f"nombre de mots: {count_words(content)}\n")
        f.write(f"top 5 mots:\n")
        i=0
        for word in most_common_words(content):
            i+=1
            f.write(f"N{i} => {word}\n")
        
        f.write(f"texte nettoye:\n{clean_text(content)}")
