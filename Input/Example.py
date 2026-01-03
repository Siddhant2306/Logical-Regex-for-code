def sum_positive(nums):
    total = 0
    sum_name = 2
    for x in nums:
        if x > 0:
            total = total + x + sum_name
    return total
