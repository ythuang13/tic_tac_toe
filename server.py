from game import TicTacToe
from _thread import *
import pickle
import socket

HEADER_SIZE = 10
HOST = "0.0.0.0"
PORT = 5555
FORMAT = "utf-8"


def threaded_client(conn, cur_player):
    global game
    char = "X" if cur_player % 2 == 1 else "O"
    game.current_player = cur_player

    # initial confirmation
    conn.send(pickle.dumps(game))

    while True:

        try:
            header = conn.recv(HEADER_SIZE)
            d = conn.recv(int(header))
            data = pickle.loads(d)

            # handle different event
            if data[0] == data[1] == -1:
                # print("Receive: Default")
                pass
            elif data[0] == data[1] == -2:
                print("Receive: Clear board")
                game.clear_board()
            elif data[0] == data[1] == -3:
                print("Receive: Reset Game")
                game.full_reset()
            else:
                print(f"Receive: play move {data[0]}, {data[1]}")
                game.play_move(data[0], data[1], char)
                game.check_win()

            data = pickle.dumps(game)
            d = bytes(f"{len(data):<{HEADER_SIZE}}", FORMAT) + data
            conn.sendall(d)
        except ValueError:
            print("Disconnect with exit code: 0")
            break
        except ConnectionResetError:
            print("Disconnect with exit code: -1")
            break

    conn.close()
    print("Connection close")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
    except socket.error as e:
        print(e)

    s.listen(2)
    print(f"{HOST} listening on {PORT}...")

    # game initialization
    game = TicTacToe()
    current_player = 0

    while True:
        # handle incoming client
        connection, address = s.accept()
        print(f"Connection from {address} has been established.")
        current_player += 1
        start_new_thread(threaded_client, (connection, current_player))

sys.exit(0)
