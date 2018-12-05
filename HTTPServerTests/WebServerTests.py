from unittest import TestCase
import requests


class TestWebServer(TestCase):

    def __intialise(self):
        self.host = "13.233.132.214" # use the web server deployed in production
        self.port = 8000
        self.resource_id = "job"
        self.job_name = "test"
        self.url = " http://{0}:{1}/{2}".format(self.host, self.port, self.resource_id)

    def test_start(self):
        self.__intialise()
        self.__test_put_data()
        self.__test_get_data()
        self.__test_post_data()
        self.__test_delete_data()

    def __test_put_data(self):
        headers = {"Content-Type": "application/json"}
        payload = {"Name": self.job_name}
        response = requests.put(self.url, headers=headers, json=payload)
        self.assertTrue(response.status_code == 200)
        response = response.json()
        self.assertTrue(response['Result'] is not None)
        self.job_id = int(response['Result'])

    def __test_get_data(self):
        url = self.url + "/<{0}>".format(self.job_id)
        response = requests.get(url)
        self.assertTrue(response.status_code == 200)
        response = response.json()
        self.assertTrue(response['Result'] == self.job_name)

        # test where job id does not exist

        url = self.url + "/<{0}>".format(1)
        response = requests.get(url)
        self.assertTrue(response.status_code == 404)

    def __test_post_data(self):
        new_job_name = "test_2"
        url = self.url + "/<{0}>/<{1}>".format(self.job_id, new_job_name)
        response = requests.post(url)
        self.assertTrue(response.status_code == 200)
        response = response.json()
        self.assertTrue(response['Result'])

        # test where job id does not exist

        url = self.url + "/<{0}>/<{1}>".format(1, new_job_name)
        response = requests.post(url)
        self.assertTrue(response.status_code == 404)

    def __test_delete_data(self):
        url = self.url + "/<{0}>".format(self.job_id)
        response = requests.delete(url)
        self.assertTrue(response.status_code == 200)
        response = response.json()
        self.assertTrue(response['Result'])

        # test where job id does not exist

        url = self.url + "/<{0}>".format(1)
        response = requests.delete(url)
        self.assertTrue(response.status_code == 404)
