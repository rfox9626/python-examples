def flatten(lst):
    res = []
    for i in lst:
        if isinstance(i, list):
            res = res + flatten(i)
        else:
            res.append(i)

    return res



def test_flatten():
  # Test 1: Standard mixed nesting
  assert flatten([1, [2, [3, 4], 5], 6]) == [1, 2, 3, 4, 5, 6]

  # Test 2: Already flat list (should remain unchanged)
  assert flatten([1, 2, 3, 4]) == [1, 2, 3, 4]

  # Test 3: Deeply nested single elements
  assert flatten([[[[[1]]]]]) == [1]

  # Test 4: Empty list and lists with empty sublists
  assert flatten([]) == []
  assert flatten([[], [[]], [1, []]]) == [1]

  # Test 5: Mixed data types (strings, numbers, booleans)
  assert flatten(["a", [1, True], ["b", [2]]]) == ["a", 1, True, "b", 2]


if __name__ == "__main__":
  test_flatten()
