class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        left = self.left.val if self.left is not None else None
        right = self.right.val if self.right is not None else None
        return 'Value:\t{}\nLeft:\t{}\nRight:\t{}'.format(self.val, left, right)