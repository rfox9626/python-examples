import threading 
import asyncio
import concurrent.futures
import time
from collections import Counter

class LogQueue:
    def __init__(self, len):
        self._limit = len
        self._data = []
        self._lock = threading.Lock()
        self.stats = {}

    def add_to_queue(self, msg):
        with self._lock:
            if len(self._data) >= self._limit:
                self._data.pop(0)

            self._data.append(msg)

    def get_batch(self, batch_size: int = 10):
        with self._lock:
            if not self._data:
                return []

            # Grab from the front of the queue (FIFO order)
            batch = self._data[:batch_size]

            stats = [x.split(" ")[2].replace("[","").replace("]","") for x in batch]
            counts = Counter(stats)
            orig_dict = Counter(self.stats)
            combined = orig_dict + counts
            self.stats = dict(combined)
            
            del self._data[:batch_size]
            return batch

    def is_empty(self):
        with self._lock:
            return len(self._data) == 0

    def dump(self):
        for i in self._data:
            print(i)

def read_lines(name):
    with open(name, "r") as f:
        for line in f:
            yield line.strip()


async def read_log_file(name, queue, writers_done):
    print(f"Reading file {name}")
    iterator = read_lines(name)
    EOF = object()

    while True:
        line = await asyncio.to_thread(next, iterator, EOF)

        if line is EOF:
            break
            
        if line:
            queue.add_to_queue(line)
            await asyncio.sleep(0.0001)

    writers_done.set()
    print(f"[{threading.current_thread().name}] Finished streaming {name}.")


def log_consumer(queue, worker, writers_done):
    print(f"Consumer {worker} has started")

    while not writers_done.is_set() or not queue.is_empty():
        batch = queue.get_batch(batch_size=10)
        if batch:
            for item in batch:
                print(f"Worker {worker} got {item}")
        else:
            if writers_done.is_set():
                break 

            time.sleep(0.01)

def run_consumers(queue, max_workers, writers_done):
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = [ executor.submit(log_consumer, queue, i, writers_done) for i in range(1, max_workers + 1)]

        concurrent.futures.wait(futures) 


async def main():
    shared_buffer = LogQueue(100)
    max_workers = 4
    writers_done = threading.Event()

    file_list = ["server_" + str(x) + ".log" for x in range(1,6)]
    async_readers = [read_log_file(f, shared_buffer, writers_done) for f in file_list]

    thread_pool_task = asyncio.to_thread(run_consumers, shared_buffer, 4, writers_done)

    # gather everything so the thread pool and the 5 async files run concurrently
    await asyncio.gather(
        thread_pool_task,
        *async_readers
    )

    print("Summary")
    for k,v in shared_buffer.stats.items():
        print(f"   {k} = {v}")

if __name__ == "__main__":
    asyncio.run(main())
