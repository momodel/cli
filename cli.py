import click
import json
import httprequests
from setuptools import setup

from pathlib import Path
home = str(Path.home())

token_file_path = home + '/.mo_cli_token.txt'

def get_stored_token():
    with open(token_file_path, 'r', encoding='utf-8') as token_file:
        token = "Bearer " + token_file.read()
        if (not token):
            return ""
        else:
            return token


@click.group()
def account():
    pass


@account.command()
def auth():
    username = click.prompt('Username', type=str)
    password = click.prompt('Password', type=str)
    token = httprequests.login(username, password)
    with open(token_file_path, 'w') as token_file:
        token_file.write(token)


@click.group()
def project_management():
    pass


@project_management.command()
def list_project():
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        json = httprequests.view_project_list(token)
        projects = json['projects']
        for project in projects:
            print("id: %s, name: %s" % (project['_id'], project['name']))


@project_management.command()
def create_project():
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.create_project(token)


@project_management.command()
@click.argument('project_id')
def delete_project(project_id):
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.delete_project(token, project_id)


@click.group()
def file_management():
    pass


@file_management.command()
@click.argument('project_id')
@click.argument('version', required=False)
def view_project_file(project_id, version):
    if (version == None):
        version = 'workspace'
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        file_json = httprequests.view_project_file(token, project_id, version)
        print(json.dumps(file_json, indent=4))


@file_management.command()
@click.argument('project_id')
@click.argument('file_path')
def upload_file(project_id, file_path):
    httprequests.upload_file(get_stored_token(), project_id, file_path)


@click.group()
def job_management():
    pass


@job_management.command()
@click.argument('project_type')
@click.argument('project_id')
def view_job(project_type, project_id):
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        response_json = httprequests.view_job(token, project_type, project_id)
        print(response_json)


@job_management.command()
@click.argument('job_id')
def view_job_log(job_id):
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        response_json = httprequests.view_job_log(token, job_id)
        print(response_json)


@job_management.command()
def create_job():
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        project_id = click.prompt("Project Id")
        project_type = click.prompt("Project type: app/module/toolkit/model")
        script_path = click.prompt("Script path")
        env = click.prompt("Environment")
        display_name = click.prompt("Display name")
        args = click.prompt("Extra arguments")
        parameters = json.dumps({'project_id': project_id, 'type': project_type, 'script_path': script_path,
                                'env': env, 'display_name': display_name, 'args': args})
        httprequests.create_job(token, parameters)

@job_management.command()
@click.argument('job_id')
def terminate_job(job_id):
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.terminate_job(token, job_id)


cli = click.CommandCollection(
    sources=[account, project_management, file_management, job_management])

def start():
    cli()

if __name__ == "__main__":
    cli()
