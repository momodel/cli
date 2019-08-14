import requests
import os
import progressbar
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

URL = "http://momodel.cn/pyapi"

def login(username, password):
    response = requests.post(
        URL + '/user/login', json={"username": username, "password": password})
    if (response.status_code == 200):
        # successful login
        print("Authentication succeeded")
        return response.json()['token']
    if (response.status_code == 400):
        print("Incorrect username/password")
        return
    print("Unknown error occured.")


def view_project_list(token):
    response = requests.get(URL + '/project?page_no=1&page_size=5&type=app&group=my', headers={"Authorization": token},
                            json={"page_no": "1", "page_size": "5", "type": "app", "group": "my"})
    if (response.status_code == 200):
        # successful
        return response.json()


def create_project(token):
    response = requests.post(URL + '/project/default', headers={"Authorization": token},
                             json={"type": "app"})
    if (response.status_code == 200):
        print('Project created successfully')
    else:
        print(response.json())
        print('Project creation failed')


def delete_project(token, project_id):
    response = requests.delete(
        URL + '/project/projects/' + project_id, headers={"Authorization": token})
    if (response.status_code == 200):
        print('Project removed successfully.')


def view_project_file(token, project_id, version):
    response = requests.get(URL + '/file/file_trees/%s?version=%s' %
                            (project_id, version), headers={"Authorization": token})
    return response.json()

def view_job(token, project_type, project_id):
    response = requests.get(URL + '/jobs/project/%s/%s' %
                            (project_type, project_id), headers={"Authorization": token})
    return response.json()


def view_job_log(token, job_id):
    response = requests.get(URL + '/jobs/logs/%s' %
                            job_id, headers={"Authorization": token})
    return response.json()


def create_job(token, parameters):
    response = requests.post(
        URL + '/jobs', json=parameters, headers={"Authorization": token})
    return response.json()


def terminate_job(token, job_id):
    response = requests.put(URL + '/jobs/logs/%s/terminate' %
                            job_id, headers={"Authorization": token})
    return response.json()


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def upload_file(token, project_id, file_path):
    file = open(file_path, 'rb')
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    chunk_size = 65536
    uuid = file_path

    headers = {}
    values = {}
    chunks = []
    chunk_index = 0
    for chunk in read_in_chunks(file, chunk_size):
        chunks.append(chunk)

    num_chunk = len(chunks)
    chunk_index = 0
    bar = progressbar.ProgressBar(maxval=num_chunk, widgets=[progressbar.Bar('=', '[', ']'),  ' ', progressbar.Percentage()])
    bar.start()
    for chunk in chunks:
        headers['Authorization'] = token
        files = {'qqfile': chunk}
        values['qqfile'] = chunk
        values['qqfilename'] = filename
        values['qquuid'] = uuid
        values['qqtotalfilesize'] = filesize
        values['qqtotalparts'] = str(num_chunk)
        values['qqpartindex'] = str(chunk_index)
        chunk_index += 1
        r = requests.post(URL + "/file/%s" % project_id, files=files, data=values, headers=headers)
        bar.update(chunk_index)
    bar.finish()
