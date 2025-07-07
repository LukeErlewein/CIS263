# Assignment 5: Minimum Heap Analysis
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

import time
import random

N = 1000000 

# MIN HEAP
class MinHeapIncremental:
    def __init__(self):
        self.heap = [None]

    # inserts a value. It compares the value with the parent of it. If the value is less than the parent it swaps them and then repeats
    # until the parent is less than the child or it has reached the root.
    def insert(self, value):
        self.heap.append(value)
        i = len(self.heap) - 1
        while i > 1 and self.heap[i] < self.heap[i // 2]:
            self.heap[i], self.heap[i // 2] = self.heap[i // 2], self.heap[i]
            i //= 2

# checks node i for a value. Then checks the child nodes of i. If node i is smaller than the child nodes its all good.
# If not then it switches with the child node and then checks the child node after the switch to check the entire branch.
# all nodes will be checked as buildMinHeap builds from the last parent node up.
def heapify(arr, n, i):
    smallest = i
    l = 2 * i
    r = 2 * i + 1

    if l <= n and arr[l] < arr[smallest]:
        smallest = l
    if r <= n and arr[r] < arr[smallest]:
        smallest = r

    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify(arr, n, smallest)


def buildMinHeap(arr):
    n = len(arr) - 1
    for i in range(n // 2, 0, -1):
        heapify(arr, n, i)

def generateAscending():
    return list(range(N))

def generateDescending():
    return list(range(N, 0, -1))

def generateRandom():
    return [random.randint(0, N * 10) for _ in range(N)]


def runTest(inputList, label):
    print(f"\n{label}")

    # Incremental
    start = time.time()
    heap = MinHeapIncremental()
    for value in inputList:
        heap.insert(value)
    end = time.time()
    print(f"Incremental: {end - start:.5f} seconds")

    # Heapify
    heapArray = [None] + inputList[:] 
    start = time.time()
    buildMinHeap(heapArray)
    end = time.time()
    print(f"Heapify: {end - start:.5f} seconds")


def main():
    random.seed(time.time())

    runTest(generateAscending(), "Ascending")
    runTest(generateDescending(), "Descending")
    runTest(generateRandom(), "Random")


if __name__ == "__main__":
    main()
