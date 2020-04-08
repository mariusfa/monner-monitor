import requests
import json
import tkinter as tk
from tkinter import messagebox

def load_projects():
    projects = []
    with open('projects.txt') as f:
        projects = f.read().splitlines()
    return projects

def save_projects(projects):
    with open('projects.txt', 'w') as f:
        for project in projects:
            f.write(project + "\n")

def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def getSuggestionList():
    URL = 'https://www.monner.no/api/suggestions'
    page = requests.get(URL)
    json_result = json.loads(page.content)
    return json_result["suggestionList"]

def parseProjects(suggestion_list):
    retrieved_projects = []
    for item in suggestion_list:
        project = item["description"]["title"]
        retrieved_projects.append(project)
    return retrieved_projects

def alertNewProjects(new_projects):
    if (len(new_projects) > 0):
        string_msg = ''
        for project in new_projects:
            string_msg += project + '\n'
        showMessage(string_msg)

def showMessage(msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning('New projects', msg)

if __name__ == "__main__":
    loaded_projects = load_projects()
    suggestion_list = getSuggestionList()
    retrieved_projects = parseProjects(suggestion_list)
    save_projects(retrieved_projects)
    new_projects = diff(retrieved_projects, loaded_projects)
    alertNewProjects(new_projects)