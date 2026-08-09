def first_non_repeating_char(str):
    dict = {}

    for i, v in enumerate(str):
        if v in dict:
            dict[v] = -1
        else:
            dict[v] = i

    # remove the -1 and sort it
    new_dict = {k: v for k,v in dict.items() if v != -1}
    
    if not new_dict:
        return -1

    # Clean_new preserves insertion order. the very first
    # element is guaranteed to be the first non-repeating 
    # character  We convert items() to an iterator and 
    # grab the first one.
    first_char, first_index = next(iter(new_dict.items()))

    return first_index



def test_first_non_repeating():
  # 'l' is the first non-repeating character (at index 0)
  assert first_non_repeating_char("leetcode") == 0

  # 'v' is the first non-repeating character (at index 2: l-o-v-e)
  assert first_non_repeating_char("loveleetcode") == 2

  # All characters repeat, should return -1 or None
  assert first_non_repeating_char("aabbcc") == -1

  # Single character string
  assert first_non_repeating_char("z") == 0

  # Non-repeating character is at the very end
  assert first_non_repeating_char("abacabad") == 3  # 'd' is at the end


if __name__ == "__main__":
  test_first_non_repeating()
