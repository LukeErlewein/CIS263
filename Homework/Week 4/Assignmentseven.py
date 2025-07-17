import random
import time

# PART 1

# Generates a list of random items with a start and end time
def generateActivityList(n, max_time=100):
    activities = []
    for _ in range(n):
        start = random.randint(0, max_time - 1)
        end = random.randint(start + 1, max_time)
        activities.append((start, end))
    return sorted(activities, key=lambda x: x[0]) # sort by start time

# Brute Force
# Checks all possible activity combinations and chooses the best possible one.
def bruteForceActivities(activities):
    n = len(activities)
    optimalList = []

    # Helper function to check if a list of activities is valid (non-overlapping)
    def validActivities(schedule):
        schedule.sort(key=lambda x: x[0])  # sort by start time
        for i in range(len(schedule) - 1):
            if schedule[i][1] > schedule[i + 1][0]:
                return False
        return True

    # Recursive function to generate all subsets and check the best one
    def generationOptimize(index, currentOptimal):
        nonlocal optimalList

        # base case: if the current list is more optimal than the previous one it replaces it.
        if index == n:
            if validActivities(currentOptimal) and len(currentOptimal) > len(optimalList):
                optimalList = currentOptimal[:]
            return

        # it will add the current item to the schedule. It will continue adding items until it comes up with a most optimal route using this item.
        # at the end it will reach base case and then if it is NOT optimal it will get rid of the current item and conintue to the next one.
        currentOptimal.append(activities[index])
        generationOptimize(index + 1, currentOptimal)
        currentOptimal.pop()

        # if it gets to this point it will ignore the previous item in the schedule and continue on.
        generationOptimize(index + 1, currentOptimal)

    # starts the optimization at index 0
    generationOptimize(0, [])
    return optimalList

# Greedy solution will always pick the items that end first.
def greedySelection(activities):
    activities.sort(key=lambda x: x[1])  # sort by end time
    result = []
    lastEndTime = 0

    for start, end in activities:
        if start >= lastEndTime:
            result.append((start, end))
            lastEndTime = end

    return result

# PART 2

# Generates an array with both positive and negative integers
def generateArray(n, low=-100, high=100):
    return [random.randint(low, high) for _ in range(n)]

# Brute Force: check every possible subarray and calculate its sum
def bruteForceMaxSubArray(arr):
    maxSum = 0
    bestStart = 0
    bestEnd = 0

    for i in range(len(arr)):
        currentSum = 0
        for j in range(i, len(arr)):
            currentSum += arr[j]
            if currentSum > maxSum:
                maxSum = currentSum
                bestStart = i
                bestEnd = j

    return maxSum, arr[bestStart:bestEnd + 1]

# Divide and Conquer approach to find the maximum subarray
def divConMaxSubArray(arr):
    def helper(left, right):
        #base case. Left and right are equal to each other meaning there is only one item in the sub array
        if left == right:
            return arr[left], [arr[left]]

        mid = (left + right) // 2

        # Find max subarray on the left and right sides
        leftSum, leftSubArray = helper(left, mid)
        rightSum, rightSubArray = helper(mid + 1, right)

        # finds best array on the left side of mid.
        maxLeftSum = float('-inf')
        tempSum = 0
        maxLeftIndex = mid
        for i in range(mid, left - 1, -1):
            tempSum += arr[i]
            if tempSum > maxLeftSum:
                maxLeftSum = tempSum
                maxLeftIndex = i

        # finds the best array on the right side of mid.
        maxRightSum = float('-inf')
        tempSum = 0
        maxRightIndex = mid + 1
        for i in range(mid + 1, right + 1):
            tempSum += arr[i]
            if tempSum > maxRightSum:
                maxRightSum = tempSum
                maxRightIndex = i

        # builds the best array from the left side and the right side and then combines them.
        crossSum = maxLeftSum + maxRightSum
        crossSubArray = arr[maxLeftIndex:maxRightIndex + 1]

        # Return the best of the three options
        maxSum = max(leftSum, rightSum, crossSum)
        if maxSum == leftSum:
            return leftSum, leftSubArray
        elif maxSum == rightSum:
            return rightSum, rightSubArray
        else:
            return crossSum, crossSubArray

    return helper(0, len(arr) - 1)


def testActivitySelection():
    activities = generateActivityList(25)

    print("Number of activities in list: 25\nActivity time range between 0 and 100\n")
    # Brute Force
    startTime = time.time()
    bruteResult = bruteForceActivities(activities)
    bruteTime = time.time() - startTime
    print(f"Brute Force: {len(bruteResult)} activities selected in {bruteTime:.5f} seconds")

    #activities = generateActivityList(2500)
    
    # Greedy
    startTime = time.time()
    greedyResult = greedySelection(activities)
    greedyTime = time.time() - startTime
    print(f"Greedy: {len(greedyResult)} activities selected in {greedyTime:.7f} seconds")

def testMaxSubArray():
    array = generateArray(10000)

    print("\nNumber of items in array: 10000\n")
    # Brute Force
    startTime = time.time()
    brute_sum, _ = bruteForceMaxSubArray(array)
    bruteTime = time.time() - startTime
    print(f"Brute Force: max sum = {brute_sum}, time = {bruteTime:.5f} seconds")

    # Divide and Conquer
    startTime = time.time()
    divConSum, _ = divConMaxSubArray(array)
    divConTime = time.time() - startTime
    print(f"Divide & Conquer: max sum = {divConSum}, time = {divConTime:.5f} seconds")

if __name__ == "__main__":
    testActivitySelection()
    testMaxSubArray()
