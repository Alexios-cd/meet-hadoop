# https://leetcode.cn/problems/merge-k-sorted-lists/
# Definition for singly-linked list.
from typing import List, Optional
from unittest import TestCase
# https://leetcode.cn/problems/merge-k-sorted-lists/description/
# 23. 合并 K 个升序链表

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def to_link(arr: List) -> ListNode:
    """
    将 数组转化为 ListNode
    :param arr: 需要转化的数组
    :return: 转化完成的 ListNode
    """
    if not arr:
        return None

    # 创建链表的头节点
    head = ListNode(arr[0])
    current = head

    # 遍历数组，将数组元素转化为链表节点
    for i in range(1, len(arr)):
        node = ListNode(arr[i])
        current.next = node
        current = node
    return head


def to_array(head: ListNode) -> List:
    """
    将 ListNode 转化为数组
    :param head: 需要转化的ListNode
    :return: 转化完成的数组
    """
    if not head:
        return []

    # 创建一个空数组
    arr = []
    current = head

    # 遍历链表，将节点的值添加到数组中
    while current:
        arr.append(current.val)
        current = current.next

    return arr


class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if lists is None or len(lists) == 0:
            return None
        lists = [lst for lst in lists if lst]

        result_list = []
        while len(lists) != 0:
            min_index = 0
            min_value = None
            for index, list_el in enumerate(lists):
                if min_value is None or min_value.val > list_el.val:
                    min_index = index
                    min_value = list_el

            if lists[min_index].next is None:
                lists.pop(min_index)
            else:
                lists[min_index] = lists[min_index].next
            result_list.append(min_value.val)
            # print(result_list)
        # 转化为ListNode
        if not result_list:
            return None
        head = ListNode(result_list[0])
        current = head

        # 遍历数组，将数组元素转化为链表节点
        for i in range(1, len(result_list)):
            node = ListNode(result_list[i])
            current.next = node
            current = node
        return head


class Test(TestCase):

    def test_01(self):
        source = [[1, 4, 5], [1, 3, 4], [2, 6]]
        lists = [to_link(el) for el in source]
        result = Solution().mergeKLists(lists)
        self.assertEquals([1, 1, 2, 3, 4, 4, 5, 6], to_array(result))
