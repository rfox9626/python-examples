def is_palindrome(text: str) -> bool:
    # remove spaces and non alphanumeric
    stripped = [x.lower() for x in text if x.isalnum()]
    return stripped == stripped[::-1]


def test_palindrome_checker():
  # Assuming your function is called is_palindrome(text: str) -> bool
  assert is_palindrome("racecar") == True
  assert is_palindrome("Madam") == True
  assert is_palindrome("Was it a car or a cat I saw?") == True
  assert is_palindrome("hello") == False
  assert is_palindrome("") == True

if __name__ == "__main__":
    test_palindrome_checker()
