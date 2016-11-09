import os, re

txt_file_paths = []
for root, dirs, files in os.walk('tmp'):
    for file in files:
        if file.endswith(".txt"):
            txt_file_paths.append(os.path.join(root, file))
for files in txt_file_paths:
    fp = open(os.getcwd() + os.sep + files, 'r')
    pattern = re.compile('\d.+\w+')
    count = 0
    correct = 0
    list_of_correct_authors = []
    list_of_classified_authors = []
    for line in fp.readlines():
        if ".txt" in line:
            correctAuthor = line.split('_')[0]
            list_of_correct_authors.append(correctAuthor)
        elif re.match(pattern, line):
            classifiedAuthor = ''.join(re.findall(r'[A-z]',line))
            list_of_classified_authors.append(classifiedAuthor)
    fp.close()

    #print(list_of_correct_authors)
    #print(list_of_classified_authors)

    for i in range(len(list_of_correct_authors)):
        if(list_of_correct_authors[i] == list_of_classified_authors[i]):
            correct += 1
        count += 1

    print("Accuracy for {}:\n{}".format(files, float(correct/count)))

