#!/usr/bin/python3
from os import system as sys
from random import choice
from math import sqrt
from time import sleep
import readline

game = "english_small"
N = 4

SMALL_ENGLISH_FILE = "liste_english_small.txt"
ENGLISH_FILE = "liste_english.txt"
FRENCH_FILE = "liste_francais.txt"


boggle_letters_4_en = [
        "rifobx",
        "ifehey",
        "denows",
        "utoknd",
        "hmsrad",
        "lupets",
        "acitoa",
        "ylgkue",
        "qbmjoa",
        "ehispn",
        "vetign",
        "baliyt",
        "ezavnd",
        "ralesc",
        "uwilrg",
        "pacemd"
        ]

boggle_letters_5_en = [
        "qbzjxk",
        "hhlrdo",
        "telpci",
        "ttotem",
        "aeaeee",
        "touoto",
        "nhdtho",
        "ssnseu",
        "sctiep",
        "yifpsr",
        "ovwrgr",
        "lhnrod",
        "riyprh",
        "eandnn",
        "eeeema",
        "aaafsr",
        "afaisr",
        "dordln",
        "mnneag",
        "ititie",
        "aumeeg",
        "yifasr",
        "ccwnst",
        "uotown",
        "etilic"
        ]

boggle_letters_4_fr = [
        "etukno",
        "ehifse",
        "navedz",
        "tlibra",
        "evgtin",
        "recals",
        "eioata",
        "spulte",
        "decamp",
        "entdos",
        "glenyu",
        "aimsor",
        "ielruw",
        "ofxria",
        "bmaqjo",
        "enhris"
        ]

if game == "english_big":
    letters = boggle_letters_5_en
    N = 5
    words = open(ENGLISH_FILE).read().split('\n')
elif game == "english_small":
    N = 4
    letters = boggle_letters_4_en
    words = open(ENGLISH_FILE).read().split('\n')
elif game == "french_small":
    N = 4
    letters = boggle_letters_4_fr
    words = open(FRENCH_FILE).read().split('\n')

def randomise_game(letters):
    board = [choice(letters.pop(letters.index(choice(letters)))) for _ in range(len(letters))]
    return board

def print_board(board):
    for i in range(int(sqrt(len(board)))):
        print(' '.join(board[i*N:i*N+N]))

def get_neighbor_indexes(board,index):
    n=set()
    for i in range(9):
        x,y = index%N+(i%3-1), index//N+(i//3-1)
        if 0 <= x < N and 0 <= y < N and i != 4:
            n.update((board[y*N+x],))
    return n

def get_indexes(board, letter, index):
    n=set()
    if index == -1:
        for i,c in enumerate(board):
            if c == letter:
                n.update((i,))
    else:
        for i in range(9):
            x,y = index%N+(i%3-1), index//N+(i//3-1)
            if 0 <= x < N and 0 <= y < N and i != 4:
                if board[y*N+x] == letter:
                    n.update((y*N+x,))
    return n


def find_pattern(board, letters, pattern, index=-1, prev_index=[]):
    if not pattern:
        #print(' '.join([str(i) for i in prev_index]))
        return True
    if pattern[0] not in letters:
        return False
    s=0
    indexes = get_indexes(board, pattern[0], index)
    for i in indexes:
        if i not in prev_index and find_pattern(board, get_neighbor_indexes(board, i), pattern[1:], i, prev_index+[i]):
            s+=1
    return s>0

def guess(board, pattern, words_found):
    if pattern == "q":
        return True
    if pattern in words:
        if find_pattern(board, board, pattern):
            if pattern in words_found:
                print("word already found")
                sleep(1)
            else:
                words_found.append(pattern)
        else:
            print("word not found")
            sleep(1)
    else:
        print("not a word")
        sleep(1)
    return False

board = randomise_game(letters)
all_words = [w for w in words if find_pattern(board, board, w)]
words_found = []
while True:
    sys("clear")
    print(sorted(words_found), str(len(words_found))+"/"+str(len(all_words)))
    print_board(board)
    if guess(board, input(" > "), words_found):
        break

print(words_found)
print(sorted(list(set(all_words).difference(set(words_found)))))
