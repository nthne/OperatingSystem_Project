import threading
import time
import random

# Config
BUFFER_SIZE = 5
buffer = [] 

# Producer
def producer(name):
    while True:
        # Busy waiting
        while len(buffer) >= BUFFER_SIZE:
            pass 
        
        # Critical section 
        item = random.randint(1, 100)
        buffer.append(item)
        print(f"[{name}] Produced {item}. Buffer: {buffer}")

        # Simulate production time
        time.sleep(random.uniform(0.1, 0.5))

# Consumer
def consumer(name):
    while True:
        # Busy waiting
        while len(buffer) == 0:
            pass
        
        # Critical section
        try:
            item = buffer.pop(0)
            print(f"[{name}] \tConsumed {item}. Buffer: {buffer}")
        except IndexError:
            # Race condition error: 
            print(f"[{name}] \tError: Buffer empty (Race Condition)!")
        
        # Simulate production time
        time.sleep(random.uniform(0.2, 0.8))

# Main
if __name__ == "__main__":
    print("STARTING METHOD 1: BUSY WAITING")
    print("WARNING: Press Ctrl+C to stop immediately (High CPU Usage)")
    
    # Build threads
    p1 = threading.Thread(target=producer, args=("Producer",))
    c1 = threading.Thread(target=consumer, args=("Consumer",))
    
    # Run threads
    p1.start()
    c1.start()