import tkinter as tk
from models.rotas import Rota
from tkinter import messagebox
from PIL import Image, ImageTk


class VanJaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitoramento de Rotas de Van")
        self.root.geometry("800x500")
        self.usuario_logado = None

        self.cabecalho()

        # titulo do frame verder
        self.f = tk.Frame(self.root, bg="#103F35")
        self.f.pack(fill=tk.X, ipady=100)
        self.title_frame = tk.Label(
            self.f,
            text="Van Já: Sua Rota Diária e Segura\n Para Picos-PI",
            bg="#103f35",
            fg="white",
            font=("Arial", 22, "bold"),
        )
        self.title_frame.pack(side="top", padx=10, pady=15)

        # frase abaixo do titulo
        self.merchan_lbl = tk.Label(
            self.f,
            text="Planos mensais ou passagens diárias. Encontre sua rota universitária.",
            bg="#103f35",
            fg="white",
        )
        self.merchan_lbl.pack(side="top")
        # barra de pesquisa
        self.search_frame = tk.Frame(self.f, bg="#103f35")
        self.search_frame.pack(side="top", pady=20)

        # Campo de Origem
        self.origem_lbl = tk.Label(
            self.search_frame, text="Origem:", bg="#103f35", fg="white"
        )
        self.origem_lbl.pack(side="left", padx=(0, 5))
        self.origem_ent = tk.Entry(self.search_frame)
        self.origem_ent.pack(side="left", ipadx=50)

        # Campo de Destino
        self.destino_lbl = tk.Label(
            self.search_frame, text="Destino:", bg="#103f35", fg="white"
        )
        self.destino_lbl.pack(side="left", padx=(10, 5))
        self.destino_ent = tk.Entry(self.search_frame)
        self.destino_ent.pack(side="left", ipadx=50)

        # Botão de busca
        self.search_btn = tk.Button(
            self.search_frame,
            text="Buscar",
            bg="#3A7C63",
            fg="white",
            font=("Helvetica", 10),
            command=self.buscar_rota,
        )
        self.search_btn.pack(side="left", padx=10)

        self.outdoor_fr = tk.Frame(self.f)
        self.outdoor_lbl = tk.Label(
            self.f,
            text="Vans Confortáveis   Motoristas Treinados    Suporte Rápido",
            bg="#B9D9C6",
            fg="black",
        )
        self.outdoor_lbl.pack(fill="x", side="top")
        # Lista de rotas (pode ser expandida depois)
        # self.routes_listbox = tk.Listbox(self.root, width=50, height=10)
        # self.routes_listbox.pack(pady=10)

        # Botão para ver detalhes (exemplo de callback OO)
        self.details_button = tk.Button(
            self.root, text="Ver Detalhes", command=self.ver_detalhes
        )
        self.details_button.pack(pady=10)

    def buscar_rota(self):
        origem = self.origem_ent.get()
        destino = self.destino_ent.get()

        if origem and destino:
            messagebox.showinfo(
                "Busca de Rotas",
                f"Ainda não há rotas disponíveis entre {origem} e {destino}.",
            )
        else:
            messagebox.showerror(
                "Erro", "Por favor, preencha os campos de origem e destino."
            )

    def cabecalho(self):
        self.header = tk.Frame(self.root, bg="#FFFFFF", height=50)
        self.header.pack(fill=tk.X)
        # Logo
        self.logo = tk.PhotoImage(file="views/Logo.png")
        self.logo_lbl = tk.Label(self.header, image=self.logo, bg="white")
        self.logo_lbl.image = self.logo
        self.logo_lbl.grid(row=0, column=0, padx=0)

        # Frame de botões
        self.frame_btns = tk.Frame(self.header, bg="#ffffff")
        self.frame_btns.grid(row=0, column=1)

        self.horarios_btn = tk.Button(
            self.frame_btns,
            text="Ajuda",
            bg="#ffffff",
            fg="black",
            font=("Arial", 12, "bold"),
            command=self.tela_ajuda,
        )
        self.horarios_btn.pack(side="left", padx=10)

        # --- Área de Login/Logout ---
        self.login_frame = tk.Frame(self.header, bg="#FFFFFF")
        self.login_frame.grid(row=0, column=2, padx=10)

        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            bg="#FFFFFF",
            fg="black",
            font="bold",
            command=self.tela_login,
        )
        self.login_button.pack()

        # pós login
        self.welcome_lbl = tk.Label(
            self.login_frame,
            text="",
            bg="#FFFFFF",
            fg="green",
            font=("Arial", 10, "bold"),
        )
        self.logout_button = tk.Button(
            self.login_frame,
            text="Sair",
            bg="#FFFFFF",
            fg="#F86666",
            font="bold",
            command=self.fazer_logout,
        )

        self.header.grid_columnconfigure(1, weight=1)

    def ver_detalhes(self):
        pass

    def tela_login(self):
        self.login = tk.Toplevel()
        self.login.title("Tela de login")
        self.login.geometry("400x600")
        self.frame = tk.Frame(self.login, bg="#103f35", bd=2, relief="groove")
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=350)

        self.close_btn = tk.Button(
            self.frame,
            text="X",
            command=self.login.destroy,
            bd=0,
            fg="red",
            font=("Arial", 10, "bold"),
        )
        self.close_btn.place(relx=1.0, rely=0.0, anchor="ne")

        self.email_lbl = tk.Label(self.frame, text="Email:", bg="#103f35", fg="white")
        self.email_lbl.place(relx=0.12, rely=0.18, anchor="w")
        self.email_ent = tk.Entry(self.frame, width=28)
        self.email_ent.place(relx=0.5, rely=0.25, anchor="center")

        self.senha_lbl = tk.Label(self.frame, text="Senha:", bg="#103f35", fg="white")
        self.senha_lbl.place(relx=0.12, rely=0.38, anchor="w")
        self.senha_ent = tk.Entry(self.frame, show="*", width=28)
        self.senha_ent.place(relx=0.5, rely=0.45, anchor="center")

        self.logar_btn = tk.Button(self.frame, text="Logar", command=self.validar_login)
        self.logar_btn.place(relx=0.5, rely=0.6, anchor="center", height=25)

        # tela de cadastro
        self.cadastro_lbl = tk.Label(
            self.frame,
            text="Não é cadastrado ainda? Clique no botão abaixo",
            bg="#103f35",
            fg="white",
            font=("Default", 8),
        )
        self.cadastro_lbl.place(relx=0.5, rely=0.80, anchor="center")
        self.cadastrar_btn = tk.Button(
            self.frame, text="Cadastrar", command=self.tela_cadastro
        )
        self.cadastrar_btn.place(
            relx=0.5, rely=0.9, anchor="center", height=20, width=75
        )

    def validar_login(self):
        from controllers.controler import validar_login

        email = self.email_ent.get()
        senha = self.senha_ent.get()

        usuario = validar_login(email, senha)

        if usuario:
            messagebox.showinfo("Login", "Login Realizado com Sucesso.")
            self.login.destroy()
            self.usuario_logado = usuario
            self.atualizar_interface_login()
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    def tela_cadastro(self):
        self.cadastro = tk.Toplevel()
        self.cadastro.title("Cadastro de Usuário")
        self.cadastro.geometry("400x600")
        frame = tk.Frame(self.cadastro, bg="#103f35", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=350)

        close_btn = tk.Button(
            frame,
            text="X",
            command=self.cadastro.destroy,
            bd=0,
            fg="red",
            font=("Arial", 10, "bold"),
        )
        close_btn.place(relx=1.0, rely=0.0, anchor="ne")

        nome_lbl = tk.Label(frame, text="Nome:", bg="#103f35", fg="white")
        nome_lbl.place(relx=0.12, rely=0.15, anchor="w")
        self.nome_ent = tk.Entry(frame, width=28)
        self.nome_ent.place(relx=0.5, rely=0.22, anchor="center")

        email_lbl = tk.Label(frame, text="Email:", bg="#103f35", fg="white")
        email_lbl.place(relx=0.12, rely=0.35, anchor="w")
        self.cad_email_ent = tk.Entry(frame, width=28)
        self.cad_email_ent.place(relx=0.5, rely=0.42, anchor="center")

        senha_lbl = tk.Label(frame, text="Senha:", bg="#103f35", fg="white")
        senha_lbl.place(relx=0.12, rely=0.55, anchor="w")
        self.cad_senha_ent = tk.Entry(frame, show="*", width=28)
        self.cad_senha_ent.place(relx=0.5, rely=0.62, anchor="center")

        tel_lbl = tk.Label(frame, text="Telefone:", bg="#103f35", fg="white")
        tel_lbl.place(relx=0.12, rely=0.75, anchor="w")
        self.tel_ent = tk.Entry(frame, width=28)
        self.tel_ent.place(relx=0.5, rely=0.82, anchor="center")

        cadastrar_btn = tk.Button(
            frame, text="Cadastrar", command=self.cadastrar_usuario
        )
        cadastrar_btn.place(relx=0.5, rely=0.93, anchor="center")

    def cadastrar_usuario(self):
        from controllers.controler import cadastrar_usuario

        nome = self.nome_ent.get()
        email = self.cad_email_ent.get()
        senha = self.cad_senha_ent.get()
        telefone = self.tel_ent.get()
        if nome and email and senha and telefone:
            sucesso = cadastrar_usuario(nome, email, senha, telefone)
            if sucesso:
                messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
                self.cadastro.destroy()
            else:
                messagebox.showerror("Erro", "Email já cadastrado!")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def atualizar_interface_login(self):
        self.login_button.pack_forget()

        primeiro_nome = self.usuario_logado["nome"].split()[0]
        self.welcome_lbl.config(text=f"Olá, {primeiro_nome}!")
        self.welcome_lbl.pack(side="left", padx=5)
        self.logout_button.pack(side="left")

    def fazer_logout(self):
        self.usuario_logado = None

        self.welcome_lbl.pack_forget()
        self.logout_button.pack_forget()

        self.login_button.pack()
        messagebox.showinfo("Logout", "Você saiu da sua conta.")

    def tela_ajuda(self):
        ajuda_window = tk.Toplevel(self.root)
        ajuda_window.title("Ajuda / Suporte")
        ajuda_window.geometry("450x300")
        ajuda_window.configure(bg="#f0f0f0")
        ajuda_window.resizable(False, False)

        # Título dentro da janela de ajuda
        titulo_lbl = tk.Label(
            ajuda_window,
            text="Central de Ajuda",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
        )
        titulo_lbl.pack(pady=(20, 10))

        # Texto de ajuda
        texto_ajuda = (
            "Bem-vindo à Central de Ajuda do Van Já!\n\n"
            "• Para buscar uma rota, utilize os campos 'Origem' e\n 'Destino' na tela principal.\n\n"
            "• Para fazer login ou se cadastrar, clique no botão 'Login'\n no canto superior direito.\n\n"
            "Para suporte adicional, entre em contato:\n"
        )

        ajuda_lbl = tk.Label(
            ajuda_window,
            text=texto_ajuda,
            justify="left",
            wraplength=400,
            bg="#f0f0f0",
        )
        ajuda_lbl.pack(pady=5, padx=20)


if __name__ == "__main__":
    Rota("Rota 1", ["Parada A", "Parada B"], "08:00 - 18:00")
    Rota("Rota 2", ["Parada C", "Parada D"], "09:00 - 19:00")
    root = tk.Tk()
    app = VanJaApp(root)
    root.mainloop()
