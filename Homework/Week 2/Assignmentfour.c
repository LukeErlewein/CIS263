// Assignment 4: Red/Black Binary Trees
// Student: Luke Erlewein
// Professor: Dr. Denton Bobeldyk
// Class: CIS 263 Summer 2025
// Source for the printing of the ascii Binary trees: https://gist.github.com/ximik777/e04e5a9f0548a2f41cb09530924bdd9a

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef enum { RED, BLACK } Color;

typedef struct Tree Tree;

typedef struct Tree {
    int element;
    Color color;
    struct Tree *left, *right, *parent;
} Tree;

// Function prototypes
Tree *rbInsert(int value, Tree *root);
void rbInsertFixup(Tree **root, Tree *node);
Tree *leftRotate(Tree *root, Tree *x);
Tree *rightRotate(Tree *root, Tree *x);


Tree *findMin(Tree *t) {
    if (t == NULL) {
        return NULL;
    } else if (t->left == NULL) {
        return t;
    } else {
        return findMin(t->left);
    }
}

Tree *find(int elem, Tree *t) {
    if (t == NULL) {
        return NULL;
    }

    if (elem < t->element) {
        return find(elem, t->left);
    } else if (elem > t->element) {
        return find(elem, t->right);
    } else {
        return t;
    }
}


//printing tree in ascii

typedef struct asciinode_struct asciinode;

struct asciinode_struct {
    asciinode *left, *right;

    //length of the edge from this node to its children
    int edge_length;

    int height;

    int lablen;

    //-1=I am left, 0=I am root, 1=right
    int parent_dir;

    //max supported unit32 in dec, 10 digits max
    char label[11];
};


#define MAX_HEIGHT 1000
int lprofile[MAX_HEIGHT];
int rprofile[MAX_HEIGHT];
#define INFINITY (1<<20)

//adjust gap between left and right nodes
int gap = 3;

//used for printing next node in the same level,
//this is the x coordinate of the next char printed
int print_next;

int MIN(int X, int Y) {
    return ((X) < (Y)) ? (X) : (Y);
}

int MAX(int X, int Y) {
    return ((X) > (Y)) ? (X) : (Y);
}

asciinode *build_ascii_tree_recursive(Tree *t) {
    asciinode *node;
    if (t == NULL) return NULL;

    node = malloc(sizeof(asciinode));
    node->left = build_ascii_tree_recursive(t->left);
    node->right = build_ascii_tree_recursive(t->right);

    if (node->left != NULL) node->left->parent_dir = -1;
    if (node->right != NULL) node->right->parent_dir = 1;

    // Show color in label
    sprintf(node->label, "%d%c", t->element, t->color == RED ? 'R' : 'B');
    node->lablen = (int) strlen(node->label);

    return node;
}


//Copy the tree into the ascii node structre
asciinode *build_ascii_tree(Tree *t) {
    asciinode *node;
    if (t == NULL) return NULL;
    node = build_ascii_tree_recursive(t);
    node->parent_dir = 0;
    return node;
}

//Free all the nodes of the given tree
void free_ascii_tree(asciinode *node) {
    if (node == NULL) return;
    free_ascii_tree(node->left);
    free_ascii_tree(node->right);
    free(node);
}

//The following function fills in the lprofile array for the given tree.
//It assumes that the center of the label of the root of this tree
//is located at a position (x,y).  It assumes that the edge_length
//fields have been computed for this tree.
void compute_lprofile(asciinode *node, int x, int y) {
    int i, isleft;
    if (node == NULL) return;
    isleft = (node->parent_dir == -1);
    lprofile[y] = MIN(lprofile[y], x - ((node->lablen - isleft) / 2));
    if (node->left != NULL) {
        for (i = 1; i <= node->edge_length && y + i < MAX_HEIGHT; i++) {
            lprofile[y + i] = MIN(lprofile[y + i], x - i);
        }
    }
    compute_lprofile(node->left, x - node->edge_length - 1, y + node->edge_length + 1);
    compute_lprofile(node->right, x + node->edge_length + 1, y + node->edge_length + 1);
}

