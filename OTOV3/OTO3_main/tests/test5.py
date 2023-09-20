from translate import Translator
import threading
import concurrent.futures
from fuzzywuzzy import fuzz
from nltk.corpus import wordnet
import time
language_list = []
spanish = []
english = []
    
def train():
    global language_list
    global spanish
    global english
    file = input("language list file(spanish file) = ")
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    spanish = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        spanish.append(l)
    f.close()
    
    file = input("language list file(english file) = ")
    f = open('trained_models_OTOV3/' + file + '.txt', 'r')
    english = []
    for l in f:
        if ";" in l:
            l = l.replace(';', ",")
        if "\n" in l:
            parts = l.split("\n", 1)
            l = parts[0]
            
        english.append(l)
    f.close()
    
    print(english)
    try:
        upto = 1
        for i in spanish:
            language_list.append([spanish[upto], english[upto]])
            
            upto += 1
    except:
        print("end of list")
        
    for i in language_list:
        print(i)

def translate(i):
    translator = Translator(to_lang="en", from_lang="es")
    translated_text = translator.translate(i[0])
    true_text = i[1]
    true_text_parts = true_text.split(",")
    true_text = true_text_parts[0].strip()
    similarity_ratio = fuzz.ratio(true_text, translated_text)
    return i[0], i[1], translated_text, similarity_ratio

def check_likeness(word1, word2):
    synonyms_word1 = set()
    synonyms_word2 = set()

    for syn in wordnet.synsets(word1):
        for lemma in syn.lemmas():
            synonyms_word1.add(lemma.name())
            
    for syn in wordnet.synsets(word2):
        for lemma in syn.lemmas():
            synonyms_word2.add(lemma.name())

    if synonyms_word1 & synonyms_word2:
        return True
    else:
        return False
    
        
train()
results_translate = []

max_threads = len(spanish)

# Create a thread pool with the specified maximum number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit tasks to the thread pool for each language
    futures = [executor.submit(translate, lang) for lang in language_list]

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

    # Print the results after all tasks have completed
    for future in concurrent.futures.as_completed(futures):
        translated_result = future.result()
        results_translate.append(future.result())

differences = []
for i in results_translate:
    if float(i[3]) < 30:
        differences.append(i)
        
for i in differences:
    print(i)
    if check_likeness(i[1], i[2]) == True:
        pass
    else:
        change = input('a difference has been found do you want to change it to the translated vertion or say the same?(do you want to change Y/N)')
        if change.lower() == 'y':
            print(i[1],i[0],i[2],i[0])
            english.remove(i[1])
            spanish.remove(i[0])
            english.append(i[2])
            spanish.append(i[0])

language_list = []
try:
    upto = 1
    for i in spanish:
        language_list.append([spanish[upto], english[upto]])
        
        upto += 1
except:
    print("end of list")
    
for i in language_list:
    print(i)



