from __future__ import annotations
import sys
import time
import zmq
import enum


class Player(enum.Enum):
    black = 1
    white = 2

    @property
    def opposite(self) -> Player:
        return Player.black if self == Player.white else Player.white


context = zmq.Context()

# Socket to receive messages on
receiver = context.socket(zmq.PULL)
receiver.connect("tcp://localhost:5557")

# Socket to send messages to
sender = context.socket(zmq.PUSH)
sender.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    s = receiver.recv_pyobj()
    sys.stdout.write(str(s))

    # Simple progress indicator for the viewer
    sys.stdout.write('.')
    sys.stdout.flush()

    # Do the work
    time.sleep(100 * 0.001)

    # Send results to sink
    sender.send(b'')