void compute_rprofile(asciinode *node, int x, int y) {
    int i, notleft;
    if (node == NULL) return;
    notleft = (node->parent_dir != -1);
    rprofile[y] = MAX(rprofile[y], x + ((node->lablen - notleft) / 2));
    if (node->right != NULL) {
        for (i = 1; i <= node->edge_length && y + i < MAX_HEIGHT; i++) {
            rprofile[y + i] = MAX(rprofile[y + i], x + i);
        }
    }
    compute_rprofile(node->left, x - node->edge_length - 1, y + node->edge_length + 1);
    compute_rprofile(node->right, x + node->edge_length + 1, y + node->edge_length + 1);
}

//This function fills in the edge_length and
//height fields of the specified tree
void compute_edge_lengths(asciinode *node) {
    int h, hmin, i, delta;
    if (node == NULL) return;
    compute_edge_lengths(node->left);
    compute_edge_lengths(node->right);

    /* first fill in the edge_length of node */
    if (node->right == NULL && node->left == NULL) {
        node->edge_length = 0;
    } else {
        if (node->left != NULL) {
            for (i = 0; i < node->left->height && i < MAX_HEIGHT; i++) {
                rprofile[i] = -INFINITY;
            }
            compute_rprofile(node->left, 0, 0);
            hmin = node->left->height;
        } else {
            hmin = 0;
        }
        if (node->right != NULL) {
            for (i = 0; i < node->right->height && i < MAX_HEIGHT; i++) {
                lprofile[i] = INFINITY;
            }
            compute_lprofile(node->right, 0, 0);
            hmin = MIN(node->right->height, hmin);
        } else {
            hmin = 0;
        }
        delta = 4;
        for (i = 0; i < hmin; i++) {
            delta = MAX(delta, gap + 1 + rprofile[i] - lprofile[i]);
        }

        //If the node has two children of height 1, then we allow the
        //two leaves to be within 1, instead of 2
        if (((node->left != NULL && node->left->height == 1) ||
             (node->right != NULL && node->right->height == 1)) && delta > 4) {
            delta--;
        }

        node->edge_length = ((delta + 1) / 2) - 1;
    }

    //now fill in the height of node
    h = 1;
    if (node->left != NULL) {
        h = MAX(node->left->height + node->edge_length + 1, h);
    }
    if (node->right != NULL) {
        h = MAX(node->right->height + node->edge_length + 1, h);
    }
    node->height = h;
}

//This function prints the given level of the given tree, assuming
//that the node has the given x cordinate.
void print_level(asciinode *node, int x, int level) {
    int i, isleft;
    if (node == NULL) return;
    isleft = (node->parent_dir == -1);
    if (level == 0) {
        for (i = 0; i < (x - print_next - ((node->lablen - isleft) / 2)); i++) {
            printf(" ");
        }
        print_next += i;
        printf("%s", node->label);
        print_next += node->lablen;
    } else if (node->edge_length >= level) {
        if (node->left != NULL) {
            for (i = 0; i < (x - print_next - (level)); i++) {
                printf(" ");
            }
            print_next += i;
            printf("/");
            print_next++;
        }
        if (node->right != NULL) {
            for (i = 0; i < (x - print_next + (level)); i++) {
                printf(" ");
            }
            print_next += i;
            printf("\\");
            print_next++;
        }
    } else {
        print_level(node->left,
                    x - node->edge_length - 1,
                    level - node->edge_length - 1);
        print_level(node->right,
                    x + node->edge_length + 1,
                    level - node->edge_length - 1);
    }
}

//prints ascii tree for given Tree structure
void print_ascii_tree(Tree *t) {
    asciinode *proot;
    int xmin, i;
    if (t == NULL) return;
    proot = build_ascii_tree(t);
    compute_edge_lengths(proot);
    for (i = 0; i < proot->height && i < MAX_HEIGHT; i++) {
        lprofile[i] = INFINITY;
    }
    compute_lprofile(proot, 0, 0);
    xmin = 0;
    for (i = 0; i < proot->height && i < MAX_HEIGHT; i++) {
        xmin = MIN(xmin, lprofile[i]);
    }
    for (i = 0; i < proot->height; i++) {
        print_next = 0;
        print_level(proot, -xmin, i);
        printf("\n");
    }
    if (proot->height >= MAX_HEIGHT) {
        printf("(This tree is taller than %d, and may be drawn incorrectly.)\n", MAX_HEIGHT);
    }
    free_ascii_tree(proot);
}

// Create a new node
Tree *new_node(int value) {
    Tree *n = malloc(sizeof(Tree));
    n->element = value;
    n->color = RED;
    n->left = n->right = n->parent = NULL;
    return n;
}

