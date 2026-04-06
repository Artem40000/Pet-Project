import customtkinter as ctk
import psycopg2
import Login
from Prime import PrimeGo

conn = psycopg2.connect(dbname="Proj", user="postgres", password="12345", host="127.0.0.1")
cursor = conn.cursor()

def RegisterGo():
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


    def ClickLogin():
        root.destroy()
        Login.LoginGo()


    def Register():
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
            cursor.execute(f"INSERT INTO Person (Name, Password) VALUES (\'{name}\' , \'{InputPassword.get()}\')")
            conn.commit()
            root.destroy()
            PrimeGo(name)



    Text_MyAccount = ctk.CTkLabel(root, height=2, font=('Arial Black', 50), text='Register', fg_color='#5d6fd3')
    Text_MyAccount.pack()



    InputName = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Name:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputName.place(relx=0.5, y=200, anchor="center")

    InputPassword = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Password:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputPassword.place(relx=0.5, y=300, anchor="center")



    ButtonConfirm = ctk.CTkButton(root, width=300, height=60, fg_color='#213397', font=('Arial Black', 30), corner_radius=35, text='CONFIRM', hover_color='#3a4cb0', command=Register)
    ButtonConfirm.place(relx=0.5, y=400, anchor="center")

    ButtonLogin = ctk.CTkButton(root, width=50, height=50, fg_color='#213397', font=('Arial Black', 30), corner_radius=35, text='L', hover_color='#3a4cb0', command=ClickLogin)
    ButtonLogin.place(relx=0.94, y=35, anchor="center")

    TextError = ctk.CTkLabel(root, fg_color='#5d6fd3', font=('Arial Black', 30), text_color='DarkRed', text='')
    TextError.place(relx=0.5, y=500, anchor="center")

    root.mainloop()