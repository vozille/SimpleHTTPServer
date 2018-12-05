from DataModels.SampleData import JobDetails
import json
from ErrorModels.ErrorModels import JobIdNotFoundError, InvalidExceptionCodeError


class ResponseHandler:
    def __init__(self, request_method, route_path, request_body):
        self.request_method = request_method
        self.route_path = route_path
        self.request_body = request_body

    @staticmethod
    def __get_headers_by_response_code(response_code):
        try:
            header = 'HTTP/1.1 ' + str(response_code)
            if response_code == 200:
                header += " OK\r\n"
            elif response_code == 403:
                header += " Invalid Request\r\n"
            elif response_code == 404:
                header += " Not Found\r\n"
            elif response_code == 500:
                header += " Internal Sever Error\r\n"
            else:
                header += " Server Error\r\n"
            header += "Content-Type: application/json\n\n"
            return header
        except Exception:
            raise InvalidExceptionCodeError

    def __get_response(self, status_code, response_body):
        if response_body is not None:
            body = json.dumps({"Result": response_body, "Error": None})
        else:
            body = json.dumps({"Result": None, "Error": "Unknown Job Id"})
        return (self.__get_headers_by_response_code(status_code) + body).encode()
        pass

    def process_response(self, ):
        body = None
        try:
            if self.request_method == "GET":
                body = JobDetails.get_job_data_by_id(self.route_path.route_id, self.route_path.route_parameters[0])
            elif self.request_method == "PUT":
                body = JobDetails.add_job_data(self.route_path.route_id, self.request_body['Name'])
            elif self.request_method == "POST":
                body = JobDetails.update_job_name(self.route_path.route_id, self.route_path.route_parameters[0],
                                                  self.route_path.route_parameters[1])
            elif self.request_method == "DELETE":
                body = JobDetails.delete_job_data(self.route_path.route_id, self.route_path.route_parameters[0])
            else:
                pass
            return self.__get_response(200, body)
        except JobIdNotFoundError:
            return self.__get_response(404, None)
