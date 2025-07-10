# Assignment 6: Hash Functions
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

import random

TableSize = 10001
ListSize = 500
HashMod = 300

random.seed(616)
InsertList = [random.randint(1, 100000) for _ in range(ListSize)]

def linearProbing():
    hashTable = [None] * TableSize
    numCollide = 0

    for currentVar in InsertList:
        index = currentVar % HashMod

        while hashTable[index] is not None:
            numCollide += 1
            index = (index + 1) % TableSize
        hashTable[index] = currentVar

    return numCollide

def quadraticProbing(c1=1, c2=2):
    hashTable = [None] * TableSize
    numCollide = 0

    for currentVar in InsertList:
        index = currentVar % HashMod
        i = 0
        while 1:
            newIndex = (index + c1 * i + c2 * i^2) % TableSize
            if hashTable[newIndex] is None:
                hashTable[newIndex] = currentVar
                break
            numCollide += 1
            i += 1

    return numCollide


# Second hash function for double hashing
def h2(x):
    return 9973 - (x % 9973)

def doubleHash():
    hashTable = [None] * TableSize
    numCollide = 0

    for currentVar in InsertList:
        index1 = currentVar % HashMod
        step = h2(currentVar)
        i = 0
        while True:
            newIndex = (index1 + (i * step)) % TableSize
            if hashTable[newIndex] is None:
                hashTable[newIndex] = currentVar
                break
            numCollide += 1
            i += 1

    return numCollide

def modifiedLinearProbing():
    hashTable = [None] * TableSize
    numCollide = 0

    for currentVar in InsertList:
        index = currentVar % HashMod

        while hashTable[index] is not None:
            numCollide += 1
            index = (index + 10) % TableSize
        hashTable[index] = currentVar

    return numCollide


linear = linearProbing()
quadratic = quadraticProbing()
double = doubleHash()
modifiedLinear = modifiedLinearProbing()

print(f"numCollide (Linear Probing): {linear}")
print(f"numCollide (Quadratic Probing): {quadratic}")
print(f"numCollide (Double Hash): {double}")
print(f"numCollide (Modified Linear Probing): {modifiedLinear}")
