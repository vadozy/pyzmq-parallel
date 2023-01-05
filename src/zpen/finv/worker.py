import os

import zmq
from zmq.decorators import context, socket

from .shared import f1, C1


@context()
@socket(zmq.PULL)  # source of tasks
@socket(zmq.PUSH)  # collector of results
def work_daemon(ctx, pull, push):
    push.connect("tcp://localhost:5558")
    pull.connect("tcp://localhost:5557")
    while True:
        job = pull.recv_pyobj()
        print(f"worker [{os.getpid()}]")
        func = job["func"]
        params = job["params"]
        data = func(**params)
        result = {"data": data, "params": params}
        push.send_pyobj(result)


if __name__ == "__main__":
    work_daemon()
