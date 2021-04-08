"""
Example 4­13. Server code
"""

import itertools
import time
import zmq

context = zmq.Context()
pusher = context.socket(zmq.PUSH)
pusher.bind("tcp://*:5557")
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

if __name__ == "__main__":
    for i in itertools.count():
        time.sleep(1)
        pusher.send_json(i)
        publisher.send_json(i)
