import zmq
from zmq.decorators import context, socket


@context()
@socket(zmq.PULL)  # collects tasks results
@socket(zmq.PUSH)  # delivers results back to manager
def collector_daemon(ctx, pull, push):
    pull.bind("tcp://*:5558")
    push.bind("tcp://*:5559")
    while True:
        result = pull.recv_pyobj()
        print("collector")
        push.send_pyobj(result)


if __name__ == "__main__":
    collector_daemon()
