from TreeNode import TreeNode

class RBTreeNode(TreeNode):
    def __init__(self, p=None, isRed=True, val=0, left=None, right=None):
        self.p = p
        self.isRed = isRed
        TreeNode.__init__(self, val, left, right)
    
    def __repr__(self):
        color = 'RED' if self.isRed else 'BLACK'
        parent = self.p.val if self.p is not None else None
        return super().__repr__() + '\nColor:\t{}\nParent:\t{}'.format(color, parent)

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val
