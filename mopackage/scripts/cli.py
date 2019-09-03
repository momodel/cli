import click
import json
import mopackage.httprequests as httprequests
from setuptools import setup

from pathlib import Path
home = str(Path.home())

token_file_path = home + '/.mo_cli_token.txt'


def get_stored_token():
    with open(token_file_path, 'r', encoding='utf-8') as token_file:
        token = token_file.read()
        if (not token):
            return ""
        else:
          # Bearer token
            return "Bearer " + token


@click.group()
def account():
    pass

@account.command()
def auth():
    try:
        username = click.prompt('Username', type=str)
        # Hide password
        password = click.prompt('Password', type=str, hide_input=True)
        token = httprequests.login(username, password)
        with open(token_file_path, 'w') as token_file:
          # Store token, if credentials run, it essentially clears previous content
            if (token):
                token_file.write(token)
    except Exception as e:
        print (e)
        print("Unexpected Error")


@click.group()
def project_management():
    pass


@project_management.command()
def list_project():
    try:
        token = get_stored_token()
        if (not token):
          # No existing token
            print("Please log in first.")
        else:
            httprequests.view_project_list(token)
    except Exception as e:
      print (e)
      print("Unexpected Error")


@project_management.command()
def create_project():
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.create_project(token)
  except:
    print('Unexpected Error')


@project_management.command()
@click.argument('project_id')
def delete_project(project_id):
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.delete_project(token, project_id)
  except:
    print ('Unexpected Error')

@click.group()
def file_management():
    pass


@file_management.command()
@click.argument('project_id')
@click.argument('version', required=False, default='workspace')
def view_project_file(project_id, version):
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.view_project_file(token, project_id, version)
  except:
    print ('Unexpected Error')

@file_management.command()
@click.argument('project_id')
@click.argument('file_path')
def upload_file(project_id, file_path):
  try:
    httprequests.upload_file(get_stored_token(), project_id, file_path)
  except:
    print ('Unexpected Error')


@click.group()
def job_management():
    pass


@job_management.command()
def view_job():
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        project_type = click.prompt("Project type: [app/module/toolkit/model]")
        project_id = click.prompt("Project ID")
        httprequests.view_job(token, project_type, project_id)
  except:
    print('Unexpected Error')

@job_management.command()
@click.argument('job_id')
def view_job_log(job_id):
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.view_job_log(token, job_id)
  except:
    print('Unexpected Error')

@job_management.command()
def create_job():
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        project_id = click.prompt("Project Id")
        project_type = click.prompt("Project type: [app/module/toolkit/model]")
        script_path = click.prompt("Script path")
        env = click.prompt("Environment: [cpu/gpu/gpu_matpool]")
        display_name = click.prompt("Display name")
        # Optional vararg args
        arg = click.prompt("Extra argument[Optional]", show_default=False, default="")
        args = ""
        while (arg):
          # Allow input while arg is non-empty
          args += arg
          args += " "
          arg = click.prompt("Extra argument[Optional]", show_default=False, default="")
        # Optional vararg jobfiles
        job_files = list()
        job_file = click.prompt("Job file[Optional]", show_default=False, default="")
        while (job_file):
          # Allow input while job_file is non-empty
          job_files.append(job_file)
          job_file = click.prompt("Job file[Optional]", show_default=False, default="")
        # Fill parameters
        parameters = {'project_id': project_id, 'type': project_type, 'script_path': script_path,
                      'env': env, 'display_name': display_name, 'args': args, 'job_files': job_files}
        httprequests.create_job(token, parameters)
  except:
    print('Unexpected Error')

@job_management.command()
@click.argument('job_id')
def terminate_job(job_id):
  try:
    token = get_stored_token()
    if (not token):
        print("Please log in first.")
    else:
        httprequests.terminate_job(token, job_id)
  except:
    print('Unexpected Error')

cli = click.CommandCollection(
    sources=[account, project_management, file_management, job_management])


def start():
    cli()

if __name__ == "__main__":
    cli()
