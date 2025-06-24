# Assignment 1: Insertion Sort
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

#this function finds the correct place to put the "num" number and then inserts it into the correct position
def insertionSort(inputList, num):
    i = len(inputList) - 1
    inputList.append(num)
    while i >= 0 and inputList[i] > num:
        inputList[i + 1] = inputList[i]
        i -= 1
    inputList[i + 1] = num


def main():
    sortedList = []
    for i in range(8):
        num = int(input(f"Enter next integer: "))
        insertionSort(sortedList, num)
        print("Current sorted array:", sortedList)


if __name__ == "__main__":
    main()