Tree *rbInsert(int value, Tree *root)
{
    Tree *z = new_node(value), *y = NULL, *x = root;

    while (x != NULL)
    {
        y = x;
        if (value < x->element)
            x = x->left;
        else if (value > x->element)
            x = x->right;
        else
        {
            free(z);
            return root;
        }
    }
    z->parent = y;
    if (y == NULL)
        root = z;
    else if (value < y->element)
        y->left = z;
    else
        y->right = z;

    z->left = NULL;
    z->right = NULL;
    z->color = RED;
    rbInsertFixup(&root, z);
    return root;
}

void rbInsertFixup(Tree **root, Tree *z)
{
    while (z->parent && z->parent->color == RED)
    {
        Tree *gp = z->parent->parent;
        if (z->parent == gp->left)
        {
            Tree *y = gp->right;
            if (y && y->color == RED)
            {
                // Case 1: Parent sibling is red
                printf("rbInsertFixup Case 1: Recoloring\n");
                z->parent->color = BLACK;
                y->color = BLACK;
                gp->color = RED;
                z = gp;
            }
            else
            {
                if (z == z->parent->right)
                {
                    // Case 2: z is right child
                    printf("rbInsertFixup Case 2: Left Rotation\n");
                    z = z->parent;
                    *root = leftRotate(*root, z);
                }
                // Case 3: z is left child
                printf("rbInsertFixup Case 3: Right Rotation and Recolor\n");
                z->parent->color = BLACK;
                gp->color = RED;
                *root = rightRotate(*root, gp);
            }
        }
        else
        {
            // Symmetric cases for right side
            Tree *y = gp->left;
            if (y && y->color == RED)
            {
                printf("rbInsertFixup Case 1: Recoloring\n");
                z->parent->color = BLACK;
                y->color = BLACK;
                gp->color = RED;
                z = gp;
            }
            else
            {
                if (z == z->parent->left)
                {
                    printf("rbInsertFixup Case 2: Right Rotation\n");
                    z = z->parent;
                    *root = rightRotate(*root, z);
                }
                printf("rbInsertFixup Case 3: Left Rotation and Recolor\n");
                z->parent->color = BLACK;
                gp->color = RED;
                *root = leftRotate(*root, gp);
            }
        }
    }
    (*root)->color = BLACK;
}


Tree *leftRotate(Tree *root, Tree *x) {
    Tree *y = x->right; // set y
    x->right = y->left; // turn y's left subtree to x's right subtree
    if (y->left) y->left->parent = x;
    y->parent = x->parent; // link x's parent to y
    if (!x->parent)
        root = y;
    else if (x == x->parent->left)
        x->parent->left = y;
    else
        x->parent->right = y;
    y->left = x; // put x on y's left
    x->parent = y;
    return root;
}

Tree *rightRotate(Tree *root, Tree *x) {
    Tree *y = x->left; // set y
    x->left = y->right; // turn x's left subtree to y's right subtree
    if (y->right) y->right->parent = x;
    y->parent = x->parent; // link x's parent to y
    if (!x->parent)
        root = y;
    else if (x == x->parent->right)
        x->parent->right = y;
    else
        x->parent->left = y;
    y->right = x; // put x on y's right
    x->parent = y;
    return root;
}

Tree *rbTransplant(Tree *root, Tree *u, Tree *v)
{
    if (u->parent == NULL)
    {
        root = v;
    } 
    else if (u == u->parent->left)
    {
        u->parent->left = v;
    }
    else
    {
        u->parent->right = v;
    }
    if (v != NULL)
        v->parent = u->parent;
    return root;
}

Tree *rbDeleteFixup(Tree *root, Tree *x, Tree *xParent);

