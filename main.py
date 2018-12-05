from Webserver.WebServer import WebServer
import socket


def main():
    web_server = WebServer(socket.gethostname().split('.')[0])
    web_server.start()


if __name__ == '__main__':
    main()
