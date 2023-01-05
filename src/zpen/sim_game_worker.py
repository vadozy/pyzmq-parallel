from __future__ import annotations
import time
import zmq
import random

from sim_shared import Player, GameState


def main():
    context = zmq.Context()
    # Socket to receive messages on
    receiver = context.socket(zmq.PULL)
    receiver.connect("tcp://localhost:5557")

    # Sockets to send solutions to
    collector = context.socket(zmq.PUSH)
    collector.connect("tcp://localhost:5558")

    # Process tasks forever
    while True:
        task = receiver.recv_pyobj()
        print("Received task")

        # Do the work
        time.sleep(0.1)  # seconds

        solution = Player(random.randint(1, 2))

        # Send results to collector
        collector.send_pyobj(solution)


if __name__ == '__main__':
    main()
