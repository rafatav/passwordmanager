from tkinter import Tk, Canvas, Label, Entry, Button, PhotoImage, END, messagebox
from random import randint, choice, shuffle
import pyperclip
import json

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def add_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def read_data():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
            web_list = json.load(file)
        return web_list
    except:
        return None


def search_website():
    web_list = read_data()
    if web_list is None:
        messagebox.showerror(title="Oops", message="Não há websites cadastrados.")
        return
    website = website_entry.get()
    for web in web_list:
        try:
            if web[website]:
                messagebox.showinfo(title=website, message=f"Email: {web[website]["email"]}\n"
                                                           f"Password: {web[website]["password"]}")
                return
        except KeyError:
            pass
    messagebox.showerror(title="Oops", message="Website não encontrado")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def create_password():
    password_entry.delete(0, END)

    password_list = []

    [password_list.append(choice(letters)) for _ in range(randint(8, 10))]
    [password_list.append(choice(symbols)) for _ in range(randint(2, 4))]
    [password_list.append(choice(numbers)) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    if read_data() is not None:
        for i in range(len(read_data())):
            data_list.append(read_data()[i])
    else:
        pass
    data_list.append({website: {"email": email, "password": password}})
    if website == "" or password == "" or email == "":
        messagebox.showerror(title="Oops", message="Por favor, não deixe nenhuma entrada vazia!")
    else:
        if messagebox.askokcancel(title=website, message=f"Email: {email}\n"
                                                         f"Senha: {password}\nProceder com essas informações?"):
            add_data(data_list)
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
data_list = []

window = Tk()
window.title("Password Manager")
window.configure(padx=50, pady=50)

image = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
image.create_image(100, 100, image=logo)
image.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1, sticky="E")

email_label = Label(text="Email/Usuário:")
email_label.grid(column=0, row=2, sticky="E")

password_label = Label(text="Senha:")
password_label.grid(column=0, row=3, sticky="E")

website_entry = Entry()
website_entry.grid(column=1, row=1, columnspan=2, sticky="EW")
website_entry.focus()

email_entry = Entry()
email_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
email_entry.insert(0, "tavares.rfl@gmail.com")

password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")

generate_pass_button = Button(text="Gerar Senha ", command=create_password)
generate_pass_button.grid(column=2, row=3)

add_pass = Button(text="Adicionar", command=save)
add_pass.grid(column=1, row=4, columnspan=2, sticky="EW")

search_button = Button(text="Procurar", command=search_website)
search_button.grid(column=2, row=1, sticky="EW")

window.mainloop()
