# Gia Buu Luong, Aymaan Mohammed
# ECE 241 - Project 3: App2, App3, App4 and App5

from Movie import Movie
from MovieList import MovieList
from Queue import Queue
import random
import math
import tkinter as tk


class Node:
    def __init__(self, movie, index=0):
        self.movie = movie
        self.left = None
        self.right = None
        self.index = index  # level-order position: left=2*i+1, right=2*i+2


class MovieBST:
    def __init__(self, filename):
        self.__root = None
        self.__size = 0
        self.__maxIndex = -1  # largest level-order index, kept up to date in insert

        with open(filename, "r") as file:
            for line in file:
                if line.strip():
                    movie_id, year, title = line.strip().split(";", 2)
                    self.insert(Movie(int(movie_id), int(year), title.strip()))

    def insert(self, movie):
        if self.__root is None:
            self.__root = Node(movie, 0)
            self.__size += 1
            self.__maxIndex = max(self.__maxIndex, 0)
        else:
            self.__insert(self.__root, movie)

    def __insert(self, node, movie):
        # Tree is sorted by ID number
        if movie.getID() < node.movie.getID():
            if node.left is None:
                node.left = Node(movie, 2 * node.index + 1)
                self.__size += 1
                self.__maxIndex = max(self.__maxIndex, node.left.index)
            else:
                self.__insert(node.left, movie)
        elif movie.getID() > node.movie.getID():
            if node.right is None:
                node.right = Node(movie, 2 * node.index + 2)
                self.__size += 1
                self.__maxIndex = max(self.__maxIndex, node.right.index)
            else:
                self.__insert(node.right, movie)

    def getSize(self):
        return self.__size

    def getMaxIndex(self):
        return self.__maxIndex

    def getMaxLevel(self):
        # Level d holds indexes 2^d-1 .. 2^(d+1)-2, so the deepest level is
        # floor(log2(maxIndex+1)). The root is at level 0.
        if self.__maxIndex < 0:
            return -1
        return int(math.log2(self.__maxIndex + 1))

    def search(self, movie_id):
        current = self.__root

        while current is not None:
            if movie_id == current.movie.getID():
                return current.movie
            elif movie_id < current.movie.getID():
                current = current.left
            else:
                current = current.right

        return None

    def displayInOrder(self):
        print("Display in order " + str(self.__size) + " items by ID")
        self.__displayInOrder(self.__root)

    def __displayInOrder(self, node):
        if node is not None:
            self.__displayInOrder(node.left)
            print(node.movie)
            self.__displayInOrder(node.right)

    def show(self):
        print("The BSTree looks like:")
        self.__show(self.__root, 0)

    def __show(self, node, level):
        if node is not None:
            # Right subtree appears above the root in the sideways tree.
            self.__show(node.right, level + 1)
            print("      " * level + str(node.movie.getID())
                  + "(" + str(node.index) + ")")
            self.__show(node.left, level + 1)

    def extractListInOrder(self, word):
        print("Begin sublist extraction for word:" + word
              + " using in-order traversal")
        userList = MovieList()
        self.__extractListInOrder(self.__root, word.lower(), userList)
        return userList

    def __extractListInOrder(self, node, word, userList):
        if node is not None:
            self.__extractListInOrder(node.left, word, userList)
            # Case-insensitive match on whole words of the title
            if word in node.movie.getTitle().lower().split():
                userList.append(node.movie)
            self.__extractListInOrder(node.right, word, userList)

    def displayLevelOrder(self):
        # Breadth-first traversal with a queue (not recursive). Each visited
        # node is printed and stored in the list at its level-order index.
        levelList = [None] * (self.__maxIndex + 1)
        if self.__root is None:
            return levelList

        queue = Queue(self.__size)
        queue.enqueue(self.__root)
        while not queue.isEmpty():
            node = queue.dequeue()
            print(node.movie)
            levelList[node.index] = node.movie
            if node.left is not None:
                queue.enqueue(node.left)
            if node.right is not None:
                queue.enqueue(node.right)
        return levelList

    @staticmethod
    def plotBST(listDB):
        # Draw the whole complete binary tree in gray, then highlight the
        # nodes present in the level-order list (and their links) in blue.
        n = len(listDB)
        if n == 0:
            return
        levels = int(math.log2(n)) + 1
        cbtSize = 2 ** levels - 1

        width, height, margin = 1400, 80 * levels + 40, 20
        x, y = [], []
        for i in range(cbtSize):
            level = int(math.log2(i + 1))
            pos = i - (2 ** level - 1)  # position within its level
            x.append(margin + (pos + 0.5) * (width - 2 * margin) / 2 ** level)
            y.append(margin + 10 + level * 80)

        def occupied(i):
            return i < n and listDB[i] is not None

        window = tk.Tk()
        window.title("BST plot")
        canvas = tk.Canvas(window, width=width, height=height, bg="white")
        canvas.pack()

        r = 4
        # Lines first so the nodes are drawn on top of them; gray before
        # blue so the highlighted links are never covered
        for highlight in (False, True):
            for i in range(1, cbtSize):
                parent = (i - 1) // 2
                if (occupied(i) and occupied(parent)) == highlight:
                    color = "blue" if highlight else "gray"
                    canvas.create_line(x[parent], y[parent], x[i], y[i],
                                       fill=color)
        for i in range(cbtSize):
            color = "blue" if occupied(i) else "gray"
            canvas.create_oval(x[i] - r, y[i] - r, x[i] + r, y[i] + r,
                               fill=color, outline=color)

        window.mainloop()
