import os, random, re
import nltk
import time
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer


punctuation = ",;.!?"

# from microsofttranslator import Translator


'''
from translate import translator
translator('en', 'es', 'Hello World!')

proxy_handler = urllib.request.ProxyHandler({"http" : "http://translate.google.com"})
proxy_opener = urllib.request.build_opener(
    urllib.request.HTTPHandler(proxy_handler),
    urllib.request.HTTPSHandler(proxy_handler))

gs_with_proxy = goslate.Goslate(opener=proxy_opener)
'''

'''
#try vietnamese
def TranslationTour(txt_file):
    print(txt_file)
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    translator = Translator('jpostigo',
                            '09aJ3SuBVACpmNQv6VWj7FKZaUjGL4GmUyGZxgwo/6E=')
    translator2 = Translator('lwilliams',
                             'gsNJczFz4VOPBSwyuwWZXYzWx4B0CSuZxgquCPpQggs=')


    #print(content)
    trans_es = translator2.translate(content,'es')
    #trans_fr = translator.translate(trans_es,'fr')
    trans_en = translator2.translate(trans_es,'en')


    sents = nltk.sent_tokenize(content)

    new_trans = ""
    for sent in sents:
        trans_es = translator.translate(sent,'es')
        #trans_fr = translator.translate(trans_es,'fr')
        trans_en = translator.translate(trans_es,'en')
        new_trans += trans_en

    print(new_trans)
    exit(4)

    newFp = open(whereToWrite + os.sep + 'trans_obfucated.txt','w')
    newFp.write(trans_en)
    newFp.close()

'''


#for synonym replacement
def Replacement(txt_file):
    #print(txt_file)
    author = txt_file.split(os.sep)[-2]
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

    output = re.sub(u"\u202d","",output)
    output = re.sub(u"\u202c","",output)
    output = re.sub(u"\u200e","",output)
    output = re.sub(u"\u200f","",output)


    newFp = open(whereToWrite + os.sep + author +'_' + 'syn_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()
    #exit(2) #get rid of this call to obfuscate rest of files.


def genCSVObfuscated(dataDir):
    # Generates CSV files for .run including the obfuscated versions as the unknown styles.

    output_filename = "with_obfuscated_" + str(round(time.time())) + ".csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(dataDir):
        file_arr = []
        for file in os.listdir(dataDir + os.sep + folder):
            author = file.split('_')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + \
                           file.split(os.sep)[-1]
            if file.split('_')[1].isnumeric():
                fp.write(author + "," + path_to_file + "\n")
            elif "syn_obfuscated" in file:
                fp.write("," + path_to_file + "\n")
    fp.close()


PATH = os.getcwd() + os.sep + "15auths" + os.sep

#CSV format
    #AA,path_to_file
    #,path_to_file (to classify)

output_filename = "leave_one_out_" + str(round(time.time())) + ".csv"
fp = open(output_filename, "w")

for folder in os.listdir(PATH):
    file_arr = []
    for file in os.listdir(PATH + os.sep + folder):
        if(not file.split('_')[1].isnumeric()):
            index = random.randint(0, len(file_arr) - 1)
            file_to_classify = file_arr[index]
            #replacement(file_to_classify)
            author = file_to_classify.split('_')[0].split(',')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + file_to_classify.split(os.sep)[-1]
            #TranslationTour(path_to_file)
            Replacement(path_to_file)

            new_file = ',' + file_to_classify.split(',')[1]
            file_arr.remove(file_to_classify)
            fp.write(new_file + '\n')
            for f in file_arr:
                fp.write(f + '\n')
            break
        file_name = folder + ',' + PATH + folder + os.sep + file
        file_arr.append(file_name)



genCSVObfuscated(PATH)