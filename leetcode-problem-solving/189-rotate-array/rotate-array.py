class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if k == 0:
            return nums
        if len(nums) == 0:
            return []
        if len(nums) < k:
            k = k % len(nums)
        k_last_ele = nums[-k:]       
        nums[k:] = nums[:-k]
        nums[:k] = k_last_ele
