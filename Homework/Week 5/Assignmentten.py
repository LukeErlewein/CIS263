# Assignment 10: Dynamic Programming
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

def knapsackSolver(values, weights, capacity):
    numItems = len(values)

    # Makes the table that is used to be able to dertermine the max value. with the number of items that each side of the table is looking at.
    dpTable = [[0] * (capacity + 1) for _ in range(numItems + 1)]

    for i in range(1, numItems + 1): # loops through all the items
        for currentWeight in range(capacity + 1): # loops for a number of times equal to the capacity.
            # If the current item can fit in the knapsack
            if weights[i - 1] <= currentWeight:
                # Compares the value of the knapsack with the value right above it in the table. 
                # Taking the max between including this item or not including this item.
                dpTable[i][currentWeight] = max(
                    dpTable[i - 1][currentWeight],
                    dpTable[i - 1][currentWeight - weights[i - 1]] + values[i - 1]
                )
            else:
                #if it dosent fit it just moves the previous value up.
                dpTable[i][currentWeight] = dpTable[i - 1][currentWeight]

    # Backtrack to find which items were used
    currentWeight = capacity
    itemsUsed = []

    # Start from the last item
    for i in range(numItems, 0, -1):
        # If the value is equal to i + i-1 then it was an item used.
        if dpTable[i][currentWeight] != dpTable[i - 1][currentWeight]:
            # Add the item to list of used items
            itemsUsed.append((values[i - 1], weights[i - 1]))
            currentWeight -= weights[i - 1]

    # bottom right is max value
    maxValue = dpTable[numItems][capacity]

    # Returns value and the list of items used in correct order
    return maxValue, itemsUsed[::-1]


def knapsackTest(capacity, items):
    #seperates the list into values and weights then calls the solver
    values, weights = zip(*items)
    maxValue, itemsUsed = knapsackSolver(values, weights, capacity)

    print(f"Maximum value: {maxValue}")
    print("Items used (value, weight):")
    for item in itemsUsed:
        print(item)


def main():
    items1 = [
        (1, 1),
        (6, 2),
        (18, 5),
        (22, 6),
        (28, 7)
    ]
    print(f"\nShort Knapsack Problem (Capacity = 11):")
    knapsackTest(11, items1)

    items2 = [
        (16808, 250),
        (50074, 659),
        (8931, 273),
        (27545, 879),
        (77924, 710),
        (64441, 166),
        (84493, 43),
        (7988, 504),
        (82328, 730),
        (78841, 613),
        (44304, 170),
        (17710, 158),
        (29561, 934),
        (93100, 279),
        (51817, 336),
        (99098, 827),
        (13513, 268),
        (23811, 634),
        (80980, 150),
        (36580, 822),
        (11968, 673),
        (1394, 337),
        (25486, 746),
        (25229, 92),
        (40195, 358),
        (35002, 154),
        (16709, 945),
        (15669, 491),
        (88125, 197),
        (9531, 904),
        (27723, 667),
        (28550, 25)
    ]
    print(f"\n\nLong Knapsack Problem (Capacity = 10000):")
    knapsackTest(10000, items2)


if __name__ == "__main__":
    main()
