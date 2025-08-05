import pandas as pd
import json
import os

class DataManager:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.projects_file = os.path.join(self.data_dir, "projects.json")
        self.tasks_file = os.path.join(self.data_dir, "tasks.json")
        self.clients_file = os.path.join(self.data_dir, "clients.json")
        self.teams_file = os.path.join(self.data_dir, "teams.json")

        self._initialize_files()

    def _initialize_files(self):
        for f in [self.projects_file, self.tasks_file, self.clients_file, self.teams_file]:
            if not os.path.exists(f):
                with open(f, "w") as file:
                    json.dump([], file)

    def _load_data(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
        return pd.DataFrame(data) if data else pd.DataFrame()

    def _save_data(self, df, file_path):
        df.to_json(file_path, orient="records", indent=4)

    def load_projects(self):
        return self._load_data(self.projects_file)

    def save_projects(self, df):
        self._save_data(df, self.projects_file)

    def add_project(self, project_data):
        projects_df = self.load_projects()
        new_project_df = pd.DataFrame([project_data])
        updated_df = pd.concat([projects_df, new_project_df], ignore_index=True)
        self.save_projects(updated_df)

    def update_project_status(self, project_name, new_status):
        projects_df = self.load_projects()
        projects_df.loc[projects_df["Project Name"] == project_name, "Status"] = new_status
        self.save_projects(projects_df)

    def load_tasks(self):
        return self._load_data(self.tasks_file)

    def save_tasks(self, df):
        self._save_data(df, self.tasks_file)

    def add_task(self, task_data):
        tasks_df = self.load_tasks()
        new_task_df = pd.DataFrame([task_data])
        updated_df = pd.concat([tasks_df, new_task_df], ignore_index=True)
        self.save_tasks(updated_df)

    def load_clients(self):
        return self._load_data(self.clients_file)

    def save_clients(self, df):
        self._save_data(df, self.clients_file)

    def add_client(self, client_data):
        clients_df = self.load_clients()
        new_client_df = pd.DataFrame([client_data])
        updated_df = pd.concat([clients_df, new_client_df], ignore_index=True)
        self.save_clients(updated_df)

    def load_teams(self):
        return self._load_data(self.teams_file)

    def save_teams(self, df):
        self._save_data(df, self.teams_file)

    def add_team_member(self, team_member_data):
        teams_df = self.load_teams()
        new_team_member_df = pd.DataFrame([team_member_data])
        updated_df = pd.concat([teams_df, new_team_member_df], ignore_index=True)
        self.save_teams(updated_df)


