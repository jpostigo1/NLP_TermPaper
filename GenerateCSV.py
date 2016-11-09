import os, random

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
            new_file = ',' + file_to_classify.split(',')[1]
            file_arr.remove(file_to_classify)
            fp.write(new_file + '\n')
            for f in file_arr:
                fp.write(f + '\n')
            break
        file_name = folder + ',' + PATH + folder + os.sep + file
        file_arr.append(file_name)

