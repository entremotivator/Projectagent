import pandas as pd
import requests
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDataManager:
    def __init__(self, sheet_id="1NOOKyz9iUzwcsV0EcNJdVNQgQVL9bu3qsn_9wg7e1lE"):
        self.sheet_id = sheet_id
        self.csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gsheet?tqx=out:csv&sheet=Tasks"
        self.gc = None
        self.sheet = None
        
    def setup_gspread_client(self, service_account_info):
        """Setup gspread client with service account credentials"""
        try:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = Credentials.from_service_account_info(
                service_account_info, 
                scopes=scopes
            )
            
            self.gc = gspread.authorize(credentials)
            self.sheet = self.gc.open_by_key(self.sheet_id)
            logger.info("Successfully connected to Google Sheets")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup gspread client: {str(e)}")
            return False
    
    def load_tasks_from_csv_url(self):
        """Load tasks from Google Sheets CSV export URL"""
        try:
            df = pd.read_csv(self.csv_url)
            df.columns = df.columns.str.strip()
            logger.info(f"Successfully loaded {len(df)} tasks from CSV URL")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load from CSV URL: {str(e)}")
            return self._get_sample_data()
    
    def load_tasks_from_gspread(self, worksheet_name="Tasks"):
        """Load tasks using gspread API"""
        try:
            if not self.gc or not self.sheet:
                logger.warning("gspread client not initialized")
                return self.load_tasks_from_csv_url()
            
            worksheet = self.sheet.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            df = pd.DataFrame(data)
            
            logger.info(f"Successfully loaded {len(df)} tasks from gspread")
            return df
            
        except Exception as e:
            logger.error(f"Failed to load from gspread: {str(e)}")
            return self.load_tasks_from_csv_url()
    
    def add_task(self, task_data, worksheet_name="Tasks"):
        """Add a new task to the Google Sheet"""
        try:
            if not self.gc or not self.sheet:
                logger.warning("gspread client not initialized, cannot add task")
                return False
            
            worksheet = self.sheet.worksheet(worksheet_name)
            
            # Prepare row data in the correct order
            row_data = [
                task_data.get('Task ID', ''),
                task_data.get('Executor', ''),
                task_data.get('Date', ''),
                task_data.get('Reminder Time', ''),
                task_data.get('Task Description', ''),
                task_data.get('Object', ''),
                task_data.get('Section', ''),
                task_data.get('Priority', ''),
                task_data.get('Executor ID', ''),
                task_data.get('Company', ''),
                task_data.get('Reminder Sent', ''),
                task_data.get('Reminder Sent Date', ''),
                task_data.get('Reminder Read', ''),
                task_data.get('Read Time', ''),
                task_data.get('Reminder Count', ''),
                task_data.get('Reminder Interval if No Report', ''),
                task_data.get('Status', ''),
                task_data.get('Comment', ''),
                task_data.get('Report Date', '')
            ]
            
            worksheet.append_row(row_data)
            logger.info(f"Successfully added task: {task_data.get('Task ID', 'Unknown')}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add task: {str(e)}")
            return False
    
    def update_task(self, task_id, updated_data, worksheet_name="Tasks"):
        """Update an existing task in the Google Sheet"""
        try:
            if not self.gc or not self.sheet:
                logger.warning("gspread client not initialized, cannot update task")
                return False
            
            worksheet = self.sheet.worksheet(worksheet_name)
            
            # Find the row with the matching Task ID
            task_id_col = worksheet.col_values(1)  # Assuming Task ID is in column A
            
            for i, cell_value in enumerate(task_id_col[1:], start=2):  # Skip header row
                if cell_value == task_id:
                    # Update the row
                    for col_name, new_value in updated_data.items():
                        col_index = self._get_column_index(worksheet, col_name)
                        if col_index:
                            worksheet.update_cell(i, col_index, new_value)
                    
                    logger.info(f"Successfully updated task: {task_id}")
                    return True
            
            logger.warning(f"Task ID {task_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Failed to update task: {str(e)}")
            return False
    
    def delete_task(self, task_id, worksheet_name="Tasks"):
        """Delete a task from the Google Sheet"""
        try:
            if not self.gc or not self.sheet:
                logger.warning("gspread client not initialized, cannot delete task")
                return False
            
            worksheet = self.sheet.worksheet(worksheet_name)
            
            # Find the row with the matching Task ID
            task_id_col = worksheet.col_values(1)
            
            for i, cell_value in enumerate(task_id_col[1:], start=2):
                if cell_value == task_id:
                    worksheet.delete_rows(i)
                    logger.info(f"Successfully deleted task: {task_id}")
                    return True
            
            logger.warning(f"Task ID {task_id} not found")
            return False
            
        except Exception as e:
            logger.error(f"Failed to delete task: {str(e)}")
            return False
    
    def get_task_analytics(self, df):
        """Generate analytics from task data"""
        try:
            analytics = {
                'total_tasks': len(df),
                'unique_executors': df['Executor'].nunique() if 'Executor' in df.columns else 0,
                'unique_companies': df['Company'].nunique() if 'Company' in df.columns else 0,
                'status_distribution': df['Status'].value_counts().to_dict() if 'Status' in df.columns else {},
                'priority_distribution': df['Priority'].value_counts().to_dict() if 'Priority' in df.columns else {},
                'executor_task_count': df['Executor'].value_counts().to_dict() if 'Executor' in df.columns else {},
                'company_task_count': df['Company'].value_counts().to_dict() if 'Company' in df.columns else {},
                'reminders_sent': len(df[df['Reminder Sent'].str.contains('Yes', case=False, na=False)]) if 'Reminder Sent' in df.columns else 0,
                'reminders_read': len(df[df['Reminder Read'].str.contains('Yes', case=False, na=False)]) if 'Reminder Read' in df.columns else 0,
                'high_priority_tasks': len(df[df['Priority'].str.contains('High', case=False, na=False)]) if 'Priority' in df.columns else 0,
                'completed_tasks': len(df[df['Status'].str.contains('Completed|Done', case=False, na=False)]) if 'Status' in df.columns else 0
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Failed to generate analytics: {str(e)}")
            return {}
    
    def get_reminder_insights(self, df):
        """Generate reminder-specific insights"""
        try:
            insights = {
                'total_reminders_sent': len(df[df['Reminder Sent'].str.contains('Yes', case=False, na=False)]) if 'Reminder Sent' in df.columns else 0,
                'total_reminders_read': len(df[df['Reminder Read'].str.contains('Yes', case=False, na=False)]) if 'Reminder Read' in df.columns else 0,
                'unread_reminders': len(df[
                    (df['Reminder Sent'].str.contains('Yes', case=False, na=False)) & 
                    (df['Reminder Read'].str.contains('No', case=False, na=False))
                ]) if all(col in df.columns for col in ['Reminder Sent', 'Reminder Read']) else 0,
                'pending_reminders': len(df[df['Reminder Sent'].str.contains('No', case=False, na=False)]) if 'Reminder Sent' in df.columns else 0,
                'avg_reminder_count': df['Reminder Count'].astype(str).str.extract('(\d+)').astype(float).mean().iloc[0] if 'Reminder Count' in df.columns else 0
            }
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate reminder insights: {str(e)}")
            return {}
    
    def _get_column_index(self, worksheet, column_name):
        """Get the column index for a given column name"""
        try:
            headers = worksheet.row_values(1)
            return headers.index(column_name) + 1
        except ValueError:
            return None
    
    def _get_sample_data(self):
        """Return sample data when live data is not available"""
        return pd.DataFrame({
            'Task ID': ['ID1', 'ID2', 'ID3', 'ID4', 'ID5'],
            'Executor': ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis'],
            'Date': ['2025-08-05', '2025-08-06', '2025-08-07', '2025-08-08', '2025-08-09'],
            'Reminder Time': ['09:00', '14:00', '10:30', '16:00', '11:15'],
            'Task Description': [
                'Complete project documentation',
                'Review client requirements', 
                'Update system architecture',
                'Conduct team meeting',
                'Finalize budget proposal'
            ],
            'Object': ['Documentation', 'Requirements', 'Architecture', 'Meeting', 'Budget'],
            'Section': ['Section A', 'Section B', 'Section C', 'Section A', 'Section B'],
            'Priority': ['High', 'Medium', 'Low', 'High', 'Medium'],
            'Executor ID': ['1001', '1002', '1003', '1004', '1005'],
            'Company': ['Company A', 'Company B', 'Company C', 'Company A', 'Company B'],
            'Reminder Sent': ['Yes', 'No', 'Yes', 'Yes', 'No'],
            'Reminder Sent Date': ['2025-08-05', '', '2025-08-07', '2025-08-08', ''],
            'Reminder Read': ['Yes', 'No', 'No', 'Yes', 'No'],
            'Read Time': ['09:15', '', '', '16:30', ''],
            'Reminder Count': ['1', '0', '2', '1', '0'],
            'Reminder Interval if No Report': ['24h', '12h', '6h', '24h', '12h'],
            'Status': ['In Progress', 'Pending', 'Completed', 'In Progress', 'Pending'],
            'Comment': ['On track', 'Waiting for approval', 'Done', 'Meeting scheduled', 'Budget review needed'],
            'Report Date': ['2025-08-05', '', '2025-08-07', '2025-08-08', '']
        })

# Utility functions for data validation
def validate_task_data(task_data):
    """Validate task data before adding/updating"""
    required_fields = ['Task ID', 'Executor', 'Task Description']
    
    for field in required_fields:
        if not task_data.get(field):
            return False, f"Missing required field: {field}"
    
    return True, "Valid"

def format_task_data(task_data):
    """Format task data for consistency"""
    formatted_data = task_data.copy()
    
    # Format date fields
    date_fields = ['Date', 'Reminder Sent Date', 'Report Date']
    for field in date_fields:
        if field in formatted_data and formatted_data[field]:
            try:
                # Ensure date is in YYYY-MM-DD format
                date_obj = pd.to_datetime(formatted_data[field])
                formatted_data[field] = date_obj.strftime('%Y-%m-%d')
            except:
                pass
    
    # Format time fields
    time_fields = ['Reminder Time', 'Read Time']
    for field in time_fields:
        if field in formatted_data and formatted_data[field]:
            try:
                # Ensure time is in HH:MM format
                time_obj = pd.to_datetime(formatted_data[field], format='%H:%M').time()
                formatted_data[field] = time_obj.strftime('%H:%M')
            except:
                pass
    
    return formatted_data

