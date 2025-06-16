import os
import sys

# Set required environment variables
os.environ['CCNET_CONF_DIR'] = '/opt/seatable/ccnet'
os.environ['SEAFILE_CONF_DIR'] = '/opt/seatable/seafile-data'

# Required to import seafserv
sys.path.insert(0, '/opt/seatable/seatable-server-latest/seafile/lib/python3/site-packages')

from seaserv import seafile_api

# TODO: Set these variables
server_url = 'https://seatable-demo.de'
base_uuid = '586a010d-7aec-42ba-a187-477c6facea6c'
# repo_id is a field in the "workspaces" table in the "dtable_db" database (every workspace is associated with a single Seafile library/repository)
repo_id = '031d8fd2-4011-43e5-b034-bf120215f002'
folder_name = f'/asset/{base_uuid}/custom/plugin-whiteboard/F7ls'
file_name = 'pageContent.json'

history_limit = seafile_api.get_repo_history_limit(repo_id)
print(f'History limit of repository {repo_id}: {history_limit}\n')

offset = 0
limit = 100

commits = seafile_api.get_commit_list(repo_id, offset, limit)

print(f'Number of commits in repository (limit = {limit}): {len(commits)}')

for c in commits:
    print(f'id = {c.id}, ctime = {c.ctime}')
    pass

entries = seafile_api.list_dir_by_path(repo_id, folder_name)
print(f'\nEntries in folder {folder_name}:')
for entry in entries:
    print(f' - {entry.obj_name}')

# Use the latest commit for now
commit_id = commits[0].id
path = os.path.join(folder_name, file_name)
limit = -1

revisions = seafile_api.get_file_revisions(repo_id, commit_id, path, limit)
print(f'\nRevisions of file {path}:')
for commit in revisions:
    if commit.rev_file_id is None:
        break

    access_token = seafile_api.get_fileserver_access_token(repo_id, commit.rev_file_id, op='download', username='seatable')
    download_link = server_url.rstrip('/') + f'/seafhttp/files/{access_token}/{file_name}'

    print(f' - Commit {commit.id}\n   size = {commit.rev_file_size}, ctime = {commit.ctime}\n   Download Link: {download_link}')
