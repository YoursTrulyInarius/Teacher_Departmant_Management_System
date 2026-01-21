import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class InformationSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Management System")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f4f4f9")

        self.db = Database()
        self.selected_item = None

        self.setup_styles()
        self.create_widgets()
        self.load_records()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure Treeview
        style.configure("Treeview", 
                        background="#ffffff", 
                        foreground="#333333", 
                        rowheight=30, 
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#0078d7")])
        
        style.configure("Treeview.Heading", 
                        background="#0078d7", 
                        foreground="white", 
                        font=("Segoe UI", 10, "bold"))
        
        # Buttons
        style.configure("Action.TButton", font=("Segoe UI", 10), padding=5)

    def create_widgets(self):
        # Sidebar/Form Container
        self.form_frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20, width=300)
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.form_frame.pack_propagate(False)

        tk.Label(self.form_frame, text="Teacher Record", font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#0078d7").pack(pady=(0, 20))

        # Form Fields
        self.fields = {}
        labels = ["First Name", "Last Name", "Email", "Department", "Phone", "Address"]
        for label in labels:
            tk.Label(self.form_frame, text=label, bg="#ffffff", font=("Segoe UI", 10)).pack(anchor=tk.W)
            entry = tk.Entry(self.form_frame, font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
            entry.pack(fill=tk.X, pady=(0, 10))
            self.fields[label] = entry

        # Action Buttons
        btn_container = tk.Frame(self.form_frame, bg="#ffffff")
        btn_container.pack(fill=tk.X, pady=20)

        self.add_btn = tk.Button(btn_container, text="Add Record", command=self.add_record, bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=10, pady=5)
        self.add_btn.pack(fill=tk.X, pady=5)

        self.update_btn = tk.Button(btn_container, text="Update Record", command=self.update_record, bg="#ffc107", fg="#333", font=("Segoe UI", 10, "bold"), bd=0, padx=10, pady=5)
        self.update_btn.pack(fill=tk.X, pady=5)

        self.delete_btn = tk.Button(btn_container, text="Delete Record", command=self.delete_record, bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=10, pady=5)
        self.delete_btn.pack(fill=tk.X, pady=5)

        self.clear_btn = tk.Button(btn_container, text="Clear Fields", command=self.clear_fields, bg="#6c757d", fg="white", font=("Segoe UI", 10, "bold"), bd=0, padx=10, pady=5)
        self.clear_btn.pack(fill=tk.X, pady=5)

        # Main Content Area
        self.content_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Search bar
        search_frame = tk.Frame(self.content_frame, bg="#f4f4f9")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg="#f4f4f9", font=("Segoe UI", 10)).pack(side=tk.LEFT)
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
        self.search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.search_records)

        # Table
        columns = ("ID", "First Name", "Last Name", "Email", "Department", "Phone", "Address")
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120 if col in ["Email", "Address", "Department"] else 100)
        
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.db.fetch_records()
        for record in records:
            self.tree.insert("", tk.END, values=record)

    def on_item_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, "values")
            self.selected_item = values[0] # ID
            
            # Fill form
            self.fields["First Name"].delete(0, tk.END)
            self.fields["First Name"].insert(0, values[1])
            self.fields["Last Name"].delete(0, tk.END)
            self.fields["Last Name"].insert(0, values[2])
            self.fields["Email"].delete(0, tk.END)
            self.fields["Email"].insert(0, values[3])
            self.fields["Department"].delete(0, tk.END)
            self.fields["Department"].insert(0, values[4])
            self.fields["Phone"].delete(0, tk.END)
            self.fields["Phone"].insert(0, values[5])
            self.fields["Address"].delete(0, tk.END)
            self.fields["Address"].insert(0, values[6])

    def add_record(self):
        data = {k: v.get() for k, v in self.fields.items()}
        if not data["First Name"] or not data["Last Name"]:
            messagebox.showwarning("Validation Error", "First and Last Name are required.")
            return
        
        self.db.add_record(data["First Name"], data["Last Name"], data["Email"], data["Department"], data["Phone"], data["Address"])
        messagebox.showinfo("Success", "Teacher record added successfully.")
        self.clear_fields()
        self.load_records()

    def update_record(self):
        if not self.selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update.")
            return
        
        data = {k: v.get() for k, v in self.fields.items()}
        self.db.update_record(self.selected_item, data["First Name"], data["Last Name"], data["Email"], data["Department"], data["Phone"], data["Address"])
        messagebox.showinfo("Success", "Teacher record updated successfully.")
        self.clear_fields()
        self.load_records()

    def delete_record(self):
        if not self.selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            self.db.delete_record(self.selected_item)
            messagebox.showinfo("Success", "Record deleted successfully.")
            self.clear_fields()
            self.load_records()

    def clear_fields(self):
        self.selected_item = None
        for entry in self.fields.values():
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    def search_records(self, event=None):
        term = self.search_entry.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.db.search_records(term)
        for record in records:
            self.tree.insert("", tk.END, values=record)

if __name__ == "__main__":
    root = tk.Tk()
    app = InformationSystemApp(root)
    root.mainloop()
