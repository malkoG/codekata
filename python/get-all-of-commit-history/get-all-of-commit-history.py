import os
import json

import xlsxwriter
from github3 import login

github_auth_instance = login(os.environ['GITHUB_USERNAME'], password=os.environ['GITHUB_PASSWORD'])

user = github_auth_instance.me()
repo = github_auth_instance.repository(os.environ['GITHUB_ORG_NAME'], os.environ['GITHUB_REPO_NAME'])

row = 1
col = 0

workbook = xlsxwriter.Workbook('GitCommitHistory.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write(0, col,     "author")
worksheet.write(0, col + 1, "message")
worksheet.write(0, col + 2, "date")
for commit in repo.commits():
    commit_dict_object = json.loads(commit.as_json())['commit']
    worksheet.write(row, col,     commit_dict_object['author']['name'])
    worksheet.write(row, col + 1, commit_dict_object['message'])
    worksheet.write(row, col + 2, commit_dict_object['author']['date'])
    row += 1

workbook.close()
