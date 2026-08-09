def remove_duplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


def test_remove_duplicates():
  # Test standard list with duplicates in various positions
  assert remove_duplicates([1, 2, 2, 3, 4, 4, 5]) == [1, 2, 3, 4, 5]

  # Test list where order preservation matters
  assert remove_duplicates([4, 1, 9, 1, 4, 2]) == [4, 1, 9, 2]

  # Test list with no duplicates
  assert remove_duplicates([1, 2, 3]) == [1, 2, 3]

  # Test list with all identical elements
  assert remove_duplicates([7, 7, 7, 7]) == [7]

  # Test empty list
  assert remove_duplicates([]) == []


if __name__ == "__main__":
  test_remove_duplicates()
