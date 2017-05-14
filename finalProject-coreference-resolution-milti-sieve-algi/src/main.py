import sys
import os
import xml.etree.ElementTree as ET
import sieves as Sieve
import corefoutput
import corefscorer


def get_name_list(names_file):
    name_list = []
    for name in names_file:
        stripped_name = name.strip()
        if not stripped_name.startswith('#') and not stripped_name == '':
            name_list += [stripped_name]
    return name_list

def parse_coref_id(input_file):
    coref_ids = []
    coref_tail = []
    elem = ET.parse(input_file).getroot()

    for phrases in elem.findall('COREF'):
        text_value = phrases.text
        tail_value = phrases.tail
        if "\n" in text_value:
            text_value = text_value.replace('\n',' ')
        if "\n" in tail_value:
            tail_value = tail_value.replace('\n',' ')

        coref_ids += [[str(phrases.get('ID')), text_value]]
        coref_tail += [[str(phrases.get('ID')), tail_value]]
    return coref_ids, coref_tail


def evaluate_coref(input_list, female_list, male_list, sieve_count):
    for file in input_list:
        filename = os.path.splitext(os.path.basename(file))[0]
        coref_ids, coref_tail = parse_coref_id(file)
        result = Sieve.main(coref_ids, coref_tail, female_list, male_list, sieve_count)
        outputfile = corefoutput.main(result)
        fwrite = open('responses/' + filename + '.response', 'w')
        fwrite.write(outputfile)
        fwrite.close()



def main():
    args = sys.argv
    if len(args) != 5:
        print ("Incorrect no of arguments supplied. Please try again. <list file of input> <list of female proper nouns> <list of male proper nouns> <sieve_count>")
    else:
        input_file_list = args[1]
        female_noun_list = args[2]
        male_noun_list = args[3]
        sieve_count = int(args[4])

        input_file = open(input_file_list, 'r')
        input_fs = input_file.read().splitlines()
        input_list = get_name_list(input_fs)

        female_file = open(female_noun_list, 'r')
        female_fs = female_file.readlines()
        female_list = get_name_list(female_fs)

        male_file = open(male_noun_list, 'r')
        male_fs = male_file.readlines()
        male_list = get_name_list(male_fs)

        evaluate_coref(input_list, female_list, male_list, sieve_count)
        responsefile = open('responselist.txt', 'w')
        for file in input_list:
            file_temp = file.split('/')[-1]
            filename = file_temp.split('.')[0]
            # print filename
            responsefile.write('responses/' + filename + '.response\n')
        responsefile.close()

        #Call Also coref-scorer
        argslist=["","responselist.txt", "../dev", "-V"]
        #argslist = ["", "responselist.txt", "../test", "-V" ]
        corefscorer.main(argslist)



if __name__ == "__main__":
    main()