# streamlit-todo-app

ProducTODO ✔️: A Streamlit To-Do List Application
ProducTODO is a modern, feature-rich to-do list application built with Python and Streamlit. It is designed to help users organize their tasks, boost productivity, and stay motivated with a clean, intuitive, and interactive user interface.

This project demonstrates proficiency in Python, UI development with Streamlit, and database management with SQLite.

➡️ View Live Demo (Replace the link above with your actual deployed Streamlit URL after deploying!)

Application Screenshot
(Note: It's highly recommended to take your own screenshot and replace the link above. You can upload your image to GitHub or an image hosting site like Imgur.)

✨ Features
This application goes beyond a simple to-do list and includes several productivity-enhancing features:

📝 Full CRUD Functionality:

Create: Add new tasks with a title, description, priority, and due date.

Read: View all tasks in a clean, organized layout.

Update: Mark tasks as complete, or edit their details (title, priority, etc.).

Delete: Remove tasks that are no longer needed.

📊 Productivity Dashboard:

Get an at-a-glance summary of your productivity.

View metrics for total, completed, and pending tasks.

A progress bar shows your overall completion rate.

🔍 Advanced Controls & Filtering:

Search: Instantly find any task using a keyword search.

Filter: Dynamically filter tasks by their status (Pending/Completed) or priority level (High/Medium/Low).

Sort: Tasks are automatically sorted by the nearest due date.

💾 Persistent Storage:

Tasks are saved to a local SQLite database (tasks.db), ensuring your data persists between sessions.

🚀 User Experience Enhancements:

Motivational Quotes: A new inspirational quote is displayed on each visit to keep you going.

Color-Coded Priorities: Visual icons (🔴🟡🟢) help quickly identify task priority.

Overdue Task Highlighting: Due dates are highlighted in red if they are past the current date.

Clean UI: A sidebar for controls keeps the main view uncluttered. Completed tasks are neatly tucked into an expander.

📥 Data Export:

Export your entire task list to a CSV file with a single click.

🛠️ Tech Stack
Framework: Streamlit

Language: Python 3

Database: SQLite3

Data Handling: Pandas (for CSV export)

⚙️ Setup and Local Installation
To run this project on your local machine, follow these steps:

1. Prerequisites:

Python 3.8 or higher installed.

2. Clone the Repository:

git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name

3. Create a Virtual Environment (Recommended):

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies:
The requirements.txt file contains all necessary libraries.

pip install -r requirements.txt

5. Run the Application:

streamlit run todo_app.py

The application will open in a new tab in your default web browser.

☁️ Deployment
This application is ready for deployment on Streamlit Community Cloud.

Push the project code (including todo_app.py and requirements.txt) to a public GitHub repository.

Sign up for Streamlit Community Cloud using your GitHub account.

Click "New app" and select the repository.

Ensure the main file path is set to todo_app.py and click "Deploy!".

🌟 Future Improvements
User Authentication: Add user accounts to allow multiple people to use the app with their own private to-do lists.

Calendar View: A visual calendar to show task due dates.

Email Reminders: Send automated email reminders for upcoming or overdue tasks.

Themes: Allow users to switch between light and dark modes.
