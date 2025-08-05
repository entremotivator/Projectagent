import pandas as pd

def load_projects():
    return pd.read_csv('projects.csv')

def load_tasks():
    return pd.read_csv('tasks.csv')

def load_clients():
    return pd.read_csv('clients.csv')

def load_teams():
    return pd.read_csv('teams.csv')


