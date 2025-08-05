import pandas as pd
import os

class DataManager:
    def __init__(self):
        self.projects_file = 'projects.csv'
        self.tasks_file = 'tasks.csv'
        self.clients_file = 'clients.csv'
        self.teams_file = 'teams.csv'
    
    def load_projects(self):
        return pd.read_csv(self.projects_file)
    
    def load_tasks(self):
        return pd.read_csv(self.tasks_file)
    
    def load_clients(self):
        return pd.read_csv(self.clients_file)
    
    def load_teams(self):
        return pd.read_csv(self.teams_file)
    
    def save_projects(self, df):
        df.to_csv(self.projects_file, index=False)
    
    def save_tasks(self, df):
        df.to_csv(self.tasks_file, index=False)
    
    def save_clients(self, df):
        df.to_csv(self.clients_file, index=False)
    
    def save_teams(self, df):
        df.to_csv(self.teams_file, index=False)
    
    def add_project(self, project_data):
        df = self.load_projects()
        new_row = pd.DataFrame([project_data])
        df = pd.concat([df, new_row], ignore_index=True)
        self.save_projects(df)
        return df
    
    def add_task(self, task_data):
        df = self.load_tasks()
        new_row = pd.DataFrame([task_data])
        df = pd.concat([df, new_row], ignore_index=True)
        self.save_tasks(df)
        return df
    
    def add_client(self, client_data):
        df = self.load_clients()
        new_row = pd.DataFrame([client_data])
        df = pd.concat([df, new_row], ignore_index=True)
        self.save_clients(df)
        return df
    
    def add_team_member(self, team_data):
        df = self.load_teams()
        new_row = pd.DataFrame([team_data])
        df = pd.concat([df, new_row], ignore_index=True)
        self.save_teams(df)
        return df
    
    def delete_project(self, index):
        df = self.load_projects()
        df = df.drop(index)
        df = df.reset_index(drop=True)
        self.save_projects(df)
        return df
    
    def delete_task(self, index):
        df = self.load_tasks()
        df = df.drop(index)
        df = df.reset_index(drop=True)
        self.save_tasks(df)
        return df
    
    def delete_client(self, index):
        df = self.load_clients()
        df = df.drop(index)
        df = df.reset_index(drop=True)
        self.save_clients(df)
        return df
    
    def delete_team_member(self, index):
        df = self.load_teams()
        df = df.drop(index)
        df = df.reset_index(drop=True)
        self.save_teams(df)
        return df

