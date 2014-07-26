import text2num

be = [
    'be',
    'was',
    'were',
    'am',
    'are',
    'is',
    'will be',
]

have = [
    'have',
    'had',
    'have',
    'will have',
]

verbs = [be, have]

def prepare(problem):

    # convert 'three' to 3
    for line in problem.splitlines(True):
        for word in line.split():
            try:
                word = text2num.text2num(word)
            except text2num.NumberException:
                pass

    # remove punctuation, replace with newlines
    # also remove conjunctions
    problem = problem.lower().replace('.', '\n').replace('?', '\n')
    for key in list(conjs.keys()):
        problem = problem.replace(key, '\n').replace(',', '')
    problem = problem.strip()
    statements, queries = [], []
    for line in problem.splitlines(True):
        if '?' in line:
            queries.append(line)
        else:
            statements.append(line)
    problem = ''
    for line in statements:
        problem += line
    problem += '\n'
    for line in queries:
        problem += line

    # simplify text
    # i.e. for now, remove articles, replace verb forms with root
    for art in ['a', 'an', 'the']:
        problem = problem.replace(art, '')
    for word in problem.split():
        for verb in verbs:
            if word in verbs:
                problem = problem.replace(word, verb[0], 1)
