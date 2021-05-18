from RBTreeNode import RBTreeNode

class RBTree():
    TNIL = RBTreeNode(isRed=False, val=-1)

    def __init__(self):
        self.root = RBTree.TNIL
    
    def __contains__(self, item):
        return self._search(item) != RBTree.TNIL

    def insert(self, val):
        z = RBTreeNode(p=None, 
                       isRed=True, 
                       val=val, 
                       left=RBTree.TNIL, 
                       right=RBTree.TNIL)
        x, y = self.root, RBTree.TNIL
        while x != RBTree.TNIL:           # start search at root and traverse down until a proper spot is found
            y = x
            x = x.left if z < x else x.right
        z.p = y
        if y is RBTree.TNIL:              # the tree is empty, we set root to be z
            self.root = z
        elif z < y:                       # otherwise set z to be y's left or right child
            y.left = z
        else:
            y.right = z
        self._insert_fix_up(z)            # fix any violations (2, 4, or 5) 

    def delete(self, val):
        y = z = self._search(val)               # 
        y_original_isRed = y.isRed              # save color to test at the end of procedure
        if z.left is RBTree.TNIL:
            x = z.right                         # set x to point to y's singular child to the LEFT
            self._transplant(z, z.right)
        elif z.right == RBTree.TNIL:
            x = z.left                          # or the RIGHT 
            self._transplant(z, z.left)
        else:                                   # in the case that z has two children, then z is not y
            y = self.minimum(z.right)           # set y to be z's successor 
            y_original_isRed = y.isRed
            x = y.right                         
            if y.p is z:
                x.p = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.p = y
            self._transplant(z, y)             
            y.left = z.left
            y.left.p = y
            y.isRed = z.isRed
        if not y_original_isRed:                # if y's color was BLACK, moving or removing y
            self._delete_fix_up(x)              # might violate property 5

    def successor(self, val):
        if (x := self._search(val)) is RBTree.TNIL:
            return
        elif x.right != RBTree.TNIL:
            return self.minimum(x.right)
        y = x.p
        while y != RBTree.TNIL and x is y.right:
            x = y
            y = y.p
        return y if y != RBTree.TNIL else None

    def predecessor(self, val):
        if (x := self._search(val)) is RBTree.TNIL:
            return
        elif x.left != RBTree.TNIL:
            return self.maximum(x.left)
        y = x.p
        while y != RBTree.TNIL and x is y.left:
            x = y
            y = y.p
        return y if y != RBTree.TNIL else None

    def _search(self, val):
        x = self.root
        while x != RBTree.TNIL:
            if x.val == val:
                return x
            if x.val < val:
                x = x.right
            else:
                x = x.left
        return RBTree.TNIL
    
    def minimum(self, root):
        while root.left != RBTree.TNIL:
            root = root.left
        return root

    def maximum(self, root):
        while root.right != RBTree.TNIL:
            root = root.right
        return root

    def _insert_fix_up(self, z):
        while z.p.isRed:                        # recall z is inserted as RED, while the parent is RED, property 4 is violated
            if z.p is z.p.p.left:               # if z's parent is a LEFT child
                y = z.p.p.right                 # set y to be z's uncle/aunt i.e. RIGHT child of z's grandparent
                if y.isRed:                     # if z's uncle is RED, we know that the grandparent is BLACK
                    z.p.isRed = False           # and we can color z's parent 
                    y.isRed = False             # and uncle/aunt to BLACK to maintain property 4 between z and its parent
                    z.p.p.isRed = True          # then color z's grandparent to RED to maintain property 4 between it and it's children (z's parent and uncle/aunt)
                    z = z.p.p                   # move pointer two levels up for the next iteration
                else:                           # other wise if the uncle/aunt is BLACK
                    if z is z.p.right:          # and z is a RIGHT child, (and we are still violating property 4)
                        z = z.p                 # move z's pointer to it's parent
                        self._left_rotate(z)    # and left rotate on z, this does not violate property 5
                    z.p.isRed = False           # set z's parent to BLACK
                    z.p.p.isRed = True          # set z's grandparent to RED
                    self._right_rotate(z.p.p)   # right rotate to turn the grandparent into z's sibling
            else:                               # swap LEFT:RIGHT if z's parent is a RIGHT child
                y = z.p.p.left         
                if y.isRed:
                    z.p.isRed = False   
                    y.isRed = False    
                    z.p.p.isRed = True  
                    z = z.p.p
                else:
                    if z is z.p.left:  
                        z = z.p
                        self._right_rotate(z)
                    z.p.isRed = False   
                    z.p.p.isRed = True  
                    self._left_rotate(z.p.p) 
        self.root.isRed = False         

    def _delete_fix_up(self, x):
        while x != RBTree.TNIL and not x.isRed:
            if x is x.p.left:
                w = x.p.right
                if w.isRed:
                    w.isRed = False
                    x.p.isRed = True
                    self._left_rotate(x.p)
                    w = x.p.right
                if not (w.left.isRed and  w.left.isRed):
                    w.isRed = True
                    x = x.p
                else:
                    if not w.right.isRed:
                        w.left.isRed = False
                        w.isRed = True
                        self._right_rotate(w)
                        w = x.p.right
                    w.isRed = x.p.isRed
                    x.p.isRed = False
                    w.right.isRed = False
                    self._left_rotate(x.p)
                    x = self.root
            else:
                w = x.p.left
                if w.isRed:
                    w.isRed = False
                    x.p.isRed = True
                    self._right_rotate(x.p)
                    w = x.p.left
                if not (w.right.isRed and  w.right.isRed):
                    w.isRed = True
                    x = x.p
                else:
                    if not w.left.isRed:
                        w.right.isRed = False
                        w.isRed = True
                        self._left_rotate(w)
                        w = x.p.left
                    w.isRed = x.p.isRed
                    x.p.isRed = False
                    w.left.isRed = False
                    self._right_rotate(x.p)
                    x = self.root
        x.isRed = False

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != RBTree.TNIL:
            y.right.p = x
        y.p = x.p
        if x.p is RBTree.TNIL:
            self.root = y
        elif x is x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y

    def _left_rotate(self, x):
        y = x.right                     # set y to be x's RIGHT
        x.right = y.left                # set y's LEFT subtree into x's RIGHT subtree 
        if y.left != RBTree.TNIL:
            y.left.p = x                # set y's LEFT subtree's parent to x
        y.p = x.p                       # x's parent adopts y
        if x.p is RBTree.TNIL:          
            self.root = y               
        elif x is x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y

    def _transplant(self, u, v):
        if u.p is RBTree.TNIL:
            self.root = v
        elif u is u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p