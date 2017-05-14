import re


def outputfileforcluster(inputfile, clusters):
    ids = 0
    f = open(inputfile, 'r')
    fs = f.read()
    fs = fs.lower()
    for cluster in clusters:
        flag = 0;
        for element in cluster:
            element = element.lower()
            init_start=0
            while fs.find(element,init_start)!=-1:
                if(element == cluster[0].lower() and flag == 0):
                    
                    if(fs[fs.find(element,init_start)-14 : fs.find(element,init_start)-7] in '<coref id='):
                        
                        p = fs[fs.find(element,init_start)-6:fs.find(element,init_start)]
                        
                        if(re.findall(r'[*][0-9]|[0-9]+',p)!=[]):
                            ids = re.findall(r'[*][0-9]|[0-9]+',p)[0]
                            flag = 1
                        
                cur_index = fs.find(element,init_start)
                if(fs[fs.find(element,init_start)-14 : fs.find(element,init_start)-7] in '<coref id='):
                    st = fs[fs.find(element,init_start)-5:fs.find(element,init_start)]
                    if(re.findall(r'[*][0-9]|[0-9]+',st)):
                        ids2 = re.findall(r'[*][0-9]|[0-9]+',st)[0]
                    if(ids != '0' and ids != ids2):
                        fs=fs[:cur_index-1]+' ref="'+str(ids)+'"'+fs[cur_index-1:]
                    init_start=cur_index+len(element)
                else:
                    init_start=cur_index+len(element)
                
    fs1 = fs.replace("txt","TXT")
    fs2 = fs1.replace('coref','coref'.upper())
    fs3 = fs2.replace('id','id'.upper())
    fs4 = fs3.replace('ref','ref'.upper())

    return fs4

def final_output(result):
    output = '<TXT>\n'
    for res in result:
        if len(res) is 2:
            output = output + r'<COREF ID="' + res[0] + '">' + res[1] + '</COREF>\n'
        elif len(res) is 3:
            output = output + r'<COREF ID="' + res[0] + '" REF="' + res[2] + '">' + res[1] + '</COREF>\n'
    output = output + '</TXT>'
    return output


def main(result):
    x = final_output(result)
    return x

if __name__ == '__main__':
    main(result)