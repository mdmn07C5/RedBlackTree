# from RBTreeNode import RBTreeNode
from RBTree import RBTree
import random

def inorder_traversal(root):
    if root == RBTree.TNIL:
        return 
    inorder_traversal(root.left)
    print('{}: {}'.format(root.val, 'R' if root.isRed else 'B'))
    inorder_traversal(root.right)

# slightly modified version of the algorithm by https://stackoverflow.com/users/4237254/bck
# which is a stand alone version of the algorithm by https://stackoverflow.com/users/1143396/j-v
# copypasta'd from https://stackoverflow.com/questions/34012886
def print_tree(root, val="val", left="left", right="right"):
    def display(root, val=val, left=left, right=right):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if root.right is RBTree.TNIL and root.left is RBTree.TNIL:
            line = '{}:{}'.format(root.val, 'R' if root.isRed else 'B')
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if root.right is RBTree.TNIL:
            lines, n, p, x = display(root.left)
            s = '{}:{}'.format(root.val, 'R' if root.isRed else 'B')
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if root.left is RBTree.TNIL:
            lines, n, p, x = display(root.right)
            s = '{}:{}'.format(root.val, 'R' if root.isRed else 'B')
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(root.left)
        right, m, q, y = display(root.right)
        s = '{}:{}'.format(root.val, 'R' if root.isRed else 'B')
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    lines, *_ = display(root, val, left, right)
    for line in lines:
        print(line)

if __name__== '__main__':
    rbtree = RBTree()
    nums = list(range(16, 32))
    random.shuffle(nums)
    for val in nums:
        rbtree.insert(val)
    print('Generated Tree:')
    print('Minimum: {}, Maximum:{}'.format(rbtree.minimum(rbtree.root).val, rbtree.maximum(rbtree.root).val))
    print_tree(rbtree.root)
    
    to_delete = []
    l = list(range(len(nums)))
    for i in range(3):
        index = random.choice(l)
        l.remove(index)
        to_delete.append(nums[index])

    for i in to_delete:
        s = rbtree.successor(i).val if rbtree.successor(i) is not None else None
        p = rbtree.predecessor(i).val if rbtree.predecessor(i) is not None else None
        print('\nSuccessor({}) = {}'.format(i, s))
        print('Predecessor({}) = {}'.format(i, p))
        rbtree.delete(i)
        print('Tree state after Delete({}):\n'.format(i))
        print_tree(rbtree.root)