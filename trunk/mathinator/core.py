import sys

global tokens, queries, modules
tokens = ['is']
queries = ['what']
_modules = ['arith']

for mod in _modules:
    import modules.mod
    
def getInput():
    f = open('in', 'r')
    lines = f.read().splitlines()
    line_words = []
    index = 0
    for line in lines:
        line_words.append(line.split(' '))
        index += 1
    return line_words
    
def parseLine(line):
    symbol = ''
    value = ''
    left = True
    for word in line:
        if word not in tokens:
            if left:
                symbol += word
            else:
                value += word
        else:
            if word == tokens[0]:
                left = False
    return (symbol, value)

def main():
    inp = getInput()
    subs = []
    vals = []
    for line in inp:
#       for word in line:
#           print(word, end=' ')
#       print()
        s, v = parseLine(line)
        subs.append(s)
        vals.append(v)
    print(subs)
    print(vals)
    print()
    count = 0
    for sub in subs:
        if sub in queries:
            if sub == queries[0]:
                ans = vals[subs.index(vals[count])]
                print(ans)
        count += 1

if __name__ == '__main__':
    main()
