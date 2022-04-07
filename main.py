import sys

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import random


def read_file(name):
    file = open(name, 'r')
    lines = file.readlines()
    txt = ''
    for line in lines:
        txt = txt + line
    return nltk.word_tokenize(txt)


def get_nouns(pos_tags):
    nn = []
    for txt, pos in pos_tags:
        if pos.find('NN') == 0:
            nn.append(txt)
    # print(nn[0:20])
    return nn


def tag(lemmas):
    tgs = nltk.pos_tag(lemmas)
    print('First 20 tagged items: ', tgs[0:20])
    return tgs


def lemmatize(tkns):
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tkns]
    lemmas = list(set(lemmas))
    # print('The number of unique lemmas: {}'.format(len(lemmas)))
    return lemmas


def lexical_diversity(unique, important):
    ld = unique / important
    print('Lexical Diversity: {:.2f}'.format(ld))
    return ld


def preprocess(text):
    tkns = [t.lower() for t in text]  # make lowercase
    tkns = [t for t in tkns if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    lexical_diversity(len(set(tkns)), len(tkns))
    lemmas = lemmatize(tkns)
    pos_tags = tag(lemmas)
    nn = get_nouns(pos_tags)
    print('Number of tokens: {}, Number of nouns: {}'.format(len(tkns), len(nn)))
    return tkns, nn


def noun_dictionary(tkns, nn):
    nn_dict = {}
    for n in nn:
        nn_dict[n] = 0
    for t in tkns:
        if nn_dict.get(t) is not None:
            nn_dict[t] = nn_dict.get(t) + 1
    nn_sorted = sorted(nn_dict, key=nn_dict.get, reverse=True)[0:50]
    for nn in nn_sorted:
        print(nn, ':', nn_dict[nn])
    return nn_sorted


# Game helper functions
def to_string(arr):
    s = ''
    for _ in arr:
        s += _
    return s


def play_game(words, points):
    print('Let\'s play a word guessing game!')
    # flag to break out of game while-loop
    end_game = False
    # first-round flag
    first_round = True
    # game while-loop
    while end_game is False:
        if first_round is False:
            print('Guess another word')
        # get random word
        word = random.choice(words)
        # get length of random word
        size = len(word)
        # create underscore array and fill with ${size} amount of '_'
        underscore = []
        for _ in range(size):
            underscore.append('_')
        # guessing while-loop
        while 1:
            # check if word is already completed, break if true
            if '_' not in underscore:
                print('\n', word)
                print('You solved it!')
                print('Total Score: {}\n'.format(points))
                first_round = False
                break
            # print current underscore string
            print(to_string(underscore))
            # ask for user input
            guess = input('Guess a letter: ')
            # check if input == '!', break out of guessing while-loop if true
            if guess == '!':
                end_game = True
                break
            # check if word contains guess and that guess was not guessed previously before
            if word.find(guess) != -1 and guess not in underscore:
                # increment points
                points += 1
                # for every char in word, if char == guess, then replace idx of char in underscore with guess
                for i in range(size):
                    if word[i] == guess:
                        underscore[i] = guess
                # print feedback and score
                print('Right! Score: {}'.format(points))
            # word does not contain letter
            elif word.find(guess) < 0:
                # decrement points
                points -= 1
                # if points become less than 0, end the game
                if points < 0:
                    end_game = True
                    break
                # print feedback and score
                print('Sorry, guess again! Score: {}'.format(points))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Required parameter <Filename> not provided.')
        sys.exit()
    filename = sys.argv[1]
    raw_text = read_file(filename)
    tokens, nouns = preprocess(raw_text)
    common_nn = noun_dictionary(tokens, nouns)
    play_game(common_nn, 5)
