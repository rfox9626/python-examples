def two_sum(nums, total):
    res = {}

    for i, j in enumerate(nums):
        needed = total - j

        if needed in res:
            return sorted([i, res[needed]])
        else:
            res[j] = i

    return None




def test_two_sum():
  # Test standard case where solution is in the middle/end
  assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]

  # Test case where numbers are not at the beginning
  assert sorted(two_sum([3, 2, 4], 6)) == [1, 2]

  # Test case with duplicate numbers
  assert sorted(two_sum([3, 3], 6)) == [0, 1]

  # Test case with negative numbers
  assert sorted(two_sum([-1, -2, -3, -4, -5], -8)) == [2, 4]


if __name__ == "__main__":
  test_two_sum()
