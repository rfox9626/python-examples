def find_common_keys(dict_list):
    if not dict_list:
        return set()

    q = set(dict_list[0].keys())

    for dict in dict_list[1:]:
        q = q.intersection(dict.keys()) 

    return(q)


def test_dictionary_intersection():
  # Test 1: Standard intersection where some keys are shared across all
  dicts_a = [{"a": 1, "b": 2, "c": 3}, {"b": 2, "c": 9, "d": 4}, {"b": 2, "e": 5}]
  # If you are doing common keys: expected would be {'b'}
  # If you are doing common items: expected would be {'b': 2} (or equivalent dict/items)
  assert find_common_keys(dicts_a) == {"b"}

  # Test 2: Multiple shared keys
  dicts_b = [{"x": 1, "y": 2, "z": 3}, {"x": 10, "y": 20, "z": 30}]
  assert find_common_keys(dicts_b) == {"x", "y", "z"}

  # Test 3: No common keys at all
  dicts_c = [{"a": 1}, {"b": 2}, {"c": 3}]
  assert find_common_keys(dicts_c) == set()

  # Test 4: Single dictionary in the list
  dicts_d = [{"a": 1, "b": 2}]
  assert find_common_keys(dicts_d) == {"a", "b"}

  # Test 5: Empty list
  assert find_common_keys([]) == set()


if __name__ == "__main__":
  test_dictionary_intersection()
