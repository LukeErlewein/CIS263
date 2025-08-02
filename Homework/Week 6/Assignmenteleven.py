# Assignment 11: Complexity Class Assignment
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

# For the logic of this I referenced this code here.
# https://leetcode.com/problems/partition-equal-subset-sum/solutions/6847382/video-detailed-explanation-with-dynamic-programming/

def setPartition(nums):
    totalSum = sum(nums)

    # if total sum is odd it cant be partitioned
    if totalSum % 2 != 0:
        return False

    targetSum = totalSum // 2
    n = len(nums)

    # Create a Dynamic Programming table but a 1d version rather than 2d.
    # The table is set up so that it is all false except for index 0.
    # When a number is analyzed it will iterate down until it hits the number starting at the target sum.
    # While subtracting if the place on the table that is the current iterator minus the number being looked at is true,
    # it will make the place on the table that the iterator is at true.
    # at the end it will check the target sums point on the table. If it is true that means that there can be a subset that equals it.

    # EXAMPLE:
    # If we have the list [2, 4, 12, 6], It will start with two and do i-2 with i starting at 12 until i hits 0 at which point it will see that dp[0] is true.
    # at that point it will make dp[2] true.
    # It will continue on with the number 4. It will do the same thing of i-4 starting at 12But then once i reaches 6 it will see that dp[2] = true.
    # It will then make dp[6] = True. Basically the final dp list after iterating through the entire list of numbers will show what sums you can make using the numbers in the list.

    dp = [False] * (targetSum + 1)
    dp[0] = True

    for num in nums:
        for i in range(targetSum, num - 1, -1):
            if dp[i - num]:
                dp[i] = True

    return dp[targetSum]


def main():
    testCases = [
        ([2, 4, 12, 6], True),      # Can be split into [2, 4, 6] and [12]
        ([1, 2, 3, 5], False),      # Can't be split
        ([3, 1, 1, 2, 2, 1], True), # Can be split into [3,1,1] and [2,2,1]
        ([2, 2, 4, 5], False),      # Odd value
    ]

    for i, (nums, expectedResult) in enumerate(testCases):
        result = setPartition(nums)
        print(f"Input = {nums}")
        print(f"Expecting Result = {expectedResult}, Actual Result = {result}\n\n")


if __name__ == "__main__":
    main()
