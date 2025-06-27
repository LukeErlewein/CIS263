import time
import math

# function to return the time that the test function wiht N takes to run.
def runTest(n, func):
    start = time.time()
    func(n)
    end = time.time()
    return end - start

def testA(n):
    someVariable = 1.0
    for i in range(n):
        someVariable = math.log(someVariable) + 3

def testB(n):
    someVariable = 1.0
    for i in range(n):
        for j in range(n):
            someVariable = math.log(someVariable) + 3

def testC(n):
    someVariable = 1.0
    for i in range(n):
        for j in range(i):
            someVariable = math.log(someVariable) + 3

def testD(n):
    someVariable = 1.0
    for i in range(n):
        for j in range(i):
            if j % 2 == 0:
                someVariable = math.log(someVariable) + 3

# iterates through the list of Ns and does the time test for each one.
def main():
    nList = [1000, 5000, 10000]

    for n in nList:
        print(f"\nn = {n}")
        print(f"A (O(n)):    {runTest(n, testA):.5f} seconds")
        print(f"B (O(n^2)):  {runTest(n, testB):.5f} seconds")
        print(f"C (O(n^2)):  {runTest(n, testC):.5f} seconds")
        print(f"D (O(n^2)):  {runTest(n, testD):.5f} seconds")


if __name__ == "__main__":
    main()
