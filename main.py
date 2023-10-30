import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as mb

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.png')
        self.add_img = self.add_img.subsample(5,5)
        
        self.refresh_img = tk.PhotoImage(file='update.png')
        self.refresh_img = self.refresh_img.subsample(5,5)

        self.del_img = tk.PhotoImage(file='del.png')
        self.del_img = self.del_img.subsample(5,5)

        self.sear_img = tk.PhotoImage(file='search.png')
        self.sear_img = self.sear_img.subsample(5,5)

        self.total_upd_img = tk.PhotoImage(file='total_upd.png')
        self.total_upd_img = self.total_upd_img.subsample(5,5)


        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=0, width=100, height=100,
                            image=self.add_img, command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0, width=100, height=100,
                            image=self.refresh_img, command=self.open_update_dialog)
        btn_refresh.pack(side=tk.LEFT)

        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0, width=100, height=100,
                            image=self.del_img, command=self.delete_records)
        btn_del.pack(side=tk.LEFT)

        btn_sear = tk.Button(toolbar, bg='#d7d7d7', bd=0, width=100, height=100,
                            image=self.sear_img, command=self.open_search_dialog)
        btn_sear.pack(side=tk.LEFT)
    
        btn_total_upd = tk.Button(toolbar, bg='#d7d7d7', bd=0, width=100, height=100,
                            image=self.total_upd_img, command=self.total_update)
        btn_total_upd.pack(side=tk.LEFT)


        self.tree = ttk.Treeview(self, columns= ('ID', 'name', 'phone', 'email', 'profit'),
                                 height=45, show='headings')
        
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('profit', width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("profit", text="Заработная плата")

        self.tree.pack(side=tk.LEFT)
        self.total_update()
        self.scroll = tk.Scrollbar(self, command=self.tree.yview)
        self.scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scroll.set)

    def total_update(self):
        try:
            self.tree.delete(*self.tree.get_children())
        except:
            pass
        sqlite_select_query = """SELECT * from users"""
        db.cursor.execute(sqlite_select_query)
        self.record = db.cursor.fetchall()
        for row in self.record:
            self.tree.insert('', tk.END, values=row)
        
    def show_warning(self):
        msg = "Вы не выбрали нужную строку, для редактирования"
        mb.showwarning("Предупреждение", msg)


    def delete_records(self):
        for row in self.tree.selection():
            self.db.cursor.execute("""DELETE FROM users WHERE ID=?""", (self.tree.set(row, "#1"), ))
        self.db.conn.commit()
        self.total_update()

    def records(self, name, phone, email, profit):
        self.db.insert_data(name, phone, email, profit)
        self.total_update()

    def update_record(self, name, phone, email, profit):
        try:
            id = self.tree.set(self.tree.selection()[0], '#1')
            self.db.cursor.execute("""UPDATE users SET name=?, phone=?, email=?, profit=? WHERE ID=?""",
                                (name, phone, email, profit, id))
            self.db.conn.commit()
            self.total_update()
        except:
            Update.destroy(self)
            self.show_warning()
            self.total_update()

    def search_records(self, name):
        name = ("%" + name + "%")
        self.tree.delete(*self.tree.get_children())
        db.cursor.execute("""SELECT * FROM users WHERE name LIKE ?""", (name, ))
        self.record = db.cursor.fetchall()
        for row in self.record:
            self.tree.insert('', tk.END, values=row)
            # print(row)
    
    def open_child(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить сотрудника компании')
        self.geometry('400x200')
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=110)
        label_profit = tk.Label(self, text='Заработная плата:')
        label_profit.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_profit = ttk.Entry(self)
        self.entry_profit.place(x=200, y=140)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                          self.view.records(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_profit.get()))


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()
        self.view = app
    
    def init_update(self):
        self.title('Редактировать позицию')
        self.btn_add.destroy()
        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind("<Button-1>", lambda event:
                        self.view.update_record(self.entry_name.get(),
                                            self.entry_phone.get(),
                                            self.entry_email.get(),
                                            self.entry_profit.get()))

        self.btn_upd.bind("<Button-1>", lambda event: self.destroy(), add='+')
        self.btn_upd.place(x=200, y=170)

    def default_data(self):
        try:
            id = self.view.tree.set(self.view.tree.selection()[0], '#1')
            self.db.cursor.execute("""SELECT * FROM users WHERE ID=?""", (id, ))

            row = db.cursor.fetchone()
            self.entry_name.insert(0, row[1])
            self.entry_phone.insert(0, row[2])
            self.entry_email.insert(0, row[3])
            self.entry_profit.insert(0, row[4])
        except:
            pass

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY NOT NULL,
                            name TEXT,
                            phone TEXT,
                            email TEXT,
                            profit INTEGER ) """)
        self.conn.commit()

    def insert_data(self, name, phone, email, profit):
        self.cursor.execute("""INSERT INTO users (name, phone, email, profit)
                            VALUES (?, ?, ?, ?)""", (name, phone, email, profit))
        self.conn.commit()

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    
    def init_child(self):
        self.title('Поиск по сотруднику')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=20, y=20)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=70, y=20)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)

        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind("<Button-1>", lambda event: self.view.search_records(self.entry_name.get()))
        self.btn_search.bind("<Button-1>", lambda event: self.destroy(), add='+')



if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('795x450')
    root.resizable(False, False)
    root.configure(bg='white')
    root.mainloop()