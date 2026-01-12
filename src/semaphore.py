import threading
import time
import random

# Config
BUFFER_SIZE = 5
buffer = [] # Sharing buffer between Producer and Consumer

# Create Semaphores
empty_slots = threading.Semaphore(BUFFER_SIZE) # Semaphore counts empty slots in Buffer.

full_slots = threading.Semaphore(0) # 2. Semaphore counts number of items in Buffer. (Initially 0)

buffer_mutex = threading.Lock() # Mutex (Lock) to protect Buffer when adding/removing elements

# Producer
def producer(name):
    while True:
        item = random.randint(1, 100)
        
        # Wait
        print(f"[{name}] Waiting for empty slot...")
        empty_slots.acquire()
        
        # Critical section
        with buffer_mutex:
            buffer.append(item)
            print(f"[{name}] \033[92mProduced {item}\033[0m. Buffer: {buffer}")
            # (\033[92m is green color in Terminal)
            
        # Signal
        full_slots.release()
        
        time.sleep(random.uniform(0.1, 0.5))

# Consumer
def consumer(name):
    while True:
        # Wait
        print(f"[{name}] Waiting for data...")
        full_slots.acquire()
        
        # Critical section
        with buffer_mutex:
            item = buffer.pop(0)
            print(f"[{name}] \033[94mConsumed {item}\033[0m. Buffer: {buffer}")
            # (\033[94m is blue color in Terminal)
            
        # Signal
        empty_slots.release()
        
        time.sleep(random.uniform(0.2, 0.8))

# Main
if __name__ == "__main__":
    print("STARTING METHOD 3: SEMAPHORES (OPTIMIZED)")
    
    p1 = threading.Thread(target=producer, args=("CPU-Producer",))
    c1 = threading.Thread(target=consumer, args=("GPU-Consumer",))
    
    p1.start()
    c1.start()