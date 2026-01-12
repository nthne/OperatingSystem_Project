import threading
import time
import random

# Config
BUFFER_SIZE = 5
buffer = [] 

# Condition variable (Have a lock inside)
condition = threading.Condition()

# Producer
def producer(name):
    while True:
        # Critical section 
        with condition:
            # 1. Check if Buffer is full, if full then go to sleep
            while len(buffer) == BUFFER_SIZE:
                print(f"[{name}] Buffer FULL. Going to sleep (wait)...")
                condition.wait() # Giải phóng lock và đi ngủ
            
            # 2. Manipulate data (when woke up and there is space)
            item = random.randint(1, 100)
            buffer.append(item)
            print(f"[{name}] Produced {item}. Buffer: {buffer}")

            # 3. Notify sleeping threads (usually Consumer)
            # Equivalent to notifyAll() in the paper
            condition.notify_all()
        
        # Exit critical section, simulate production time
        time.sleep(random.uniform(0.1, 0.5))

# Consumer
def consumer(name):
    while True:
        # Critical section 
        with condition:
            # 1. Check if Buffer is empty, if empty then go to sleep
            while len(buffer) == 0:
                print(f"[{name}] Buffer EMPTY. Going to sleep (wait)...")
                condition.wait() # Giải phóng lock và đi ngủ
            
            # 2. Manipulate data (when woke up and there is space)
            item = buffer.pop(0)
            print(f"[{name}] \tConsumed {item}. Buffer: {buffer}")
            
            # 3. Notify sleeping threads (usually Producer)
            condition.notify_all()
            
        # Get out of critical section, simulate processing time
        time.sleep(random.uniform(0.2, 0.8))

if __name__ == "__main__":
    print("STARTING METHOD 2: CONDITION VARIABLES (MONITOR)")
    
    # Build threads 
    p1 = threading.Thread(target=producer, args=("Producer",))
    c1 = threading.Thread(target=consumer, args=("Consumer-1",))
    c2 = threading.Thread(target=consumer, args=("Consumer-2",))
    
    # Run threads
    p1.start()
    c1.start()
    c2.start()