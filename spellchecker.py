import re
import sys


def spellcheck(fname_txt,fname_dict):
    tokens_dict = makeList(fname_dict)
    with open(fname_txt) as fp:
        res_text = ""
        line_no = 0
        for line in fp:
            line_token = []
            mispelled_line = line # store the line for later use

            # whitespace around unambiguous separators
            line = re.sub(r'([\\?!()\";/\\|`])',r' \1 ', line)

            # whitespace around commas that aren't in numbers
            line = re.sub(r'([^0-9]),', r'\1 ', line)
            line = re.sub(r',([^0-9])', r' \1', line)

            line = re.sub(r'([^0-9]);', r'\1 ', line)
            line = re.sub(r';([^0-9])', r' \1', line)

            line = re.sub(r'([^0-9]):', r'\1 ', line)
            line = re.sub(r':([^0-9])', r' \1', line)

            # remove period and replace with whitespace
            line = re.sub(r'([A-Za-z]+)\.', r' \1 ', line)

            # remove comma and replace with whitespace
            line = re.sub(r' ([^0-9]) ,', r' \1 ', line)

            # remove abbreviations (e.g. U.S.A.) and replace with whitespace 
            line = re.sub(r'([A-Z]\.)+',r' ',line)

            # words with internal hyphens are broken apart
            line = re.sub(r'(\w+)-(\w+)',r'\1 \2',line)

            line_token.extend(line.split())
            line_no += 1
            mispelled_count = 0
            res_line = mispelled_line
            for token in line_token:
                a_word = False
                for token_w in tokens_dict:
                    if token == token_w:
                        a_word = True
                        break
                if a_word == False:
                    res_line = re.sub(token,suggest(tokens_dict,token,line_no), res_line)
                    mispelled_count += 1
            if mispelled_count == 0:
                res_text += mispelled_line
            else:
                res_text += res_line
        writeToFile(res_text,fname_txt)

# implementation of the edit distance algorithm
def edit_dist(mispelled,target):
    m_len = len(mispelled)
    t_len = len(target)

    
    l = [[0 for x in range(t_len+1)] for y in range(m_len+1)]

    # set empty string row cells from 1 to m_len+1
    for i in range(1, m_len+1):
        l[i][0] = i

    # set empty string column from 1 to t_len+1
    for j in range(1, t_len+1):
        l[0][j] = j
    
    for i in range(1, m_len+1):
        for j in range(1, t_len+1):
            # same character/letter cost 0 for substitution
            if mispelled[i-1] == target[j-1]: 
                dist_cost = 0 
            else:
                # default substitution cost
                dist_cost = 2  
            l[i][j] = min(l[i-1][j] + 1, l[i-1][j-1] + dist_cost, l[i][j-1]+1)
    return l[m_len][t_len] # return distance cost

# Returns a list of at most 3 words with the least edit distance
def suggest(tokens_dict,m,l):
    suggested = []
    res = False
    temp = ""
    for token_w in tokens_dict:
        if edit_dist(m,token_w) <= 2:
            if(len(suggested) < 3):
                suggested.append(token_w)
                res = True
                temp = "mispelled word: "+m+" -- (line: "+str(l)+") -- "
    if res == False:
        # if no suggestions of set distance range is found, we return the mispelled word
        temp = "mispelled word: "+m+" -- (line: "+str(l)+") -- "+"suggested words: []"
        print(temp)
        return m
    else:
        temp += "suggested words : ["
        for i in range(len(suggested)):
            if i == len(suggested)-1:
                temp += suggested[i]+"]"
            else:
                temp += suggested[i]+", "
        print(temp)
        return suggested[0]

# writing to file. Ovewrites existing file
def writeToFile(txt,og_fname):
    name = "corrected_"+og_fname
    f = open(name,"w")
    f.write(txt)
    f.close()


# for dictionary words to list
def makeList(f):
    with open(f) as fp:
        tokens = []
        for line in fp:
            tokens.extend(line.split())
        return tokens        


def main():
    # to run program type : python3 <file_name> words
    spellcheck(sys.argv[1],sys.argv[2])


if __name__ == '__main__':
    main()

    