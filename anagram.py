def is_anagram(s1, s2):
    return sorted(s1.replace(" ", "").lower()) == sorted(s2.replace(" ", "").lower())



def test_anagram():
  # Standard anagrams
  assert is_anagram("listen", "silent") == True
  assert is_anagram("triangle", "integral") == True

  # Case-insensitivity and whitespace handling (if you want to be robust)
  assert is_anagram("Astronomer", "Moon starer") == True

  # Not anagrams (different letters or lengths)
  assert is_anagram("hello", "world") == False
  assert is_anagram("rat", "car") == False
  assert is_anagram("abc", "abcd") == False
