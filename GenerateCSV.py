import os, random, re
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import WhitespaceTokenizer

punctuation = ",;.!?"

def replacement(txt_file):
    print(txt_file)
    stops = set(stopwords.words('english')+['I'])
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()


    token = nltk.word_tokenize(content)
    pos = nltk.pos_tag(token)

    output = ""

    for word, speech in pos:
        if speech == 'JJ':
            syn = wordnet.synsets(word)
            if syn:
                print(word + ', ' + str(syn))
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


    '''

    for word in token:
        syn = wordnet.synsets(word)
        if word not in stops and syn:
            print(syn[0].lemma_names('eng')[0])
            output += ' ' + str(syn[0].lemma_names('eng')[0])
        else:
            output += ' ' + word
    '''
    newFp = open('obfucated.txt','w')
    newFp.write(output)
    newFp.close()
    exit(2)


PATH = os.getcwd() + os.sep + "Drexel-AMT-Corpus" + os.sep


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
            replacement(os.getcwd() + os.sep +
                        "Drexel-AMT-Corpus" + os.sep + 'aa' + os.sep + file_to_classify.split(os.sep)[9])
            new_file = ',' + file_to_classify.split(',')[1]
            file_arr.remove(file_to_classify)
            fp.write(new_file + '\n')
            for f in file_arr:
                fp.write(f + '\n')
            break
        file_name = folder + ',' + PATH + folder + os.sep + file
        file_arr.append(file_name)