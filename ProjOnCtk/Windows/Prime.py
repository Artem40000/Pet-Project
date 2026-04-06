import customtkinter as ctk
import psycopg2, Register

conn = psycopg2.connect(dbname="Proj", user="postgres", password="12345", host="127.0.0.1")
cursor = conn.cursor()

def PrimeGo(username):
    root = ctk.CTk()
    WindowWidth = 700
    WindowHeight = 600
    ScreenWidth = root.winfo_screenwidth()
    ScreenHeight = root.winfo_screenheight()
    x = int((ScreenWidth / 2) - (WindowWidth / 2))
    y = int((ScreenHeight / 2) - (WindowHeight / 2))
    root.geometry(f"{WindowWidth}x{WindowHeight}+{x}+{y}")
    root.resizable(False, False)
    root.configure(fg_color='#5d6fd3')

    cursor.execute(f"SELECT * FROM Person WHERE Name = \'{username}\'")
    user = cursor.fetchone()

    InputName = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Name:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputName.place(relx=0.5, y=200, anchor="center")

    InputPassword = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Password:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputPassword.place(relx=0.5, y=300, anchor="center")

    InputName.insert(0, user[1])
    InputPassword.insert(0, user[2])



    def Edit():
        name = InputName.get().strip()
        cursor.execute(f"SELECT Name FROM Person WHERE Name=\'{name}\'")
        ValidName = cursor.fetchone()
        if ValidName: ValidName = ValidName[0]

        if not name or not InputPassword.get().strip(): TextError.configure(text='Заполните поля!'); return
        elif len(name) > 30: TextError.configure(text="Длинное имя"); return
        elif len(InputPassword.get()) > 48: TextError.configure(text="Длинный пароль"); return
        elif len(name) < 4: TextError.configure(text="Короткое имя"); return
        elif len(InputPassword.get()) < 6: TextError.configure(text="Короткий пароль"); return
        elif ' ' in name or ' ' in InputPassword.get(): TextError.configure(text="Пробел в поле(ях)!"); return
        elif not str(name).isalpha(): TextError.configure(text="Некорректное имя!"); return

        if (ValidName is not None and ValidName == name) or (not ValidName and not name):
            TextError.configure(text="Такой пользователь есть!")
        else:
            cursor.execute(f"UPDATE Person SET Name=\'{name}\' WHERE Name=\'{username}\'")
            cursor.execute(f"UPDATE Person SET Password=\'{InputPassword.get()}\' WHERE Name=\'{name}\'")
            conn.commit()
            cursor.execute(f"SELECT * FROM Person WHERE Name=\'{name}\'")
            UserName = cursor.fetchone()
            if UserName: UserName = UserName[1]
            root.destroy()
            PrimeGo(UserName)



    def Delete():
        cursor.execute(f"DELETE FROM Person WHERE Name=\'{InputName.get().strip()}\'")
        conn.commit()
        root.destroy()
        Register.RegisterGo()



    Text_MyAccount = ctk.CTkLabel(root, height=2, font=('Arial Black', 40), text='My Account', fg_color='#5d6fd3')
    Text_MyAccount.pack()



    ButtonEdit = ctk.CTkButton(root, width=200, height=50, fg_color='Green', font=('Arial Black', 30), corner_radius=35, text='EDIT', hover_color='DarkGreen', command=Edit)
    ButtonEdit.place(relx=0.3, y=400, anchor="center")

    ButtonDelete = ctk.CTkButton(root, width=200, height=50, fg_color='Red', font=('Arial Black', 30), corner_radius=35, text='DELETE', hover_color='Crimson', command=Delete)
    ButtonDelete.place(relx=0.7, y=400, anchor="center")

    TextError = ctk.CTkLabel(root, fg_color='#5d6fd3', font=('Arial Black', 30), text_color='DarkRed', text='')
    TextError.place(relx=0.5, y=500, anchor="center")

    root.mainloop()