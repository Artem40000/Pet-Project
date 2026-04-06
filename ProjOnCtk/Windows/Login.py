import customtkinter as ctk
import Register, psycopg2, Prime

conn = psycopg2.connect(dbname="Proj", user="postgres", password="12345", host="127.0.0.1")
cursor = conn.cursor()

def LoginGo():
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

    def ClickReg():
        root.destroy()
        Register.RegisterGo()

    def Login():
        name = InputName.get().strip()
        password = InputPassword.get().strip()
        cursor.execute(f"SELECT * FROM Person WHERE Name=\'{name}\'")
        All = cursor.fetchone()
        if not All: TextError.configure(text='Пользователь не существует!'); return

        Name = All[1]
        Password = All[2]

        if password != Password: TextError.configure(text='Неверный пароль!'); return

        if name == Name and password == Password: root.destroy(); Prime.PrimeGo(name)



    Text_MyAccount = ctk.CTkLabel(root, height=2, font=('Arial Black', 50), text='Login', fg_color='#5d6fd3')
    Text_MyAccount.pack()



    InputName = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Name:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputName.place(relx=0.5, y=200, anchor="center")

    InputPassword = ctk.CTkEntry(root, width=525, height=65, fg_color='#3aafff', font=('Arial Black', 30), corner_radius=20, placeholder_text="Password:", text_color='Black', placeholder_text_color='White', border_width=5, border_color='#1c2e92')
    InputPassword.place(relx=0.5, y=300, anchor="center")



    ButtonConfirm = ctk.CTkButton(root, width=300, height=60, fg_color='#213397', font=('Arial Black', 30), corner_radius=35, text='CONFIRM', hover_color='#3a4cb0', command=Login)
    ButtonConfirm.place(relx=0.5, y=400, anchor="center")

    ButtonReg = ctk.CTkButton(root, width=50, height=50, fg_color='#213397', font=('Arial Black', 30), corner_radius=35, text='R', hover_color='#3a4cb0', command=ClickReg)
    ButtonReg.place(relx=0.94, y=35, anchor="center")

    TextError = ctk.CTkLabel(root, width=50, height=50, fg_color='#5d6fd3', font=('Arial Black', 30), text='')
    TextError.place(relx=0.5, y=500, anchor="center")

    root.mainloop()