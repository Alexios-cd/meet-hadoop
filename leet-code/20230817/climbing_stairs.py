from unittest import TestCase


# https://leetcode.cn/problems/climbing-stairs/
# 70. 爬楼梯
# 这是一个经典的动态规划问题。
#
# 设爬到第 n 阶楼梯的方法数为 f(n)，那么爬到第 n 阶楼梯的方式只有两种：从第 n-1 阶楼梯爬一步，或者从第 n-2 阶楼梯爬两步。
#
# 因此，f(n) = f(n-1) + f(n-2)。
#
# 根据初始条件，可以得到 f(1) = 1，f(2) = 2。
#
# 根据上述递推关系，可以使用动态规划的方法计算出 f(n)。


class Solution:
    def climbStairs(self, n: int) -> int:

        if n == 1:
            return 1
        if n == 2:
            return 2
        dp = [0] * (n + 1)
        dp[1] = 1
        dp[2] = 2
        for i in range(3, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]


class Test(TestCase):
    def test_01(self):
        stairs = Solution().climbStairs(10)
        self.assertEquals(3, stairs)
