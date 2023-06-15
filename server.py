import socket
import subprocess
import signal
import sys

HOST = '127.0.0.1'
PORT = 1234


def handle_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        data = data.decode()
        lines = data.split('\n')
        num_files = None
        makefile = None
        files = []
        for line in lines:
            if line.startswith('Number:'):
                num_files = int(line.split()[1])
            elif line.startswith('Makefile:'):
                makefile = line.split()[1]
            elif line.startswith('File'):
                files.append(line.split()[1])
        if num_files is None or len(files) != num_files:
            conn.sendall(b'Result: Fail\nInvalid number of files\n')
            continue
        if makefile is not None:
            make_result = subprocess.run(['make', '-f', makefile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if make_result.returncode != 0:
                conn.sendall(b'Result: Fail\n' + make_result.stderr)
                continue
        compile_result = subprocess.run(['gcc'] + files, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if compile_result.returncode == 0:
            conn.sendall(b'Result: OK\n')
        else:
            conn.sendall(b'Result: Fail\n' + compile_result.stderr)


def handle_signal(signum, frame):
    print('Received signal', signum)
    sys.exit(0)


# signal.signal(signal.SIGUSR1, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        handle_connection(conn)
