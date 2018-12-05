import socket
import threading
from Webserver.ResponseHandler import ResponseHandler
import Webserver.RequestModels as WebServerRequestModels
import re
import json
from urllib.parse import unquote


class WebServer:
    def __init__(self, host="127.0.0.1", port=8000):
        # intialise host, port , max connections
        self.host = host
        self.port = port
        self.CONNECTION_COUNT = 5
        self.PACKET_SIZE = 1024
        self.socket = None

    def start(self):
        # intialise and bind the socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
            print("Server started at -- {0}:{1}".format(self.host, self.port))
        except Exception as exception:
            print(exception)
            exit(1)

        self.__listen()

    def __listen(self):
        self.socket.listen(self.CONNECTION_COUNT)
        while True:
            socket_client, socket_address = self.socket.accept()
            socket_client.settimeout(10)
            print("Connection from {0}".format(socket_address))
            threading.Thread(target=self.__handle_client, args=(socket_client, socket_address)).start()

    @staticmethod
    def __process_request_path(request_path):
        # utility function to process request path
        request_path = unquote(request_path)
        parameters = re.findall('\<(.*?)\>', request_path)
        resource_id = request_path.split('/')[1]
        return WebServerRequestModels.RoutePathModel(resource_id, parameters)

    def __process_request_params(self, data):
        # utility function to process request path details
        data = unquote(data)
        try:
            data_without_request_body = data.split("\r\n\r\n")[0]
            request_body = json.loads(data.split("\r\n\r\n")[1])
        except:
            data_without_request_body = data
            request_body = None
        request_method = data.split(' ')[0]
        request_path = self.__process_request_path(data.split(' ')[1])
        request_additional_params = dict()
        request_additional_params_raw = data_without_request_body.split('\r\n')[1:]

        for parameters_raw in request_additional_params_raw:
            parameters_raw = parameters_raw.rstrip()
            parameter_list = parameters_raw.split(':')
            if len(parameter_list) == 2:
                request_additional_params[parameter_list[0]] = parameter_list[1]

        request_additional_params['body'] = request_body

        return request_method, request_path, request_additional_params

    def __handle_client(self, socket_client, socket_address):

        # receive and process the request from the socket client

        while True:
            print(socket_address)
            data = socket_client.recv(self.PACKET_SIZE).decode()

            if not data:
                break
            try:
                request_method, request_path, request_additional_params = self.__process_request_params(data)
                print(data)
                response_handler = ResponseHandler(request_method, request_path, request_additional_params['body'])

                """
                process response method can be extended to serve contents other than json
                """

                response = response_handler.process_response()

                socket_client.send(response)
            except Exception as E:
                print(E)

            socket_client.close()
            break
