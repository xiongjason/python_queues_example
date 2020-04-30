import threading
import queue
import time
import random

MAX_THREADS = 5
MAX_QUEUE_SIZE = 300
QUEUE = queue.Queue(MAX_QUEUE_SIZE)


class QueuePopper:
    def __init__(self, name, q):
        self.name = name
        self.q = q
        self.thread = threading.Thread(target=self.start_popping)

    def stop(self):
        print(f"Joining queue popper {self.name}")
        self.thread.join()

    def start(self):
        self.thread.start()

    def start_popping(self):
        popping = True

        while popping:
            item = self.q.get()

            if item is None:
                popping = False

            print(f"{self.name} found this item: {item}")
            time.sleep(random.randint(1, 3))  # Pretend to do work by sleeping

            self.q.task_done()

        print(f"{self.name} done processing the queue")


class QueuePusher:
    def __init__(self, q):
        self.q = q
        self.thread = threading.Thread(target=self.start_pushing)

    def stop(self):
        print(f"Joining queue pusher")
        self.thread.join()

    def start(self):
        self.thread.start()

    def start_pushing(self):
        print("Starting to push items into the queue")

        for i in range(500):
            while self.q.full():
                print("Queue is full, pop something off!")
                time.sleep(1)

            print(f"Pushing {i} into the queue")
            self.q.put(i)

        print("Done pushing items into the queue")


if __name__ == "__main__":
    qpopper_threads = {}
    for i in range(1, MAX_THREADS + 1):
        qpopper_threads[i] = QueuePopper(i, QUEUE)  # Worker threads
        qpopper_threads[i].start()  # Start the worker threads

    qpusher = QueuePusher(QUEUE)  # Inserts items into the queue
    qpusher.start()  # Start the thread that pushes the items into the queue
    qpusher.stop()  # Join the thread (all items are pushed into the queue)

    QUEUE.join()
    print("Queue has been joined all items in the queue have been pushed out")

    print("Notifying workers nothing left in the queue")
    # Notify worker threads the queue is done
    for i in range(MAX_THREADS):
        QUEUE.put(None)

    # Join the worker threads
    for key in qpopper_threads.keys():
        qpopper_threads[key].stop()
