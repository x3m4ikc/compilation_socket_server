import socket
import argparse


def send_files(host, port, files, makefile=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        num_files = len(files)
        header = 'Number: {}\n'.format(num_files)
        if makefile is not None:
            header += 'Makefile: {}\n'.format(makefile)
        s.sendall(header.encode())
        for file in files:
            with open(file, 'rb') as f:
                filename = 'File {}\n'.format(file)
                s.sendall(filename.encode() + f.read())


def upgrade_server(host, port, files, makefile=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        header = 'Upgrade\n'
        num_files = len(files)
        header += 'Number: {}\n'.format(num_files)
        if makefile is not None:
            header += 'Makefile: {}\n'.format(makefile)
        s.sendall(header.encode())
        for file in files:
            with open(file, 'rb') as f:
                filename = 'File {}\n'.format(file)
                s.sendall(filename.encode() + f.read())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', nargs='?', default='127.0.0.1')
    parser.add_argument('port', nargs='?', type=int, default=1234)
    parser.add_argument('files', nargs='+')
    parser.add_argument('-m', '--makefile')
    parser.add_argument('-u', '--upgrade', action='store_true')
    args = parser.parse_args()
    if args.upgrade:
        upgrade_server(args.host, args.port, args.files, args.makefile)
    else:
        send_files(args.host, args.port, args.files, args.makefile)


if __name__ == '__main__':
    main()
