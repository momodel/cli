import requests
import os
import progressbar

URL = "https://momodel.cn/pyapi"

def login(username, password):
    response = requests.post(
        URL + '/user/login', json={"username": username, "password": password})
    if (response.status_code == 200):
        # successful login
        print("登陆成功！")
        return response.json()['token']
    if 'message' in response.json():
        print (response.json()['message'])
        return


def view_project_list(token):
    response = requests.get(URL + '/project?page_no=1&page_size=5&type=app&group=my', headers={"Authorization": token},
                            json={"page_no": "1", "page_size": "5", "type": "app", "group": "my"})
    json = response.json()
    if (response.status_code == 200):
        # successful
        if (json and 'projects' in json and json['projects']):
          projects = json['projects']
          for project in projects:
            print("id: %s, name: %s, type: %s" %
                  (project['_id'], project['name'], project['type']))
        else:
          print("No project at the moment")
        # return response.json()
    else:
      print (json['message'])

def create_project(token):
    response = requests.post(URL + '/project/default', headers={"Authorization": token},
                             json={"type": "app"})
    json = response.json()
    if (response.status_code == 200):
        print('Project created successfully')
    else:
        print(json['message'])

def delete_project(token, project_id):
    response = requests.delete(
        URL + '/project/projects/' + project_id, headers={"Authorization": token})
    json = response.json()
    if (response.status_code == 200):
        print('项目删除成功')
    else:
      print(json['message'])

def view_project_file(token, project_id, version):
    response = requests.get(URL + '/file/file_trees/%s?version=%s' %
                            (project_id, version), headers={"Authorization": token})
    json = response.json()
    if (response.status_code == 200) :
      if (json['children']):
        for child in json['children']:
          print (child['key'])
      else:
        print ('Empty')
    else:
      print(json['message'])

def view_job(token, project_type, project_id):
    response = requests.get(URL + '/jobs/project/%s/%s' %
                            (project_type, project_id), headers={"Authorization": token})
    json = response.json()
    if (response.status_code == 200):
      objects = json['response']['objects']
      if (objects):
        for object in objects:
          print('Job Name: %s\nJob ID: %s\nEnv: %s\nScript Path: %s\nDuration: %s\nStart Time: %s\nStatus: %s'
                          % (object['display_name'], object['_id'], object['env'], object['script_path'], object['duration'], object['start_time'], object['status']))
          print('------------')
      else:
        print ('该项目下当前无Job')
    else:
      print (json['message'])

def view_job_log(token, job_id):
    response = requests.get(URL + '/jobs/logs/%s' %
                            job_id, headers={"Authorization": token})
    json = response.json()
    if (response.status_code == 200):
      print (json['logs'])
    else:
      print (json['message'])

def create_job(token, parameters):
    response = requests.post(
        URL + '/jobs', json=parameters, headers={"Authorization": token}, )
    json = response.json()
    if (response.status_code == 200):
      print ('Job创建成功，Job ID为%s, Job名称为%s' % (json['response']['_id'], json['response']['display_name']))
    else:
      print (json['message'])

def terminate_job(token, job_id):
    response = requests.put(URL + '/jobs/%s/terminate' %
                            job_id, headers={"Authorization": token})
    json = response.json()
    if (response.status_code == 200):
      print ('Job终止成功！')
    else:
      print (json['message'])

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
        if (r.status_code != 200):
          print ('Upload failed!')
          return
        bar.update(chunk_index)
    bar.finish()
    print ('Upload finished!')
