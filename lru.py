from threading import Lock

class BasicLRU:
    def __init__(self, len):
        self.limit = len
        self.data = {}
        self.lock = Lock()

    def get(self, key):
        with self.lock:
            if key not in self.data:
                return None

            val = self.data.pop(key)
            self.data[key] = val
            return val

    def put(self, key, entry):
        with self.lock:
            if key in self.data:
                self.data.pop(key)
            elif len(self.data) >= self.limit:
                # get oldest from list
                rm_key = next(iter(self.data))
                self.data.pop(rm_key)

            self.data[key] = entry

if __name__ == "__main__":
    # Create a cache with a max capacity of 2 items
    my_cache = BasicLRU(2)
    
    my_cache.put("user_101", "Alice")
    my_cache.put("user_102", "Bob")
    
    # Access user_101, making it the most recently used
    print("Get user_101:", my_cache.get("user_101")) 
    
    # Adding a 3rd item should evict user_102 because user_101 was just accessed
    my_cache.put("user_103", "Charlie")
    
    print("Get user_102 (should be evicted):", my_cache.get("user_102")) # Returns None
    print("Get user_103:", my_cache.get("user_103")) # Returns Charlie
