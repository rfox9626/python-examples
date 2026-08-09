def is_pangram(str):
    return len(set([x.lower() for x in str if x.isalpha()])) == 26


def test_pangram():
  # Classic English pangram containing all 26 letters
  assert is_pangram("The quick brown fox jumps over the lazy dog") == True 

  # Another classic pangram with mixed case and punctuation
  assert is_pangram("Pack my box with five dozen liquor jugs.") == True

  # Missing some letters (Not a pangram)
  assert is_pangram("Hello World") == False
  assert is_pangram("abcdefghijklmnopqrstuvwxy") == False  # Missing 'z'
  assert is_pangram("") == False  # Empty string


if __name__ == "__main__":
  test_pangram()
