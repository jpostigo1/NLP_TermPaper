import os, sys, re
from collections import namedtuple

RESULT_FILE_DIR = "tmp"
RESULT_FILE_EXT = ".txt"

# Keys in the results dictionary
FILE_NAME_KEY = "file_name_key"
FILE_PATH_KEY = "file_path_key"
CANONICIZERS_KEY = "canonicizers_key"
EVENT_DRIVER_KEY = "event_driver_key"
ANALYSIS_KEY = "analysis_key"
RESULTS_KEY = "results_key"


class Result:
    """
    The result representing the classification of a single file from the JGAAP output text file.
    There are many Results per experiment.
    """

    def __init__(self, text_block):
        match = re.match(r"^(.*?) (.*)\nCanonicizers: (.*)\nEventDriver: (.*)\nAnalysis: (.*)\n(.*)$",
                         text_block)

        if match:
            canonicizers = match.group(3).split(', ') if match.group(3) != "none" else []
        else:
            sys.exit("Invalid result text: \n{}".format(text_block))

        classifications = []
        classify_lines = match.group(6).split('\n')
        for classify_line in classify_lines:
            _, style_classified, number_score = classify_line.split(' ')
            classifications.append((style_classified, number_score))

        self.file_name = match.group(1)
        self.full_file_path = match.group(2)
        self.canonicizers = canonicizers  # list of canonicizers used (empty if none)
        self.event_driver = match.group(4)
        self.analysis_method = match.group(5)
        self.classifications = classifications  # a list of tuples (style_classified, number_score)


    def getClassifiedAuthor(self):
        """Returns the first classified style/author"""
        return self.classifications[0][0]

    def isCorrect(self):
        return self.getClassifiedAuthor() == self.file_name[:self.file_name.index('_')]

    def toString(self):
        return "File: {}, Path: {}, Canonicizers: {}, Event Driver: {}, " \
               "Analysis Method: {}, Classifications: {}"\
            .format(self.file_name,
                    self.full_file_path,
                    str(self.canonicizers),
                    self.event_driver,
                    self.analysis_method,
                    str(self.classifications))

def getResultFilePaths(dir_to_search):
    txt_file_paths = []
    for root, dirs, files in os.walk(dir_to_search):
        for file in files:
            if file.endswith(RESULT_FILE_EXT):
                txt_file_paths.append(os.path.join(root, file))
    return txt_file_paths


def getExperimentAccuracy(list_of_results):
    """Returns a simple accuracy for the list of Result objects."""
    num_correct, num_total = 0, 0
    for result in list_of_results:
        if result.isCorrect():
            num_correct += 1
        num_total += 1
    return num_correct / num_total


def getFileResults(fullpath):
    """Returns a list of Result objects for one result text file."""
    fp = open(fullpath, 'r')
    text_blocks = fp.read().split("\n\n\n")
    fp.close()

    results = []
    for text_block in text_blocks:
        if text_block != "":
            results.append(Result(text_block))

    return results


def getAllFilesResults(working_dir, result_files_dir):
    """Returns a dictionary with entries of {filename: [<Result>, <Result>, ...]}."""
    filename_results = {}
    result_file_paths = getResultFilePaths(result_files_dir)

    for file_path in result_file_paths:
        fullpath = working_dir + os.sep + file_path
        filename_results[file_path] = getFileResults(fullpath)

    return filename_results


def main():
    all_files_results = getAllFilesResults(os.getcwd(), RESULT_FILE_DIR)

    """
    for filename in all_files_results:
        for result in all_files_results[filename]:
            print("{}:\n{}\n".format(filename, result.toString()))
    """
    results_array = []
    for filename, results in all_files_results.items():
        results_array.append((filename, getExperimentAccuracy(results)))
    results_array = sorted(results_array, key=lambda x: x[0])

    for filename,accuracy in results_array:
        print("Accuracy for {}:\n{}".format(filename, accuracy))


if  __name__ =='__main__':
    main()
