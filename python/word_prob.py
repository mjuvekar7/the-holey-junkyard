global sell
global buy
global gain
global loss

sell = ['sell', 'selling', 'sells', 'sold']
buy = ['buy', 'buying', 'bought', 'buys', 'purchase', 'purchases', 'purchasing']
gain = ['profit', 'gain']
loss = ['loss']

def solve_pl(prob):
    """Solves simple profit and loss problems."""
    global sell
    global buy
    global gain
    global loss

    sell_word = False
    buy_word = False
    gain_word = False
    loss_word = False
    sp, cp, gainp = 0, 0, 0
    words = prob.split()

    for i in range(0, len(words[:])):
        words[i] = words[i].lower().rstrip('.,!?%').lstrip('$')

    for word in words:
        if sell_word:
            if word.isdecimal():
                sell_word = False
                sp = int(word)
                continue
        if buy_word:
            if word.isdecimal():
                buy_word = False
                cp = int(word)
                continue
        if gain_word:
            if words[words.index(word) - 1].isdecimal():
                gainp = int(words[words.index(word) - 1])
            elif word.isdecimal():
                gain_word = False
                gainp = int(word)
                continue
        if loss_word:
            if words[words.index(word) - 1].isdecimal():
                gainp = 0 - int(words[words.index(word) - 1])
            elif word.isdecimal():
                loss_word = False
                gainp = 0 - int(word)
                continue
        
        if word in sell:
            sell_word = True
        elif word in buy:
            buy_word = True
        elif word in gain:
            gain_word = True
        elif word in loss:
            loss_word = True

    if gainp == 0:
        if 'percent' in words:
            if sp > cp:
                print('Profit percent is {%}'.format((sp - cp)/cp))
            elif cp > sp:
                print('Loss precent is {%}'.format((cp - sp)/cp))
            else:
                print('No profit, no loss!')
        else:
            if sp > cp:
                print('Profit is {}'.format(sp - cp))
            elif cp > sp:
                print('Loss is {}'.format(cp - sp))
            else:
                print('No profit, no loss!')
    else:
        if sp == 0:
            print('Selling price is {}'.format(((100+gainp)/100) * cp))
        elif cp == 0:
            print('Cost price is {}'.format((100/(100+gainp)) * sp))
        else:
            print('Error!')

def prob_type():
    """What type of problem are we solving?"""
    # code to decide type of problem
    # types include:
    #  -- profit and loss (solve_pl)
    #  -- simple interest (solve_si)
    #  -- compound interest (solve_ci)
    #  -- etc.

