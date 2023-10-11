import tkinter as tk
import sqlite3
from tkinter import messagebox

# Initialize the SQLite database
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

# Modify your code to drop and recreate the table
cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, heading TEXT, content TEXT)''')
conn.commit()

def create_note():
    heading = heading_entry.get().strip()
    content = note_text.get("1.0", tk.END).strip()
    if heading and content:
        cursor.execute("INSERT INTO notes (heading, content) VALUES (?, ?)", (heading, content))
        conn.commit()
        messagebox.showinfo("Note Created", "Note has been created.")
        heading_entry.delete(0, tk.END)  # Clear the heading entry
        note_text.delete("1.0", tk.END)  # Clear the text widget
        list_notes()  # Refresh the list of notes

def list_notes():
    cursor.execute("SELECT id, heading FROM notes")
    notes = cursor.fetchall()
    if notes:
        notes_listbox.delete(0, tk.END)
        for note in notes:
            notes_listbox.insert(tk.END, f"{note[0]}. {note[1]}")

def read_selected_note():
    selected_index = notes_listbox.curselection()
    if selected_index:
        selected_id = int(notes_listbox.get(selected_index[0]).split(".")[0])
        cursor.execute("SELECT content, heading FROM notes WHERE id=?", (selected_id,))
        note = cursor.fetchone()
        if note:
            note_text.delete("1.0", tk.END)
            note_text.insert(tk.END, note[0])
            heading_entry.delete(0, tk.END)
            heading_entry.insert(0, note[1])

def delete_selected_note():
    selected_index = notes_listbox.curselection()
    if selected_index:
        selected_id = int(notes_listbox.get(selected_index[0]).split(".")[0])
        cursor.execute("DELETE FROM notes WHERE id=?", (selected_id,))
        conn.commit()
        messagebox.showinfo("Note Deleted", "Selected note has been deleted.")
        list_notes()  # Refresh the list of notes

app = tk.Tk()
app.title("Note Taking App")
app.geometry("600x400")

heading_label = tk.Label(app, text="Heading:")
heading_label.pack()
heading_entry = tk.Entry(app)
heading_entry.pack()

note_text = tk.Text(app)
note_text.pack(fill=tk.BOTH, expand=True)

notes_listbox = tk.Listbox(app, selectmode=tk.SINGLE)
notes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(app)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
notes_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=notes_listbox.yview)

create_button = tk.Button(app, text="Create Note", command=create_note)
create_button.pack()

list_button = tk.Button(app, text="List Notes", command=list_notes)
list_button.pack()

read_button = tk.Button(app, text="Read Note", command=read_selected_note)
read_button.pack()

delete_button = tk.Button(app, text="Delete Note", command=delete_selected_note)
delete_button.pack()

app.mainloop()
