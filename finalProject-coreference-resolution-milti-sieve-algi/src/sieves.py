import itertools
import re
from nltk.corpus import wordnet as wn

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
                 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
                 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
                 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
                 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
simplePronouns = ("he", "she", "her", "his", "hers", "him")
simplePronouns_male = ("he", "his", "him")
simplePronouns_female = ("she", "her", "hers")
personPronouns = ("i", "we", "you")
neuteredPronouns = ("its", "it", "they", "them", "theirs", "their")
reflexivePronouns = ("himself", "themselves", "herself", "itself")


#Match nominal phrases exactly
def exact_string_matching(noun_phrases):
    for np_1, np_2 in itertools.combinations(noun_phrases, 2):
        if np_1[1] not in stopwords:
            if np_1[1].lower() == np_2[1].lower() and np_1[0] != np_2[0]:
                if (len(np_1) == 2):
                    np_1.append(np_2[0])
                if (len(np_2) == 2):
                    np_2.append(np_1[0])
    return noun_phrases

#Match Acronyms and Appositives
def precise_constructs_matching(noun_phrases,phrase_tail):
    for np_1, np_2 in itertools.combinations(noun_phrases, 2):
        if len(np_2[1].split()) == 1:
            if(is_abbrev(np_2[1], np_1[1])):
                if (len(np_1) == 2):
                    np_1.append(np_2[0])
                if (len(np_2) == 2):
                    np_2.append(np_1[0])
    for i,np in enumerate(phrase_tail):
        if np[1] is "," or np[1] is 'is':
            if len(noun_phrases[i+1]) == 2:
                noun_phrases[i+1].append(np[0])
    return noun_phrases

# def is_abbrev(abbrev, text):
#     flag = True
#     text_split = text.split(" ")
#     if len(abbrev) == len(text_split):
#         i = 0
#         for split in text_split:
#             if split[0].lower() == abbrev[i].lower():
#                 i += 1
#                 continue
#             else:
#                 flag = False
#                 break
#     else:
#         flag = False
#     return flag

def is_abbrev(abbrev, text):
    pattern = "(|.*\s)".join(abbrev.lower())
    return re.match("^" + pattern, text.lower()) is not None

#Match nominal mentions having words in common
def strict_head_matching(noun_phrases):
    for np_1, np_2 in itertools.combinations(noun_phrases, 2):
        np_1_words = np_1[1].split()
        np_2_words = np_2[1].split()
        if (len(np_1_words) > 1 or len(np_2_words) > 1):
            for word1 in np_1_words:
                if word1.lower() not in stopwords:
                    for word2 in np_2_words:
                        if word2.lower() not in stopwords:
                            if (word1.lower() == word2.lower()):
                                if (len(np_1) == 2):
                                    np_1.append(np_2[0])
                                if (len(np_2) == 2):
                                    np_2.append(np_1[0])
                                continue
    return noun_phrases


#Match Synonyms
def lexical_matching(noun_phrases):
    for i, np_1 in enumerate(noun_phrases):
        if np_1[1].lower() not in stopwords:
            np_1_words = np_1[1].split()
            synonym1=[]
            synonym2 = []
            for word in np_1_words:
                if word.lower() not in stopwords:
                    for sysnet in wn.synsets(word.lower(), wn.NOUN):
                        synonym1 += [(sysnet, sysnet.lexname())]
            for j, np_2 in enumerate(noun_phrases[i+1:]):
                if np_2[1].lower() not in stopwords:
                    np_2_words=np_2[1].split()
                    synonym2 = []
                    for word in np_2_words:
                        if word.lower() not in stopwords:
                            for sysnet in wn.synsets(word.lower(), wn.NOUN):
                                synonym2 += [(sysnet, sysnet.lexname())]
                    synonymn_match=set(synonym1).intersection(set(synonym2))
                    if len(synonymn_match)>1 and np_1[1]!= np_2[1]:
                        if (len(np_1) == 2):
                            np_1.append(np_2[0])
                        if (len(np_2) == 2):
                            np_2.append(np_1[0])
    return noun_phrases

#Match pronouns
def pronoun_matching(noun_phrases, females_list, males_list):
    for i, np_1 in enumerate(noun_phrases):
        if any(pronoun in np_1[1] for pronoun in simplePronouns):
            end_range = i - 11 if (i - 11) > 0 else 0
            start_range=i-1 if i-1>0 else 0
            #for j, np_2 in enumerate(noun_phrases[start_range:i - 1]):
            for np_2 in (noun_phrases[start_range:end_range:-1]):
                if any(pronoun in np_1[1] for pronoun in simplePronouns_male) and any(np in np_2[1] for np in males_list):
                    if len(np_1) == 2:
                        np_1.append(np_2[0])
                if any(pronoun in np_1[1] for pronoun in simplePronouns_female) and any(np in np_2[1] for np in females_list):
                    if len(np_1) == 2:
                        np_1.append(np_2[0])
    return noun_phrases


def main(noun_phrases,phrase_tail,females_list,males_list,seive_count):
    if seive_count >= 1:
        noun_phrases = exact_string_matching(noun_phrases)
    if seive_count >= 2:
        noun_phrases = precise_constructs_matching(noun_phrases,phrase_tail)
    if seive_count >= 3:
        noun_phrases = strict_head_matching(noun_phrases)
    if seive_count >= 4:
        noun_phrases = lexical_matching(noun_phrases)
    if seive_count >= 5:
        noun_phrases = pronoun_matching(noun_phrases, females_list, males_list)

    results = noun_phrases
    return results

if __name__ == '__main__':
    main(noun_phrases,phrase_tail,females_list,males_list,seive_count)