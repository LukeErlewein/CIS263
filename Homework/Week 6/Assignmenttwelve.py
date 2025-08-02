# Assignment 12: Complexity Class Assignment 2
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

import random
import time

# Brute force for Set Partition problem
def setPartitionBruteForce(nums):
    totalSum = sum(nums)
    if totalSum % 2 != 0:
        return False

    # finds target sum
    targetSum = totalSum // 2
    n = len(nums)

    # Recursive generates all combinations of numbers in listSize
    def generateCombinations(start, listSize, current):
        if len(current) == listSize:
            return [current] 

        result = []
        for i in range(start, n):
            combos = generateCombinations(i + 1, listSize, current + [nums[i]])
            result.extend(combos)  # gets all the combos and adds them to list
        return result

    # Try all subset sizes from 1 to n
    for listSize in range(1, n + 1):
        allCombos = generateCombinations(0, listSize, [])
        for subset in allCombos:
            if sum(subset) == targetSum:
                return True

    return False


# Repeat of the Dynamic Programming implementation from Assignment Eleven.
def setPartitionDynamicProgramming(nums):
    totalSum = sum(nums)
    if totalSum % 2 != 0:
        return False

    targetSum = totalSum // 2
    dp = [False] * (targetSum + 1)
    dp[0] = True

    for num in nums:
        for i in range(targetSum, num - 1, -1):
            if dp[i - num]:
                dp[i] = True

    return dp[targetSum]

# Generates a random list of numbers.
# I added a modifier to make sure that the list is always even so it gets run.
def generateInput(size, maxVal=20):
    nums = [random.randint(1, maxVal) for _ in range(size)]
    totalSum = sum(nums)
    if totalSum % 2 != 0:
        nums[size-1] = nums[size-1]+1
    return nums

# tests both the brute force method and the dynamic programming method with the different constraints.
def timeTests(startSize=1, endSize=2, step=1, maxVal=10):
    print("N\tBrute Force Time\t\tDP Time")

    for size in range(startSize, endSize + 1, step):
        nums = generateInput(size, maxVal)

        # Time brute force
        startBF = time.perf_counter()
        setPartitionBruteForce(nums)
        bruteForceTime = time.perf_counter()

        # Time Dynamic Programming
        startDP = time.perf_counter()
        setPartitionDynamicProgramming(nums)
        DPTime = time.perf_counter()

        print(f"{size}\t{bruteForceTime-startBF:.6f}\t\t{DPTime-startDP:.6f}")

def main():
    print("\n\nTimes for inputs:")
    timeTests(startSize=3, endSize=30, step=3, maxVal=20)

if __name__ == "__main__":
    main()
