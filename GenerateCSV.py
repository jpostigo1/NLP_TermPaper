import os, random, re
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer


punctuation = ",;.!?"

from microsofttranslator import Translator


'''
from translate import translator
translator('en', 'es', 'Hello World!')

proxy_handler = urllib.request.ProxyHandler({"http" : "http://translate.google.com"})
proxy_opener = urllib.request.build_opener(
    urllib.request.HTTPHandler(proxy_handler),
    urllib.request.HTTPSHandler(proxy_handler))

gs_with_proxy = goslate.Goslate(opener=proxy_opener)
'''

def TranslationTour(txt_file):
    print(txt_file)
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    translator = Translator('jpostigo',
                            '09aJ3SuBVACpmNQv6VWj7FKZaUjGL4GmUyGZxgwo/6E=')

    
    #print(content)
    trans_es = translator.translate(content,'es')
    #trans_fr = translator.translate(trans_es,'fr')
    trans_en = translator.translate(trans_es,'en')

    print(trans_en)
    exit(4)

    #newFp = open(whereToWrite + os.sep + 'trans_obfucated.txt','w')
    #newFp.write(output)
    #newFp.close()




#for synonym replacement
def Replacement(txt_file):
    print(txt_file)
    stops = set(stopwords.words('english')+['I'])
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    token = nltk.word_tokenize(content)
    pos = nltk.pos_tag(token)

    output = ""
    for word, speech in pos:
        if speech == 'JJ':
            syn = wordnet.synsets(word)
            if syn:
                output += ' ' + str(syn[0].lemma_names('eng')[0])
            else:
                output += ' ' + word
        else:
            if(word in punctuation):
                output += word
            else:
                output += ' ' + word

    output = re.sub(r" ''",'"', output)
    output = re.sub(r'`` ', '"' , output)
    output = re.sub(r'\( ', '(', output)
    output = re.sub(r' \)', ')', output)
    output = re.sub(r" '", "'", output)

    newFp = open(whereToWrite + os.sep + 'syn_obfucated.txt','w')
    newFp.write(output)
    newFp.close()
    exit(2) #get rid of this call to obfuscate rest of files.




PATH = os.getcwd() + os.sep + "10auths" + os.sep


#CSV format
    #AA,path_to_file
    #,path_to_file (to classify)

fp = open("leave_one_out.csv", "w")

for folder in os.listdir(PATH):
    file_arr = []
    for file in os.listdir(PATH + os.sep + folder):
        if(not file.split('_')[1].isnumeric()):
            index = random.randint(0, len(file_arr) - 1)
            file_to_classify = file_arr[index]
            #replacement(file_to_classify)
            author = file_to_classify.split('_')[0].split(',')[0]
            path_to_file = os.getcwd() + os.sep + "10auths" + os.sep + author + os.sep + file_to_classify.split(os.sep)[9]
            TranslationTour(path_to_file)
            Replacement(path_to_file)

            new_file = ',' + file_to_classify.split(',')[1]
            file_arr.remove(file_to_classify)
            fp.write(new_file + '\n')
            for f in file_arr:
                fp.write(f + '\n')
            break
        file_name = folder + ',' + PATH + folder + os.sep + file
        file_arr.append(file_name)