Tree *rbDelete(Tree *root, int key)
{
    Tree *z = root;
    while (z != NULL && z->element != key)
    {
        if (key < z->element)
            z = z->left;
        else
            z = z->right;
    }

    if (z == NULL)
    {
        printf("Key %d not found.\n", key);
        return root;
    }

    Tree *y = z;
    Color yOriginalColor = y->color;
    Tree *x, *xParent;

    if (z->left == NULL)
    {
        x = z->right;
        xParent = z->parent;
        root = rbTransplant(root, z, z->right);
    }
    else if (z->right == NULL)
    {
        x = z->left;
        xParent = z->parent;
        root = rbTransplant(root, z, z->left);
    }
    else
    {
        y = findMin(z->right);
        yOriginalColor = y->color;
        x = y->right;
        if (y->parent == z)
        {
            if (x != NULL)
                x->parent = y;
            xParent = y;
        }
        else
        {
            root = rbTransplant(root, y, y->right);
            y->right = z->right;
            y->right->parent = y;
            xParent = y->parent;
        }

        root = rbTransplant(root, z, y);
        y->left = z->left;
        y->left->parent = y;
        y->color = z->color;
    }

    free(z);

    if (yOriginalColor == BLACK)
    {
        root = rbDeleteFixup(root, x, xParent);
    }

    return root;
}

Tree *rbDeleteFixup(Tree *root, Tree *x, Tree *xParent)
{
    while ((x == NULL || x->color == BLACK) && x != root)
    {
        if (x == xParent->left)
        {
            Tree *w = xParent->right;
            if (w && w->color == RED)
            {
                printf("Delete Case 1: Left Rotation and Recolor\n");
                //sibling is red. 
                w->color = BLACK;
                xParent->color = RED;
                root = leftRotate(root, xParent);
                w = xParent->right;
            }
            if ((w->left == NULL || w->left->color == BLACK) &&
                (w->right == NULL || w->right->color == BLACK))
                {
                // parent is black and both childred are black.
                printf("Delete Case 2: Recoloring\n");
                w->color = RED;
                x = xParent;
                xParent = x->parent;
            }
            else
            {
                if (w->right == NULL || w->right->color == BLACK)
                {
                    printf("Delete Case 3: Right Rotation and Recolor\n");
                    if (w->left != NULL) w->left->color = BLACK;
                    w->color = RED;
                    root = rightRotate(root, w);
                    w = xParent->right;
                }
                printf("Delete Case 4: Left Rotation and Recolor\n");
                w->color = xParent->color;
                xParent->color = BLACK;
                if (w->right != NULL) w->right->color = BLACK;
                root = leftRotate(root, xParent);
                x = root;
                break;
            }
        }
        else
        {
            // symmetric
            Tree *w = xParent->left;
            if (w && w->color == RED)
            {
                printf("Delete Case 1: Right Rotation and Recolor\n");
                w->color = BLACK;
                xParent->color = RED;
                root = rightRotate(root, xParent);
                w = xParent->left;
            }
            if ((w->left == NULL || w->left->color == BLACK) &&
                (w->right == NULL || w->right->color == BLACK))
                {
                printf("Delete Case 2: Recoloring\n");
                w->color = RED;
                x = xParent;
                xParent = x->parent;
            }
            else
            {
                if (w->left == NULL || w->left->color == BLACK)
                {
                    printf("Delete Case 3: Left Rotation and Recolor\n");
                    if (w->right != NULL) w->right->color = BLACK;
                    w->color = RED;
                    root = leftRotate(root, w);
                    w = xParent->left;
                }
                printf("Delete Case 4: Right Rotation and Recolor\n");
                w->color = xParent->color;
                xParent->color = BLACK;
                if (w->left != NULL) w->left->color = BLACK;
                root = rightRotate(root, xParent);
                x = root;
                break;
            }
        }
    }

    if (x != NULL)
        x->color = BLACK;
    return root;
}


int main()
{
    Tree *root = NULL;
    int rbInsertNum;

    //int demorbInsert[] = {41, 38, 31, 12, 19, 8};
    //int demoDelete[] = {8, 12, 19};

    printf("i: Insert number\n");
    printf("d: Delete number\n");
    printf("q: Quit\n\n");

    char command;
    int value;

    while (1)
    {
        printf("Enter command: ");
        int result = scanf(" %c", &command);

        if (command == 'q')
        {
            break;
        }
        else if (command == 'i')
        {
            if (scanf("%d", &value) == 1)
            {
                root = rbInsert(value, root);
                if (root) root->color = BLACK;
                printf("Inserted %d\n", value);
                print_ascii_tree(root);
            }
        }
        else if (command == 'd')
        {
            if (scanf("%d", &value) == 1)
            {
                root = rbDelete(root, value);
                if (root) root->color = BLACK;
                printf("Deleted %d\n", value);
                print_ascii_tree(root);
            }
        }

        printf("\n");
    }

    return 0;
}
