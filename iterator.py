class Iterator:
    def __init__(self, collection):
        self._data = collection
        self._limit = len(collection)
        self._index = 0

    def __iter__(self):
        return Iterator(self._data)

    def __next__(self):
        if self._index >= self._limit:
            raise StopIteration

        val = self._data[self._index]
        self._index += 1

        return val


def test_iterator():
    # Test 1: Basic iteration over a list
    items = ["apple", "banana", "cherry"]
    it = Iterator(items)
    
    collected = []
    for item in it:
        collected.append(item)
    
    assert collected == ["apple", "banana", "cherry"], f"Expected list items, got {collected}"

    # Test 2: Reusability (Multiple loops using the same iterator instance)
    first_pass = list(it)
    second_pass = list(it)
    assert first_pass == second_pass == ["apple", "banana", "cherry"], "Iterator failed to reset for subsequent loops"

    # Test 3: Empty collection handling
    empty_it = Iterator([])
    empty_collected = list(empty_it)
    assert empty_collected == [], "Empty collection should yield nothing"

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_iterator()
