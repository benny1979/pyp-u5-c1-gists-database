import requests
import pprint
import sqlite3

BASE_URL = 'https://api.github.com/users/{}/gists'

def import_gists_to_database(db, username, commit=True):
    gists = requests.get(BASE_URL.format(username))
    gists.raise_for_status()
    gists = gists.json()
    conn = db
    parameters = []
    for gist in gists:
        github_id = gist['id']
        html_url = gist['html_url']
        git_pull_url = gist['git_pull_url']
        git_push_url = gist['git_push_url']
        commits_url = gist['commits_url'] 
        forks_url = gist['forks_url'] 
        public = gist['public'] 
        created_at = gist['created_at']
        updated_at = gist['updated_at']
        comments = gist['comments']
        comments_url = gist['comments_url']
        gist_data = (github_id, html_url, git_pull_url, git_push_url, \
                    commits_url, forks_url, public, created_at, updated_at, \
                    comments,comments_url)
        parameters.append(gist_data)
    query = """INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, 
                                commits_url, forks_url, public, created_at, updated_at,
                                comments,comments_url) VALUES (?,?,?,?,?,?,?,?,?,?,?);"""
    cursor = conn.cursor()
    cursor.executemany(query, parameters)
    if commit == True:
        conn.commit()
    return gists