import zmq
import time
from sim_shared import GameState, create_dummy_linked_game_states


def main():
    context = zmq.Context()
    #  Socket to talk to server
    print("Connecting to sim_games parallel games server...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    gs: GameState = create_dummy_linked_game_states(10)
    print("Sending gs to sim_games parallel server...")

    # Start our clock now
    tstart = time.time()

    socket.send_pyobj(gs)

    print("Waiting for results...")
    results = socket.recv_pyobj()

    tend = time.time()
    print("Total elapsed time: %d msec" % ((tend - tstart) * 1000))

    print("Got results!")
    print(results)


if __name__ == '__main__':
    main()
