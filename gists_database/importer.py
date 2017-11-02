import requests
import pprint
import sqlite3

BASE_URL = 'https://api.github.com/users/{}/gists'

def import_gists_to_database(db, username, commit=True):
    gists = requests.get(BASE_URL.format(username))
    gists.raise_for_status()
    gists = gists.json()
    conn = db
    query = """INSERT INTO gists (github_id, html_url, git_pull_url, 
                                git_push_url, commits_url, forks_url, public, 
                                created_at, updated_at, comments, comments_url) 
                                VALUES (:id, :html_url, :git_pull_url, 
                                :git_push_url, :commits_url, :forks_url, 
                                :public, :created_at, :updated_at, :comments, 
                                :comments_url);"""
    cursor = conn.cursor()
    for gist in gists:
        cursor.execute(query, gist)
    if commit == True:
        conn.commit()
    return gists