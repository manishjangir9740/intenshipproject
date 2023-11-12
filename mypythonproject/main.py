import tkinter as tk
from tkinter import END, Listbox, Entry, Button, Scrollbar, PhotoImage, Label, StringVar
import os

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("400x700+400+100")
        self.root.resizable(False, False)

        self.task_list = []

        # ICON
        image_icon = PhotoImage(file="Images/To-Do-List1.png")
        self.root.iconphoto(False, image_icon)  


        # TOP BAR
        Top_Image=PhotoImage(file="Images/Topbar2.png")
        Label(self.root, image=Top_Image).pack()

        

        dock_Image=PhotoImage(file="Images/Logodus1.png")
        Label(self.root, image=dock_Image, bg="#02605B").place(x=30, y=25)

        note_image = PhotoImage(file="Images/To-Do-List1.png")
        Label(self.root, image=note_image, bg="#000000").place(x=340, y=25)

        heading = tk.Label(self.root, text="TASKS", font="arial 20 bold", fg="white", bg="#016A65")
        heading.place(x=155, y=25)
        note_Image=PhotoImage(file="Images/To-Do-List1.png")
        Label(self.root, image=note_Image, bg="#015A54").place(x=340, y=25)

        # MAIN
        frame = tk.Frame(self.root, width=400, height=50, bg="white")
        frame.place(x=0, y=180)

        self.task_var = StringVar()
        self.task_entry = Entry(frame, textvariable=self.task_var, width=18, font="arial 20", bd=0)
        self.task_entry.place(x=10, y=7)
        self.task_entry.focus()

        add_button = Button(frame, text="Add", font="arial 20 bold", width=6, bg="#5a95ff", fg="#fff", bd=0, command=self.add_task)
        add_button.place(x=300, y=0)

        delete_button = Button(self.root, text="Delete", font="arial 12", command=self.delete_task)
        delete_button.pack(side=tk.BOTTOM, pady=5)

        update_button = Button(self.root, text="Update", font="arial 12", command=self.update_task)
        update_button.pack(side=tk.BOTTOM, pady=5)

        complete_button = Button(self.root, text="Mark as Completed", font="arial 12", command=self.mark_as_completed)
        complete_button.pack(side=tk.BOTTOM, pady=5)

        # LISTBOX
        frame1 = tk.Frame(self.root, bd=3, width=700, height=280, bg="#32485b")
        frame1.pack(pady=(160, 0))

        self.listbox = Listbox(frame1, font=("arial", 12), width=40, height=16, bg="#32405b", fg="white", cursor="hand2", selectbackground="#5a95ff")
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=2)

        scrollbar = Scrollbar(frame1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.open_task_file()

    def add_task(self):
        task = self.task_var.get()
        self.task_entry.delete(0, END)
        if task:
            with open("tasklist.txt", "a") as taskfile:
                taskfile.write(f"\n{task}")
            self.task_list.append(task)
            self.listbox.insert(END, task)

    def delete_task(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            selected_task_index = int(selected_task_index[0])
            task = self.listbox.get(selected_task_index)
            if task in self.task_list:
                self.task_list.remove(task)
                with open("tasklist.txt", "w") as taskfile:
                    for t in self.task_list:
                        taskfile.write(t + "\n")
                self.listbox.delete(selected_task_index)

    def open_task_file(self):
        try:
            with open("tasklist.txt", "r") as taskfile:
                tasks = taskfile.readlines()

            for task in tasks:
                if task != "\n":
                    self.task_list.append(task.strip())
                    self.listbox.insert(END, task.strip())

        except FileNotFoundError:
            file = open("tasklist.txt", "w")
            file.close()

    def update_task(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            selected_task_index = int(selected_task_index[0])
            task = self.listbox.get(selected_task_index)

            # Create a new window for updating the task
            update_window = tk.Toplevel(self.root)
            update_window.title("Update Task")

            # Entry widget for updating the task
            update_entry = Entry(update_window, width=30, font="arial 12", bd=5)
            update_entry.insert(0, task)
            update_entry.pack(pady=10)

            # Button to perform the update
            update_button = Button(update_window, text="Update", font="arial 12 bold", command=lambda: self.perform_update(update_window, update_entry, selected_task_index))
            update_button.pack()

    def perform_update(self, update_window, update_entry, selected_task_index):
        updated_task = update_entry.get()
        if updated_task:
            self.task_list[selected_task_index] = updated_task
            self.listbox.delete(selected_task_index)
            self.listbox.insert(selected_task_index, updated_task)
            with open("tasklist.txt", "w") as taskfile:
                for t in self.task_list:
                    taskfile.write(t + "\n")
        update_window.destroy()

    def mark_as_completed(self):
        selected_task_index = self.listbox.curselection()
        if selected_task_index:
            selected_task_index = int(selected_task_index[0])
            task = self.listbox.get(selected_task_index)
            if "(Completed)" not in task:
                updated_task = task + " (Completed)"
                self.task_list[selected_task_index] = updated_task
                self.listbox.delete(selected_task_index)
                self.listbox.insert(selected_task_index, updated_task)
                with open("tasklist.txt", "w") as taskfile:
                    for t in self.task_list:
                        taskfile.write(t + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
