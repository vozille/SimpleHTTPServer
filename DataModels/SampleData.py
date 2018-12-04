import time
from ErrorModels.ErrorModels import JobIdNotFoundError


class _JobModel:
    def __init__(self, job_name):
        self.job_id = int(time.time())
        self.job_name = job_name

    def get_job_id(self):
        return self.job_id


class _JobData:
    def __init__(self):
        self.job_list = []

    def add_job_data(self, job_name):
        new_job = _JobModel(job_name)
        self.job_list.append(new_job)
        return new_job.get_job_id()

    def get_job_data_by_id(self, job_id):
        job_id = int(job_id)
        for job in self.job_list:
            if job.job_id == int(job_id):
                return job.job_name
        raise JobIdNotFoundError

    def update_job_name(self, job_id, job_name):
        job_id = int(job_id)
        for job in self.job_list:
            if job.job_id == job_id:
                job.job_name = job_name
                return True
        raise JobIdNotFoundError

    def delete_job_data(self, job_id):
        job_id = int(job_id)
        index = -1
        for i in range(len(self.job_list)):
            if self.job_list[i].job_id == job_id:
                index = i
        if index >= 0:
            del self.job_list[index]
            return True
        raise JobIdNotFoundError


JobDetails = _JobData()
