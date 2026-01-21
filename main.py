import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class InformationSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Management System")
        self.root.geometry("1100x800")
        self.root.configure(bg="#f4f4f9")

        self.db = Database()
        self.selected_item = None

        self.setup_styles()
        self.create_widgets()
        self.load_records()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Professional Colors
        self.colors = {
            "primary": "#2c3e50",    # Dark Midnight
            "secondary": "#34495e",  # Lighter Midnight
            "accent": "#3498db",     # Bright Blue
            "bg": "#f8f9fa",         # Light Gray Bg
            "white": "#ffffff",
            "success": "#27ae60",
            "warning": "#f39c12",
            "danger": "#e74c3c",
            "text": "#2c3e50"
        }

        # Configure Treeview
        style.configure("Treeview", 
                        background="#ffffff", 
                        foreground="#2c3e50", 
                        rowheight=35, 
                        fieldbackground="#ffffff",
                        font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", "#3498db")])
        
        style.configure("Treeview.Heading", 
                        background="#2c3e50", 
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview.Heading", background=[("active", "#34495e")])
        
        # Alternating row colors
        self.tree_tag_colors = ("#ffffff", "#f2f4f6")

    def create_widgets(self):
        # Sidebar/Form Container - Modern Dark Look
        self.sidebar = tk.Frame(self.root, bg=self.colors["primary"], padx=25, pady=30, width=320)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="TMS", font=("Segoe UI", 16, "bold"), 
                 bg=self.colors["primary"], fg=self.colors["white"]).pack(pady=(0, 30))

        # Form Fields with modern styling
        self.fields = {}
        labels = ["First Name", "Last Name", "Email", "Department", "Phone", "Address"]
        for label in labels:
            lbl = tk.Label(self.sidebar, text=label.upper(), bg=self.colors["primary"], 
                           fg="#bdc3c7", font=("Segoe UI", 8, "bold"))
            lbl.pack(anchor=tk.W, pady=(2, 0))
            
            entry = tk.Entry(self.sidebar, font=("Segoe UI", 10), bd=0, 
                             highlightthickness=1, highlightbackground="#34495e",
                             bg="#34495e", fg="white", insertbackground="white")
            entry.pack(fill=tk.X, pady=(1, 8), ipady=3)
            self.fields[label] = entry

        # Action Buttons Container
        btn_container = tk.Frame(self.sidebar, bg=self.colors["primary"])
        btn_container.pack(fill=tk.X, pady=(15, 0))

        def create_btn(text, cmd, color):
            btn = tk.Button(btn_container, text=text, command=cmd, bg=color, fg="white", 
                            font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2",
                            activebackground=color, activeforeground="white")
            btn.pack(fill=tk.X, pady=4, ipady=4)
            return btn

        self.add_btn = create_btn("ADD TEACHER", self.add_record, self.colors["success"])
        self.update_btn = create_btn("UPDATE RECORD", self.update_record, self.colors["warning"])
        self.delete_btn = create_btn("DELETE RECORD", self.delete_record, self.colors["danger"])
        
        tk.Frame(btn_container, height=1, bg="#34495e").pack(fill=tk.X, pady=15)
        self.clear_btn = create_btn("CLEAR FORM", self.clear_fields, "#7f8c8d")

        # Main Content Area
        self.content_frame = tk.Frame(self.root, bg="#f4f4f9", padx=20, pady=20)
        self.content_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Search bar - Modern Style
        search_frame = tk.Frame(self.content_frame, bg="#f4f4f9")
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(search_frame, text="SEARCH RECORDS:", bg="#f4f4f9", 
                 fg=self.colors["primary"], font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        
        self.search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), bd=0, 
                                     highlightthickness=1, highlightbackground="#dcdde1",
                                     bg="white")
        self.search_entry.pack(side=tk.LEFT, padx=15, fill=tk.X, expand=True, ipady=4)
        self.search_entry.bind("<KeyRelease>", self.search_records)

        # Table
        columns = ("ID", "First Name", "Last Name", "Email", "Department", "Phone", "Address")
        # Hide ID from displaycolumns
        self.tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", displaycolumns=columns[1:])
        
        for col in columns:
            if col != "ID":
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120 if col in ["Email", "Address", "Department"] else 100)
            else:
                self.tree.column(col, width=0, stretch=tk.NO)
        
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)

    def load_records(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        records = self.db.fetch_records()
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=record, tags=(tag,))
        
        self.tree.tag_configure('evenrow', background=self.tree_tag_colors[0])
        self.tree.tag_configure('oddrow', background=self.tree_tag_colors[1])

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
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=record, tags=(tag,))
        
        self.tree.tag_configure('evenrow', background=self.tree_tag_colors[0])
        self.tree.tag_configure('oddrow', background=self.tree_tag_colors[1])

if __name__ == "__main__":
    root = tk.Tk()
    app = InformationSystemApp(root)
    root.mainloop()
