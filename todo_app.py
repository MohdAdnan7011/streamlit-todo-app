import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import random

# --- DATABASE SETUP ---

# Function to create a connection to the SQLite database
def create_connection():
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect("tasks.db")  # Creates the file if it doesn't exist
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
    return conn

# Function to create the tasks table if it doesn't exist
def create_table(conn):
    """Create a tasks table."""
    try:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT,
                due_date DATE,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Table creation error: {e}")

# --- TASK MANAGEMENT FUNCTIONS ---

def add_task(conn, title, description, priority, due_date):
    """Add a new task to the database."""
    sql = ''' INSERT INTO tasks(title, description, priority, due_date, status)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (title, description, priority, due_date, "Pending"))
    conn.commit()
    return cur.lastrowid

def view_all_tasks(conn):
    """Query all rows in the tasks table."""
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY due_date ASC")
    rows = cur.fetchall()
    return rows

def update_task_status(conn, task_id, status):
    """Update a task's status."""
    sql = ''' UPDATE tasks
              SET status = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (status, task_id))
    conn.commit()

def update_task_details(conn, task_id, title, description, priority, due_date):
    """Update all details of a specific task."""
    sql = ''' UPDATE tasks
              SET title = ?,
                  description = ?,
                  priority = ?,
                  due_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (title, description, priority, due_date, task_id))
    conn.commit()


def delete_task(conn, task_id):
    """Delete a task by task id."""
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()

# --- HELPER FUNCTIONS ---

def get_motivational_quote():
    """Returns a random motivational quote."""
    quotes = [
        "The secret of getting ahead is getting started. - Mark Twain",
        "The best way to predict the future is to create it. - Peter Drucker",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "Well done is better than well said. - Benjamin Franklin",
        "It does not matter how slowly you go as long as you do not stop. - Confucius"
    ]
    return random.choice(quotes)

# --- UI LAYOUT ---

def main():
    st.set_page_config(page_title="ProducTODO ✔️", layout="wide", page_icon="✔️")

    # Initialize connection and create table
    conn = create_connection()
    if conn is not None:
        create_table(conn)
    else:
        st.error("Error! cannot create the database connection.")
        return

    # Initialize session state for editing
    if 'task_to_edit' not in st.session_state:
        st.session_state.task_to_edit = None

    # --- HEADER ---
    st.title("ProducTODO ✔️")
    st.markdown(f"> *{get_motivational_quote()}*")
    st.markdown("---")


    # --- SIDEBAR FOR CONTROLS ---
    st.sidebar.header("Controls & Filters")

    # Add new task form in the sidebar
    with st.sidebar.expander("➕ Add a New Task", expanded=True):
        with st.form("New Task Form", clear_on_submit=True):
            new_title = st.text_input("Title", max_chars=100, placeholder="e.g., Read a chapter of a book")
            new_desc = st.text_area("Description (Optional)", placeholder="Add more details here...")
            col1, col2 = st.columns(2)
            with col1:
                new_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            with col2:
                new_due_date = st.date_input("Due Date", min_value=date.today())
            
            submitted = st.form_submit_button("Add Task")
            if submitted and new_title:
                add_task(conn, new_title, new_desc, new_priority, new_due_date)
                st.sidebar.success("Task added successfully!")
                st.rerun()

    # Filters and Search
    search_query = st.sidebar.text_input("🔍 Search Tasks", placeholder="Search by keyword...")
    filter_priority = st.sidebar.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])
    filter_status = st.sidebar.selectbox("Filter by Status", ["All", "Pending", "Completed"])

    all_tasks = view_all_tasks(conn)

    # --- DASHBOARD / SUMMARY ---
    pending_tasks_count = sum(1 for task in all_tasks if task[5] == "Pending")
    completed_tasks_count = len(all_tasks) - pending_tasks_count
    total_tasks = len(all_tasks)

    st.header("Productivity Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("✅ Completed", f"{completed_tasks_count}")
    col3.metric("⏳ Pending", f"{pending_tasks_count}")
    if total_tasks > 0:
        completion_rate = (completed_tasks_count / total_tasks) * 100
        col4.metric("Completion Rate", f"{completion_rate:.2f}%")
        st.progress(completion_rate / 100)
    else:
        col4.metric("Completion Rate", "0%")
        st.progress(0)
    
    st.markdown("---")

    # --- TASK DISPLAY ---

    # Apply filters
    tasks_to_display = all_tasks
    if search_query:
        tasks_to_display = [t for t in tasks_to_display if search_query.lower() in t[1].lower() or search_query.lower() in t[2].lower()]
    if filter_priority != "All":
        tasks_to_display = [t for t in tasks_to_display if t[3] == filter_priority]
    if filter_status != "All":
        tasks_to_display = [t for t in tasks_to_display if t[5] == filter_status]

    # Display pending tasks
    st.header("Pending Tasks")
    pending_tasks = [task for task in tasks_to_display if task[5] == "Pending"]
    
    if not pending_tasks:
        st.info("🎉 No pending tasks! You're all caught up.")
    else:
        for task in pending_tasks:
            task_id, title, description, priority, due_date_str, status, _ = task
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            is_overdue = due_date < date.today()

            priority_map = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            
            task_container = st.container(border=True)
            with task_container:
                # Edit Form inside the container for a specific task
                if st.session_state.task_to_edit == task_id:
                    with st.form(f"edit_form_{task_id}"):
                        st.subheader(f"Editing Task: '{title}'")
                        edit_title = st.text_input("Title", value=title)
                        edit_desc = st.text_area("Description", value=description)
                        edit_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(priority))
                        edit_due_date = st.date_input("Due Date", value=due_date)
                        
                        c1, c2 = st.columns(2)
                        if c1.form_submit_button("Save Changes", use_container_width=True):
                            update_task_details(conn, task_id, edit_title, edit_desc, edit_priority, edit_due_date)
                            st.session_state.task_to_edit = None
                            st.rerun()
                        if c2.form_submit_button("Cancel", use_container_width=True):
                            st.session_state.task_to_edit = None
                            st.rerun()

                else:
                    cols = st.columns([1, 6, 2, 2, 2])
                    
                    # Column 1: Checkbox for completion
                    is_completed = cols[0].checkbox("", key=f"check_{task_id}")
                    if is_completed:
                        update_task_status(conn, task_id, "Completed")
                        st.rerun()

                    # Column 2: Title and Description
                    with cols[1]:
                        st.markdown(f"**{title}**")
                        if description:
                            with st.expander("Details"):
                                st.write(description)

                    # Column 3: Priority
                    cols[2].markdown(f"{priority_map.get(priority, '')} {priority}")
                    
                    # Column 4: Due Date
                    date_color = "red" if is_overdue else "gray"
                    cols[3].markdown(f"<span style='color:{date_color};'>🗓️ {due_date.strftime('%b %d, %Y')}</span>", unsafe_allow_html=True)
                    
                    # Column 5: Edit and Delete buttons
                    with cols[4]:
                        if st.button("✏️ Edit", key=f"edit_{task_id}", use_container_width=True):
                            st.session_state.task_to_edit = task_id
                            st.rerun()
                        if st.button("🗑️ Delete", key=f"del_{task_id}", use_container_width=True):
                            delete_task(conn, task_id)
                            st.rerun()
    
    # Display completed tasks in an expander
    st.markdown("---")
    with st.expander("✅ Completed Tasks"):
        completed_tasks = [task for task in tasks_to_display if task[5] == "Completed"]
        if not completed_tasks:
            st.write("No tasks completed yet.")
        else:
            for task in completed_tasks:
                task_id, title, _, _, _, _, _ = task
                cols = st.columns([1, 8, 2])
                # Un-complete checkbox
                uncomplete = cols[0].checkbox("", value=True, key=f"uncheck_{task_id}")
                if not uncomplete:
                    update_task_status(conn, task_id, "Pending")
                    st.rerun()

                cols[1].markdown(f"~~_{title}_~~")
                if cols[2].button("🗑️ Delete", key=f"del_comp_{task_id}", use_container_width=True):
                    delete_task(conn, task_id)
                    st.rerun()

    # --- EXPORT DATA ---
    if total_tasks > 0:
        df = pd.DataFrame(all_tasks, columns=['ID', 'Title', 'Description', 'Priority', 'Due Date', 'Status', 'Created At'])
        csv = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="📥 Export Tasks to CSV",
            data=csv,
            file_name='my_tasks.csv',
            mime='text/csv',
        )

    conn.close()

if __name__ == '__main__':
    main()