import tkinter as tk
import tkinter.ttk as ttk
import psycopg2
from tkinter import PhotoImage
import pathlib

class Table(tk.Frame):
    def __init__(self, parent=None, headings=tuple(), displaycolumns=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"] = headings
        table["displaycolumns"] = displaycolumns

        for head in headings:
            table.heading(head, text=head, anchor=tk.CENTER)
            table.column(head, anchor=tk.CENTER)

        for row in rows:
            table.insert('', tk.END, values=tuple(row))

        scrolltable = tk.Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        table.pack(expand=tk.YES, fill=tk.BOTH)

params = {
    'host': 'localhost',
    'database': 'Bank',
    'user': 'postgres',
    'password': '1qaz!QAZ'
}

def load_data():
        with psycopg2.connect(**params) as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT s.id, s.transactionid, CONCAT(c1.firstname,' ',c1.lastname) AS sender_fullname, CONCAT(c2.firstname,' ',c2.lastname) AS receiver_fullname, s.amount, s.transaction_date, s.comm
        FROM suspensiontransactions s
        JOIN bankaccounts b1 ON s.senderaccountid = b1.id
        JOIN bankaccounts b2 ON s.receiveraccountid = b2.id
        JOIN clients c1 ON b1.clientid = c1.id
        JOIN clients c2 ON b2.clientid = c2.id;''')
            data = cursor.fetchall()

        table = Table(table_frame, headings=('id', 'transactionid', 'Отправитель', 'Получатель', 'Сумма транзакции', 'Дата транзакции', 'Описание'), displaycolumns=('Отправитель', 'Получатель', 'Сумма транзакции', 'Дата транзакции', 'Описание'), rows=data)
        table.pack(expand=tk.YES, fill=tk.BOTH)

def close_window():
    root.destroy()

root = tk.Tk()

root.attributes("-fullscreen", True)

img_file_name_back = "icons/background_1.png"
current_dir = pathlib.Path(__file__).resolve().parent
img_path_back = current_dir / img_file_name_back
background_image = PhotoImage(file=img_path_back)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

table_frame = tk.Frame(root, bg='white')
table_frame.place(x=50, y=50, relwidth=0.9, relheight=0.5)

img_file_name_load = "icons/load_icon.png"
img_path_load = current_dir / img_file_name_load
icon_image_load = PhotoImage(file=img_path_load)
load_button = tk.Button(root, text="Загрузить данные", image=icon_image_load, command=load_data)
load_button.place(relx=0.5, y=20, anchor=tk.CENTER, width=50, height=50)

img_file_name_close = "icons/close_icon.png"
img_path_close = current_dir / img_file_name_close
icon_image_close = PhotoImage(file=img_path_close)
close_button = tk.Button(root, image=icon_image_close, width=50, height=50, command=close_window)
close_button.place(x=root.winfo_screenwidth() - 70, y=20)

root.mainloop()
