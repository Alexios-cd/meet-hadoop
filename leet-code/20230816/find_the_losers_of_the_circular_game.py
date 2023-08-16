from typing import List
from unittest import TestCase

# https://leetcode.cn/problems/find-the-losers-of-the-circular-game/description/
class Solution:
    def circularGameLosers(self, n: int, k: int) -> List[int]:
        data_array = [0 for i in range(0, n)]
        count = 1
        index = 0
        while True:
            # 如果有个人，第二次接到球，游戏退出
            if data_array[index] == 1:
                break
            data_array[index] = 1
            index = (index+count*k)%n
            count += 1
        print(data_array)
        return [i+1 for i, num in enumerate(data_array) if num != 1]


class Test(TestCase):
    def test_01(self):
        n = 5
        k = 2
        losers = Solution().circularGameLosers(n, k)
        self.assertEquals(losers, [4, 5])
