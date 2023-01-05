import zmq


def main():
    # Client sends tasks to this port synchronously
    context = zmq.Context()
    collector_server = context.socket(zmq.REP)
    collector_server.bind("tcp://*:5559")

    # Socket to receive solutions on
    receiver = context.socket(zmq.PULL)
    receiver.bind("tcp://*:5558")

    while True:
        solutions = []
        # Received signal that the start of batch
        tasks_count = int(collector_server.recv_string())
        print("Collector received signal that {} tasks' solutions are coming soon...")

        # Collect tasks solutions
        for i in range(tasks_count):
            s = receiver.recv_pyobj()
            print("Received solution number {}".format(i + 1))
            solutions.append(s)

        print("Sending all solutions to sim_games server")
        collector_server.send_pyobj(solutions)


if __name__ == '__main__':
    main()
