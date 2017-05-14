import os
import sys
from collections import defaultdict


def tree():
    return defaultdict(tree)

class Viterbi:

    def __init__(self):
        self.data_path = '../data/'
        self.prob_file = ''
        self.sentences_file = ''
        self.probs_given_q = tree()
        self.probs_given_e = tree()
        self.tags = {'phi','noun','verb','prep','inf','fin'}
        self.default_prob = 0.0001


    def generate_tag_sequence(self):
        for fname in os.listdir(self.data_path):
            if fname[0] == '.' or fname != self.sentences_file:
                continue
            path = os.path.join(self.data_path, fname)
            f = open(path, 'r')
            for line in iter(f):
                print("\n")
                print("PROCESSING SENTENCE: " + line)
                pi = tree()
                fwd_pi = tree()
                back_pointer = tree()
                words = line.split()

                pi[0]['phi'] = 1
                for tag in self.tags:
                    if words[0].lower() not in self.probs_given_e.keys() or tag not in self.probs_given_e[words[0]].keys():
                        self.probs_given_e[words[0]][tag] = self.default_prob

                for k in range(1, len(words) + 1):
                    for tag in self.tags:
                        if k == 1:
                            pi[1][tag] = pi[0]['phi'] * float(self.probs_given_q[tag]['phi']) * float(
                                self.probs_given_e[words[0]][tag])
                            fwd_pi[1][tag] = pi[1][tag]
                            back_pointer[1][tag] = ['phi', pi[1][tag]]
                        else:
                            pi_list = []
                            fwd_pi_list = []
                            for tag_other in self.tags:
                                if words[k - 1] not in self.probs_given_e.keys() or tag not in self.probs_given_e[words[k - 1]].keys():
                                    self.probs_given_e[words[k - 1]][tag] = self.default_prob
                                if tag not in self.probs_given_q.keys() or tag_other not in self.probs_given_q[tag].keys():
                                    self.probs_given_q[tag][tag_other] = self.default_prob
                                pi_temp = pi[k - 1][tag_other] * self.probs_given_q[tag][tag_other] * self.probs_given_e[words[k - 1]][tag]
                                pi_temp_fwd = fwd_pi[k - 1][tag_other] * self.probs_given_q[tag][tag_other] * self.probs_given_e[words[k - 1]][tag]
                                pi_list.append((tag_other, pi_temp))
                                fwd_pi_list.append((tag_other, pi_temp_fwd))
                            sum = 0
                            for pi_value in fwd_pi_list:
                                sum += float(pi_value[1])
                            fwd_pi[k][tag] = sum

                            max_pi = float('-inf')
                            for pi_value in pi_list:
                                if pi_value[1] > max_pi:
                                    max_pi = float(pi_value[1])
                                    pi[k][tag] = max_pi
                                    back_pointer[k][tag] = [pi_value[0], pi_value[1]]

                pi_list = []
                for tag in self.tags:
                    pi_temp = pi[len(words)][tag] * float(self.probs_given_q['fin'][tag])
                    pi_list.append((tag, pi_temp))
                    max_pi = float('-inf')
                for pi_value in pi_list:
                    if pi_value[1] > max_pi:
                        max_pi = float(pi_value[1])
                        pi[len(words)]['fin'] = float(pi_value[1])
                        back_pointer[len(words) + 1]['fin'] = [pi_value[0], pi_value[1]]

                print("FINAL VITERBI NETWORK")
                for key, val in pi.items():
                    for tag in self.tags:
                        for value in val.items():
                            if key == 0 or tag[0] == 'fin':
                                continue
                            if tag == value[0]:
                                print("P(" + words[key - 1] + "=" + value[0] + ") = " + "%0.10f" % value[1])
                                break
                print("\n")
                print("FINAL BACKPOINTER NETWORK")
                for key, val in back_pointer.items():
                    if key == len(words) + 1 or key == 1:
                        continue
                    for tag in self.tags:
                        for value in val.items():
                            if value[0] == tag:
                                print("P(" + words[key - 1] + "=" + value[0] + ") = " + value[1][0])
                                break
                print("\n")
                print("BEST TAG SEQUENCE HAS PROBABILITY=" + "%0.10f" % back_pointer[len(words) + 1]['fin'][1])
                prev = 'fin'
                for key in range(len(words) + 1, 1, -1):
                    print (words[key - 2] + "->" + back_pointer[key][prev][0])
                    prev = back_pointer[key][prev][0]

                print("\n")
                print("FORWARD ALGORITHM RESULTS")
                for key, val in fwd_pi.items():
                    if key == 0:
                        continue
                    for tag in self.tags:
                        for value in val.items():
                            if tag == value[0]:
                                print("P(" + words[key - 1] + "=" + value[0] + ") = " + "%0.10f" % value[1])
                                break
                print("\n")


    def tabulate_probs(self):
        for fname in os.listdir(self.data_path):
            if fname[0] == '.' or fname != self.prob_file:
                continue
            path = os.path.join(self.data_path, fname)
            f = open(path, 'r')
            for line in iter(f):
                words = line.split()
                if words[0].lower() in self.tags:
                    self.probs_given_q[words[0].lower()][words[1].lower()] = float(words[2])
                else:
                    self.probs_given_e[words[0].lower()][words[1].lower()] = float(words[2])
        for tag in self.tags:
            if 'phi' not in self.probs_given_q[tag].keys():
                self.probs_given_q[tag]['phi'] = self.default_prob
            if 'fin' not in self.probs_given_q.keys() or tag not in self.probs_given_q['fin'].keys():
                self.probs_given_q['fin'][tag] = self.default_prob

    def main(self):
        self.prob_file = sys.argv[1]
        self.sentences_file = sys.argv[2]

v = Viterbi()
v.main()
v.tabulate_probs()
v.generate_tag_sequence()

