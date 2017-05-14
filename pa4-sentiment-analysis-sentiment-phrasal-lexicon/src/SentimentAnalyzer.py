import os
import sys
from itertools import islice
from collections import defaultdict
import math

class NaiveBayes:
    class TrainSplit:
        """Represents a set of training/testing data. self.train is a list of Examples, as is self.test. 
        """

        def __init__(self):
            self.train = []
            self.test = []

    class Example:
        """Represents a document with a label. klass is 'pos' or 'neg' by convention.
           words is a list of strings.
        """

        def __init__(self):
            self.klass = ''
            self.words = []
            self.fileName = ''

    def __init__(self):
        """NaiveBayes initialization"""
        self.numFolds = 10
        self.hits_great = 0
        self.hits_poor = 0
        self.index = defaultdict(lambda: defaultdict(dict))
        self.phrase_count = 0
        self.semantic_orientation = defaultdict(lambda : 0)

    #############################################################################
    # TODO TODO TODO TODO TODO
    # Implement the Multinomial Naive Bayes classifier and the Naive Bayes Classifier with
    # Boolean (Binarized) features.
    # If the BOOLEAN_NB flag is true, your methods must implement Boolean (Binarized)
    # Naive Bayes (that relies on feature presence/absence) instead of the usual algorithm
    # that relies on feature counts.
    #
    #
    # If any one of the FILTER_STOP_WORDS and BOOLEAN_NB flags is on, the
    # other one is meant to be off.

    def window(self, seq, n=3):
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    def classify(self, words):
        """ TODO
          'words' is a list of words to classify. Return 'pos' or 'neg' classification.
        """

        # Write code here

        semantic_orientation = 0
        semantic_orientation_sum = 0
        count = 0

        for words_set in self.window(words, 3):
            flag = False
            first_term = words_set[0]
            terms_split = first_term.split("_")
            first_word = terms_split[0]
            first_tag = terms_split[1]
            if first_word.lower() == 'great':
                self.hits_great += 1
            if first_word.lower() == 'poor':
                self.hits_poor += 1
            if first_tag not in ('JJ', 'RB', 'RBR', 'RBS', 'NN', 'NNS'):
                continue
            else:
                sec_term_split = words_set[1].split("_")
                sec_word = sec_term_split[0]
                sec_tag = sec_term_split[1]
                third_term_split = words_set[2].split("_")
                third_word = third_term_split[0]
                third_tag = third_term_split[1]
                if first_tag in ('JJ'):
                    if (sec_tag in ('NN', 'NNS') or
                            (sec_tag in ('JJ') and third_tag not in ('NN', 'NNS'))):
                        flag = True
                elif first_tag in ('RB', 'RBR', 'RBS'):
                    if (sec_tag in ('VB', 'VBD', 'VBN', 'VBG') or
                            (sec_tag in ('JJ') and third_tag not in ('NN', 'NNS'))):
                        flag = True
                elif first_tag in ('NN', 'NNS'):
                    if sec_tag in ('JJ'):
                        if third_tag not in ('NN', 'NNS'):
                            flag = True
            if flag:
                if (first_word, sec_word) in self.semantic_orientation:
                    semantic_orientation = self.semantic_orientation[(first_word, sec_word)]
                elif (first_word, sec_word) in self.index:
                    phrase_near_great = self.index[(first_word, sec_word)]['great']
                    phrase_near_poor = self.index[(first_word, sec_word)]['poor']
                    if phrase_near_great == 0:
                        phrase_near_great = 0.01
                    if phrase_near_poor == 0:
                        phrase_near_poor = 0.01
                    value = float(phrase_near_great * self.hits_poor) / float(phrase_near_poor * self.hits_great)
                    semantic_orientation = (math.log(value) / math.log(2))
                    self.semantic_orientation[(first_word, sec_word)] = semantic_orientation
                semantic_orientation_sum += semantic_orientation
                count += 1

        semantic_orientation_sum = semantic_orientation_sum/count

        if semantic_orientation_sum>=0:
            return 'pos'
        else:
            return 'neg'

    def calculate_semantic_orientation(self):
        semantic_orientation = 0
        for (first_word, sec_word) in self.index:
            phrase_near_great = self.index[(first_word, sec_word)]['great']
            phrase_near_poor = self.index[(first_word, sec_word)]['poor']
            if phrase_near_great == 0:
                phrase_near_great = 0.01
            if phrase_near_poor == 0:
                phrase_near_poor = 0.01
            value = float(phrase_near_great * self.hits_poor) / float(phrase_near_poor * self.hits_great)
            semantic_orientation += (math.log(value) / math.log(2))
            self.semantic_orientation[(first_word, sec_word)] = semantic_orientation


    def addExample(self, klass, words):
        """
         * TODO
         * Train your model on an example document with label klass ('pos' or 'neg') and
         * words, a list of strings.
         * You should store whatever data structures you use for your classifier 
         * in the NaiveBayes class.
         * Returns nothing
        """

        # Write code here

        position = -1

        for words_set in self.window(words, 3):
            position += 1
            flag = False
            first_term = words_set[0]
            terms_split = first_term.split("_")
            first_word = terms_split[0]
            first_tag = terms_split[1]
            if first_word.lower() == 'great':
                self.hits_great += 1
            if first_word.lower() == 'poor':
                self.hits_poor += 1
            if first_tag not in ('JJ', 'RB', 'RBR', 'RBS', 'NN', 'NNS'):
                continue
            else:
                sec_term_split = words_set[1].split("_")
                sec_word = sec_term_split[0]
                sec_tag = sec_term_split[1]
                third_term_split = words_set[2].split("_")
                third_word = third_term_split[0]
                third_tag = third_term_split[1]
                if first_tag in ('JJ'):
                    if (sec_tag in ('NN', 'NNS') or
                            (sec_tag in ('JJ') and third_tag not in ('NN', 'NNS'))):
                        flag = True
                elif first_tag in ('RB', 'RBR', 'RBS'):
                    if (sec_tag in ('VB', 'VBD', 'VBN', 'VBG') or
                            (sec_tag in ('JJ') and third_tag not in ('NN', 'NNS'))):
                        flag = True
                elif first_tag in ('NN', 'NNS'):
                    if sec_tag in ('JJ'):
                        if third_tag not in ('NN', 'NNS'):
                            flag = True
            if flag:
                self.phrase_count += 1
                start_range = position-15
                end_range = position+17
                if (first_word, sec_word) in self.index:
                    great = self.index[(first_word, sec_word)]['great']
                    poor = self.index[(first_word, sec_word)]['poor']
                else:
                    initial_value = defaultdict()
                    great = 0
                    poor = 0
                    initial_value['great'] = great
                    initial_value['poor'] = poor
                    self.index[(first_word, sec_word)] = initial_value

                great_present = False
                poor_present = False

                for near_terms in words[start_range:end_range]:
                    near_word = near_terms.split("_")[0]
                    if near_word.lower() == 'great':
                        great_present = True
                    if near_word.lower() == 'poor':
                        poor_present = True
                if great_present:
                    great += 1
                if poor_present:
                    poor += 1
                value = defaultdict()
                value['great'] = great
                value['poor'] = poor
                self.index[(first_word, sec_word)] = value

                # print ("<firstword-secondword> : %s_%s - %s_%s" %(first_word,first_tag,sec_word,sec_tag))
        # print ("self.index: %s" %(len(self.index)))
        # print ("self.hits_great: %s" %(self.hits_great))
        # print ("self.hits_poor: %s" %(self.hits_poor))
        pass

    # END TODO (Modify code beyond here with caution)
    #############################################################################


    def readFile(self, fileName):
        """
         * Code for reading a file.  you probably don't want to modify anything here, 
         * unless you don't like the way we segment files.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        result = self.segmentWords('\n'.join(contents))
        return result

    def segmentWords(self, s):
        """
         * Splits lines on whitespace for file reading
        """
        return s.split()

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        for fileName in posTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            example.klass = 'pos'
            split.train.append(example)
        for fileName in negTrainFileNames:
            example = self.Example()
            example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            example.klass = 'neg'
            split.train.append(example)
        return split

    def train(self, split):
        for example in split.train:
            words = example.words
            self.addExample(example.klass, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posTrainFileNames = os.listdir('%s/pos/' % trainDir)
        negTrainFileNames = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                example.klass = 'pos'
                example.fileName = fileName
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            for fileName in negTrainFileNames:
                example = self.Example()
                example.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                example.klass = 'neg'
                example.fileName = fileName
                if fileName[2] == str(fold):
                    split.test.append(example)
                else:
                    split.train.append(example)
            splits.append(split)
        return splits


def test10Fold(data_path):
    nb = NaiveBayes()
    splits = nb.crossValidationSplits(data_path)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        accuracy = 0.0
        for example in split.train:
            words = example.words
            classifier.addExample(example.klass, words)

        for example in split.test:
            words = example.words
            guess = classifier.classify(words)
            if example.klass == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def main():
    args = sys.argv
    test10Fold(args[1])


if __name__ == "__main__":
    main()
