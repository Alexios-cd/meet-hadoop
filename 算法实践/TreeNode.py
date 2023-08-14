from typing import Optional, List


# 二叉搜索树（Binary Search Tree，BST）是一种特殊的二叉树结构，具有以下特点：
# 有序性：对于BST中的每个节点，其左子树中的所有节点值都小于该节点的值，而右子树中的所有节点值都大于该节点的值。这个特性使得BST中的节点按照一定顺序排列。
# 唯一性：BST中不允许存在相同值的节点。如果插入一个已经存在的节点值，要么忽略该值，要么更新对应节点的值。
# 查找效率高：由于BST的有序性，可以利用二分查找的思想在BST中快速地查找一个特定的值。平均情况下，查找、插入和删除操作的时间复杂度为O(log n)，其中n是BST中节点的个数。
# 可以支持动态操作：BST的结构可以随时进行插入和删除操作，使得BST可以动态地维护一个有序集合。
# 需要注意的是，BST的性能取决于树的形状，如果BST退化成链表，其性能将退化为O(n)。因此，在实际使用中，需要保证BST的平衡性，以提高性能。常见的平衡二叉搜索树包括AVL树、红黑树等。
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def buildTree(arr: List[int]) -> TreeNode:
    """
    快速构建一个 TreeNode leet-code常用
    :param arr:  数组
    :return: 构建好的 TreeNode
    """
    if not arr:
        return None

    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while i < len(arr):
        node = queue.pop(0)
        if arr[i] is not None:
            node.left = TreeNode(arr[i])
            queue.append(node.left)
        i += 1
        if i < len(arr) and arr[i] is not None:
            node.right = TreeNode(arr[i])
            queue.append(node.right)
        i += 1

    return root


def treeToArray(root: TreeNode):
    """
    将一个TreeNode 快速 序列化成一个数组
    :param root:  TreeNode对象
    :return:  数组
    """
    if not root:
        return []

    arr = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node:
            arr.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            arr.append(None)

    # 删除末尾连续的None值
    while arr and arr[-1] is None:
        arr.pop()

    return arr
