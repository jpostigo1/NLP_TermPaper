import os, re, random, shutil, subprocess
from nltk import sent_tokenize
import GenerateCSV

# Run this from the NLP_TermPaper dir to get the grammar scores.


AUTHORS_DIR = "15auths"
TEMP_DIR = "tempSentencePairs"

def writeSentencePairs():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)
    for author_dir in os.listdir(AUTHORS_DIR):
        author_files = [f for f in os.listdir(AUTHORS_DIR + os.sep + author_dir) if re.match(r"^[a-zA-Z]*_\d.*", f)]
        rand_file_contents = open(AUTHORS_DIR + os.sep + author_dir + os.sep + random.choice(author_files), "r").read()
        sents = sent_tokenize(rand_file_contents)
        index = random.randint(1, len(sents) - 1)
        sent_pair = sents[index-1:index+1]
        os.mkdir(TEMP_DIR + os.sep + author_dir)
        output_file = open(TEMP_DIR + os.sep + author_dir + os.sep + author_dir + "_original", "w")
        output_file.write(" ".join(sent_pair))
        output_file.close()


def writeObfuscated():
    for original in os.listdir(TEMP_DIR):
        GenerateCSV.Sentence_Join(TEMP_DIR + os.sep + original + os.sep + original + "_original")
        GenerateCSV.Sentence_Split(TEMP_DIR + os.sep + original + os.sep + original + "_original")
        GenerateCSV.Replacement(TEMP_DIR + os.sep + original + os.sep + original + "_original")
        GenerateCSV.Remove_Stopwords(TEMP_DIR + os.sep + original + os.sep + original + "_original")
        GenerateCSV.Replace_Stopwords(TEMP_DIR + os.sep + original + os.sep + original + "_original")


def getAverageParseScore(parser_output):
    results = re.findall(r"# Parse \d+ with score (-?[0-9.]+)", str(parser_output))
    sum = 0
    for r in results:
        sum += float(r)
    return sum / len(results)


def printScores():
    for author_dir in os.listdir(TEMP_DIR):
        original_score = None
        scores = {}
        for text_file in os.listdir(TEMP_DIR + os.sep + author_dir):
            output = subprocess.check_output(["stanford-parser-full-2015-12-09" + os.sep + "lexparser.sh",
                                               TEMP_DIR + os.sep + author_dir + os.sep + text_file],
                                              stderr=subprocess.STDOUT)
            score = getAverageParseScore(output)
            if text_file == author_dir + "_original":
                original_score = score
            else:
                scores[text_file] = score
        for filename,parse_score in scores.items():
            print(filename + "'s difference from original: " + str(original_score - parse_score))


def main():
    # extract two sentences from each author and write them to a new file
    writeSentencePairs()
    # run obfuscation methods on each sentence-pair file and write results to a new file
    writeObfuscated()
    # get average parse scores of before and after versions
    printScores()


if  __name__ =='__main__':
    main()
