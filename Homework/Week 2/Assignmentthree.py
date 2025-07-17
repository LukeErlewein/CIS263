# Assignment 3: Binary Search Trees
# Student: Luke Erlewein
# Professor: Dr. Denton Bobeldyk
# Class: CIS 263 Summer 2025

# Part 1
class TreeNode:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

# I refer to the roots as root = TreeNode in the BST set up functions in part 4.

# Part 2
def inorder(node):
    if node:
        inorder(node.left)
        print(node.value, end=" ")
        inorder(node.right)

def preorder(node):
    if node:
        print(node.value, end=" ")
        preorder(node.left)
        preorder(node.right)

def postorder(node):
    if node:
        postorder(node.left)
        postorder(node.right)
        print(node.value, end=" ")

# Part 3
# determines if it is a BST by looking at the minimum and maximum node value so far on the branch. On the left branches the maximum node should be the parent of the left branch.
# when looking at the right branch the minimum value should be the parent node of that branch.
def isBST(node, min = float('-inf'), max = float('inf')):
    if node is None:
        return True
    if node.value <= min or node.value >= max:
        return False
    return isBST(node.left, min, node.value) and isBST(node.right, node.value, max)


# Part 4
# Find minimum node (used for successor)
def findMinNode(node):
    while node.left:
        node = node.left
    return node

# Find a node by value
def findNode(root, val):
    if root is None or root.value == val:
        return root
    elif val < root.value:
        return findNode(root.left, val)
    else:
        return findNode(root.right, val)

# Find successor
# successor is the next highest possible value in the entire tree
def findSuccessor(root, val):
    node = findNode(root, val)
    if node is None:
        return None
    if node.right:
        return findMinNode(node.right)
    successor = None
    parent = root
    while parent != node:
        if node.value < parent.value:
            successor = parent
            parent = parent.left
        else:
            parent = parent.right
    return successor


# setups for BSTs
def validBSTsetup():
    nodes = {val: TreeNode(val) for val in [20, 10, 30, 5, 15, 25, 35, 13]}
    root = nodes[20]
    root.left = nodes[10]; nodes[10].parent = root
    root.right = nodes[30]; nodes[30].parent = root
    nodes[10].left = nodes[5]; nodes[5].parent = nodes[10]
    nodes[10].right = nodes[15]; nodes[15].parent = nodes[10]
    nodes[15].left = nodes[13]; nodes[13].parent = nodes[15]
    nodes[30].left = nodes[25]; nodes[25].parent = nodes[30]
    nodes[30].right = nodes[35]; nodes[35].parent = nodes[30]
    return root

# invalid BST because of it sets up 25 as the right child of 15.
def invalidBSTSetup():
    nodes = {val: TreeNode(val) for val in [20, 10, 30, 5, 15, 25, 35, 12]}
    root = nodes[20]
    root.left = nodes[10]; nodes[10].parent = root
    root.right = nodes[30]; nodes[30].parent = root
    nodes[10].left = nodes[5]; nodes[5].parent = nodes[10]
    nodes[10].right = nodes[15]; nodes[15].parent = nodes[10]
    nodes[15].left = nodes[12]; nodes[12].parent = nodes[15]
    nodes[15].right = nodes[25]; nodes[25].parent = nodes[15]
    nodes[30].right = nodes[35]; nodes[35].parent = nodes[30]
    return root

# Print tree information
def testTree(name, root, targetNode):
    print(f"{name}:\n")
    print("Inorder:   ", end=""); inorder(root); print()
    print("Preorder:  ", end=""); preorder(root); print()
    print("Postorder: ", end=""); postorder(root); print()
    print("Is BST?:   ", isBST(root))
    successor = findSuccessor(root, targetNode)
    print(f"Successor of {targetNode} is {successor.value if successor else 'None'}\n\n\n")

# Main function to run everything
def main():
    validBST = validBSTsetup()
    invalidBST = invalidBSTSetup()
    
    testTree("Valid BST", validBST, 15)
    testTree("Invalid BST", invalidBST, 15)

if __name__ == "__main__":
    main()
