import os, random, re, math
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords

punctuation = ",;.!?"

def Replace_Stopwords(txt_file):
    author = txt_file.split(os.sep)[-2]
    operators = set('and', 'or', 'not', 'a', 'was', 'i', 'at',
                     'or', 'an', 'it', 'who','its', 'am', 'as','he',
                     'in', 'be')

    stops = set(stopwords.words('english')) - operators
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    token = nltk.word_tokenize(content)
    pos = nltk.pos_tag(token)
    output = ""

    for word, speech in pos:
        if word in stops:
            syn = wordnet.synsets(word)

            if syn:
                to_replace = word
                for l in syn[0].lemmas():
                    if word != l.name():
                        print(word, l.name())
                        to_replace = l.name()
                        break
                output += to_replace + " "
            else:
                output += word + " "
        else:
            output += word + " "
    output = re.sub(r" \,\.", ".", output)
    output = re.sub(r" \.", ".", output)
    output = re.sub(r" \?", "?", output)
    output = re.sub(r" \!", "!", output)
    output = re.sub(r" \,", ",", output)
    output = re.sub(r" \;", ";", output)
    output = re.sub(r" \:", ":", output)
    output = re.sub(r" ''",'"', output)
    output = re.sub(r'`` ', '"' , output)
    output = re.sub(r'\( ', '(', output)
    output = re.sub(r' \)', ')', output)
    output = re.sub(r" '", "'", output)

    output = re.sub(u"\u202d","",output)
    output = re.sub(u"\u202c","",output)
    output = re.sub(u"\u200e","",output)
    output = re.sub(u"\u200f","",output)
    output = re.sub(u"\uf0b0","",output)

    newFp = open(whereToWrite + os.sep + author +'_' + 'replacestop_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()

def Remove_Stopwords(txt_file):
    author = txt_file.split(os.sep)[-2]
    stops = set(stopwords.words('english')+['I'])
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    token = nltk.word_tokenize(content)

    output = ' '.join([word for word in token if word not in stops])

    output = re.sub(r" \,\.", ".", output)
    output = re.sub(r" \.", ".", output)
    output = re.sub(r" \?", "?", output)
    output = re.sub(r" \!", "!", output)
    output = re.sub(r" \,", ",", output)
    output = re.sub(r" \;", ";", output)
    output = re.sub(r" \:", ":", output)
    output = re.sub(r" ''",'"', output)
    output = re.sub(r'`` ', '"' , output)
    output = re.sub(r'\( ', '(', output)
    output = re.sub(r' \)', ')', output)
    output = re.sub(r" '", "'", output)

    output = re.sub(u"\u202d","",output)
    output = re.sub(u"\u202c","",output)
    output = re.sub(u"\u200e","",output)
    output = re.sub(u"\u200f","",output)
    output = re.sub(u"\uf0b0","",output)

    #exit(2) #remove this to make files

    newFp = open(whereToWrite + os.sep + author +'_' + 'stop_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()

#for combining sentences
def Sentence_Join(txt_file):
    author = txt_file.split(os.sep)[-2]
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    token = nltk.sent_tokenize(content)
    length = len(token)
    sents_to_combine = math.ceil(length/3)
    where_to_combine = math.ceil(length/sents_to_combine)

    new_content = ""
    count = 0
    toLower = False
    for sent in token:
        new_sent = ""
        word_token = nltk.word_tokenize(sent)
        pos = nltk.pos_tag(word_token)
        for word, speech in pos:
            if speech == "." and count % where_to_combine == 0:
                new_sent += "and "
                toLower = True
            else:
                if(toLower):
                    new_sent += word.lower() + " "
                else:
                    new_sent += word + " "
                toLower = False
        count += 1

        new_content += new_sent
    output = new_content

    output = re.sub(r" \,\.", ".", output)
    output = re.sub(r" \.", ".", output)
    output = re.sub(r" \,", ",", output)
    output = re.sub(r" \;", ";", output)
    output = re.sub(r" \:", ":", output)
    output = re.sub(r" ''",'"', output)
    output = re.sub(r'`` ', '"' , output)
    output = re.sub(r'\( ', '(', output)
    output = re.sub(r' \)', ')', output)
    output = re.sub(r" '", "'", output)

    output = re.sub(u"\u202d","",output)
    output = re.sub(u"\u202c","",output)
    output = re.sub(u"\u200e","",output)
    output = re.sub(u"\u200f","",output)
    output = re.sub(u"\uf0b0","",output)

    newFp = open(whereToWrite + os.sep + author +'_' + 'combine_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()

#for splitting sentences into multiple sentences
def Sentence_Split(txt_file):
    author = txt_file.split(os.sep)[-2]
    fp = open(txt_file,encoding='utf-8')
    content = fp.read()
    fp.close()

    whereToWrite = os.sep.join(txt_file.split(os.sep)[0:-1])

    token = nltk.sent_tokenize(content)
    new_content = ""
    for sent in token:
        count = 0
        new_sent = ""
        word_token = nltk.word_tokenize(sent)
        pos = nltk.pos_tag(word_token)
        for word, speech in pos:
            if speech == 'CC' and len(sent) - count > 4\
                    and len(sent) - count < 4:
                new_sent = new_sent[:-1]
                new_sent += '. '
            else:
                new_sent += word + " "
            count += 1
        new_content += new_sent

    output = new_content

    output = re.sub(r" \,\.", ".", output)
    output = re.sub(r" \.", ".", output)
    output = re.sub(r" \,", ",", output)
    output = re.sub(r" \;", ";", output)
    output = re.sub(r" \:", ":", output)
    output = re.sub(r" ''",'"', output)
    output = re.sub(r'`` ', '"' , output)
    output = re.sub(r'\( ', '(', output)
    output = re.sub(r' \)', ')', output)
    output = re.sub(r" '", "'", output)

    output = re.sub(u"\u202d","",output)
    output = re.sub(u"\u202c","",output)
    output = re.sub(u"\u200e","",output)
    output = re.sub(u"\u200f","",output)
    output = re.sub(u"\uf0b0","",output)

    newFp = open(whereToWrite + os.sep + author +'_' + 'sent_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()

#for synonym replacement
def Replacement(txt_file):
    #print(txt_file)
    author = txt_file.split(os.sep)[-2]
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
    output = re.sub(u"\uf0b0","",output)


    newFp = open(whereToWrite + os.sep + author +'_' + 'syn_obfuscated.txt','w')
    newFp.write(output)
    newFp.close()


def genCSVObfuscated(dataDir):
    # Generates CSV files for .run including the obfuscated versions as the unknown styles.
    output_filename = "with_obfuscated.csv"
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

def genCSVSent_Obfuscated(dataDir):
    # Generates CSV files for .run including the obfuscated versions as the unknown styles.
    output_filename = "sent_obfuscated.csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(dataDir):
        for file in os.listdir(dataDir + os.sep + folder):
            author = file.split('_')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + \
                           file.split(os.sep)[-1]
            if file.split('_')[1].isnumeric():
                fp.write(author + "," + path_to_file + "\n")
            elif "sent_obfuscated" in file:
                fp.write("," + path_to_file + "\n")
    fp.close()

    output_filename = "combine_obfuscated.csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(dataDir):
        for file in os.listdir(dataDir + os.sep + folder):
            author = file.split('_')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + \
                           file.split(os.sep)[-1]
            if file.split('_')[1].isnumeric():
                fp.write(author + "," + path_to_file + "\n")
            elif "combine_obfuscated" in file:
                fp.write("," + path_to_file + "\n")
    fp.close()


def genCSVStop_Obfuscated(dataDir):
    # Generates CSV files for .run including the obfuscated versions as the unknown styles.
    output_filename = "stop_obfuscated.csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(dataDir):
        for file in os.listdir(dataDir + os.sep + folder):
            author = file.split('_')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + \
                           file.split(os.sep)[-1]
            if file.split('_')[1].isnumeric():
                fp.write(author + "," + path_to_file + "\n")
            elif "stop_obfuscated" in file:
                fp.write("," + path_to_file + "\n")
    fp.close()

    output_filename = "replacestop_obfuscated.csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(dataDir):
        for file in os.listdir(dataDir + os.sep + folder):
            author = file.split('_')[0]
            path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + \
                           file.split(os.sep)[-1]
            if file.split('_')[1].isnumeric():
                fp.write(author + "," + path_to_file + "\n")
            elif "replacestop_obfuscated" in file:
                fp.write("," + path_to_file + "\n")
    fp.close()

def main():
    PATH = os.getcwd() + os.sep + "15auths" + os.sep
    '''
    CSV format:
        AA,path_to_file
        ,path_to_file (to classify)
    '''
    output_filename = "leave_one_out.csv"
    fp = open(output_filename, "w")

    for folder in os.listdir(PATH):
        file_arr = []
        for file in os.listdir(PATH + os.sep + folder):
            if(not file.split('_')[1].isnumeric()):
                index = random.randint(0, len(file_arr) - 1)
                file_to_classify = file_arr[index]
                author = file_to_classify.split('_')[0].split(',')[0]
                path_to_file = os.getcwd() + os.sep + "15auths" + os.sep + author + os.sep + file_to_classify.split(os.sep)[-1]
                #TranslationTour(path_to_file)
                Replacement(path_to_file)
                Sentence_Split(path_to_file)
                Remove_Stopwords(path_to_file)
                Sentence_Join(path_to_file)
                Replace_Stopwords(path_to_file)
                new_file = ',' + file_to_classify.split(',')[1]
                file_arr.remove(file_to_classify)
                fp.write(new_file + '\n')
                for f in file_arr:
                    fp.write(f + '\n')
                break
            file_name = folder + ',' + PATH + folder + os.sep + file
            file_arr.append(file_name)


    genCSVObfuscated(PATH)
    genCSVSent_Obfuscated(PATH)
    genCSVStop_Obfuscated(PATH)

if  __name__ =='__main__':
    main()