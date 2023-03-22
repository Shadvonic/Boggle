import random
import string
from random import choice


class TrieNode:
    def __init__(self, item, children):
        self.char = item.upper()
        self.children = children
        self.visited = False

    def getChild(self, char):
        if self.children != None:
            for child in self.children:
                if child.char == char.upper():
                    return child
        return None


class makeTrie:
    def __init__(self, start=TrieNode(item="^", children=None)):
        self.root = start

    def insert(self, node, string):
        for char in string.upper():
            newNode = node.getChild(char)
            if newNode != None:
                node = newNode
            else:
                if node.children == None:
                    node.children = []
                newNode = TrieNode(char, children=None)
                node.children.append(newNode)
                node = newNode
        if node.children == None:
            node.children = []
        node.children.append(TrieNode("$", children=None))

    def search(self, node, string):
        isPartial = False
        isWord = False

        for char in string:
            newNode = node.getChild(char)
            if newNode == None:
                return (isWord, isPartial)
            else:
                node = newNode
        if len(node.children) == 1:
            if node.getChild("$") != None:
                isWord = True
            else:
                isPartial = True
        else:
            isPartial = True
            if node.getChild("$") != None:
                isWord = True
        return (isWord, isPartial)

    def buildDictionary(self, filePath):
        global fileError
        try:
            lines = open(filePath).readlines()
            for line in lines:
                if line != "\n" and line != "":
                    self.insert(self.root, line.rstrip("\n"))
        except:
            print("Error opening wordlist")
            fileError = True


def findWords(boardSetup, trie):
    for i in range(4):
        for j in range(4):
            adjacent(boardSetup, trie, i, j, boardSetup[i][j], [])


def adjacent(boardSetup, trie, row, col, currentString, usedIndexes):
    global computerFoundWords
    global playerFoundWords

    moves = [
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
        [-1, -1],
        [-1, 1],
        [1, -1],
        [1, 1],
    ]
    usedIndexes.append([row, col])

    for move in moves:
        tempRow = row + move[0]
        tempCol = col + move[1]
        if (
            tempRow >= 0
            and tempRow < 4
            and tempCol >= 0
            and tempCol < 4
            and [tempRow, tempCol] not in usedIndexes
        ):
            tempString = currentString + boardSetup[tempRow][tempCol]
            isWord, isPartial = trie.search(trie.root, tempString)

            if (
                isWord
                and tempString not in playerFoundWords
                and tempString not in computerFoundWords
                and len(tempString) >= 3
            ):
                computerFoundWords.append(tempString)
            if isPartial:
                adjacent(boardSetup, trie, tempRow, tempCol, tempString, usedIndexes)
                usedIndexes.pop()


def setUpBorad():
    output = ""
    for row in range(4):
        for col in range(4):
            output += str(boggleBoard[row][col]) + " "
        output += "\n"
    print(output)


def createBoard():
    global boggleBoard
    letterSelection = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(4):
        for j in range(4):
            boggleBoard[i][j] = random.choice(letterSelection)


def playGame():
    userInput = ""
    playerScore = 0
    print("press 0 to exit game")
    while userInput != "0":
        userInput = input("Guess a word: ")
        if len(userInput) < 3:
            print("Guess must be 3 letters long\n")
        else:
            if (
                myDict.search(myDict.root, userInput)[0] == True
                and userInput.upper() not in playerFoundWords
            ):
                playerFoundWords.append(userInput.upper())
                playerScore += 1
            elif userInput.upper() in playerFoundWords:
                print("Word has already been used!")
    findWords(boggleBoard, myDict)
    playerFoundWords.sort()
    computerFoundWords.sort()


def scoreTracker():
    playerScore = 0
    print("\nScore: " + str(playerScore))
    print("\nWords Found: ")
    if len(playerFoundWords) == 0:
        print("No words found")
    else:
        for playerWord in playerFoundWords:
            print(playerWord)
    print("\nComputer Words Found ")
    if len(computerFoundWords) == 0:
        print("No words found")
    else:
        for computerWord in computerFoundWords:
            print(computerWord)


def main():
    global fileError
    global boggleBoard
    global computerFoundWords
    global playerFoundWords
    global userInput
    global playerScore
    global myDict

    fileError = False
    computerFoundWords = []
    playerFoundWords = []
    boggleBoard = [
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
        ["", "", "", ""],
    ]

    myDict = makeTrie()
    myDict.buildDictionary("C:\\Users\\moxey\\Desktop\\mywords.txt")

    if fileError == True:
        return
    createBoard()
    setUpBorad()
    playGame()
    scoreTracker()


if __name__ == "__main__":
    main()
