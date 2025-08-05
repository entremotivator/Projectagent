# Streamlit Project Management System

A comprehensive web-based project management application built with Python and Streamlit.

## Features

- 📊 **Dashboard Overview** - Real-time metrics and visualizations
- 🏗️ **Project Management** - Create, view, edit, and delete projects
- ✅ **Task Management** - Manage tasks linked to projects
- 👥 **Client Management** - Maintain client information and contacts
- 🔧 **Team Management** - Manage team members and their roles
- 📥 **CSV Export** - Export all data to CSV format
- ⚙️ **JSON Service Upload** - Ready for Google Sheets integration

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install streamlit pandas
   ```

2. **Run the Application**
   ```bash
   streamlit run app_enhanced.py
   ```

3. **Access the Application**
   Open your browser and go to `http://localhost:8501`

## File Structure

```
streamlit-project-management/
├── app_enhanced.py          # Main Streamlit application
├── data_manager.py          # Data management utilities
├── projects.csv             # Sample projects data
├── tasks.csv               # Sample tasks data
├── clients.csv             # Sample clients data
├── teams.csv               # Sample teams data
├── deployment_guide.md     # Comprehensive deployment guide
├── system_architecture.md  # System architecture documentation
└── README.md              # This file
```

## Data Structure

### Projects
- Project Name, Description, Status, Due Date, Assigned To, Client Name

### Tasks
- Task Name, Project Name, Description, Status, Due Date, Assigned To

### Clients
- Client Name, Contact Person, Email, Phone, Company, Address

### Teams
- Team Member Name, Role, Email, Phone, Department, Status

## Documentation

- **[Deployment Guide](deployment_guide.md)** - Complete installation and deployment instructions
- **[System Architecture](system_architecture.md)** - Technical architecture overview

## Requirements

- Python 3.8+
- Streamlit
- Pandas

## License

This project is open source and available under the MIT License.

## Author

Created by Manus AI - August 2025

