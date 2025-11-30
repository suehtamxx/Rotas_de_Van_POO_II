import tkinter as tk
from tkinter import messagebox


class TelaLoginFrame(tk.Frame):
    """
    Formulário de autenticação.
    Captura email e senha, comunicando-se com o controlador para validar o acesso de clientes e motoristas.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.frame_conteudo = tk.Frame(self, bg="#103f35", bd=2, relief="groove")
        self.frame_conteudo.place(
            relx=0.5, rely=0.5, anchor="center", width=300, height=350
        )

        close_btn = tk.Button(
            self.frame_conteudo,
            text="X",
            command=lambda: controlador.mostrar_frame("TelaPrincipalFrame"),
            bg="red",
            fg="white",
            font=("Arial", 10, "bold"),
        )
        close_btn.place(relx=1.0, rely=0.0, anchor="ne")

        # Inputs
        tk.Label(self.frame_conteudo, text="Email:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.18, anchor="w"
        )
        self.email_ent = tk.Entry(self.frame_conteudo, width=28)
        self.email_ent.place(relx=0.5, rely=0.25, anchor="center")

        tk.Label(self.frame_conteudo, text="Senha:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.38, anchor="w"
        )
        self.senha_ent = tk.Entry(self.frame_conteudo, show="*", width=28)
        self.senha_ent.place(relx=0.5, rely=0.45, anchor="center")

        tk.Button(self.frame_conteudo, text="Logar", command=self.enviar_login).place(
            relx=0.5, rely=0.6, anchor="center", height=25
        )

        tk.Label(
            self.frame_conteudo,
            text="Não é cadastrado ainda?",
            bg="#103f35",
            fg="white",
            font=("Default", 8),
        ).place(relx=0.5, rely=0.80, anchor="center")
        tk.Button(
            self.frame_conteudo,
            text="Cadastrar",
            command=lambda: controlador.mostrar_frame("TelaCadastroFrame"),
        ).place(relx=0.5, rely=0.9, anchor="center", height=20, width=75)

    def enviar_login(self):
        email = self.email_ent.get()
        senha = self.senha_ent.get()
        # O controlador conecta na API e retorna o objeto usuário ou None
        self.controlador.tentar_login(email, senha)


class TelaCadastroFrame(tk.Frame):
    """
    Formulário de registro de novos usuários.
    Coleta dados pessoais e permite a escolha do tipo de conta (Cliente ou Motorista) para salvar no banco de dados.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        frame = tk.Frame(self, bg="#103f35", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=400)

        tk.Button(
            frame,
            text="X",
            command=lambda: controlador.mostrar_frame("TelaLoginFrame"),
            bd=0,
            fg="red",
            font=("Arial", 10, "bold"),
        ).place(relx=1.0, rely=0.0, anchor="ne")

        # Campos
        tk.Label(frame, text="Nome:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.15, anchor="w"
        )
        self.nome_ent = tk.Entry(frame, width=28)
        self.nome_ent.place(relx=0.5, rely=0.22, anchor="center")

        tk.Label(frame, text="Email:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.30, anchor="w"
        )
        self.cad_email_ent = tk.Entry(frame, width=28)
        self.cad_email_ent.place(relx=0.5, rely=0.37, anchor="center")

        tk.Label(frame, text="Senha:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.45, anchor="w"
        )
        self.cad_senha_ent = tk.Entry(frame, show="*", width=28)
        self.cad_senha_ent.place(relx=0.5, rely=0.52, anchor="center")

        tk.Label(frame, text="Telefone:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.60, anchor="w"
        )
        self.tel_ent = tk.Entry(frame, width=28)
        self.tel_ent.place(relx=0.5, rely=0.67, anchor="center")

        # Radio Buttons
        self.tipo_usuario_var = tk.StringVar(value="cliente")
        tk.Label(frame, text="Tipo de Conta:", bg="#103f35", fg="white").place(
            relx=0.12, rely=0.75, anchor="w"
        )
        tk.Radiobutton(
            frame,
            text="Cliente",
            variable=self.tipo_usuario_var,
            value="cliente",
            bg="#103f35",
            fg="white",
            selectcolor="#103f35",
            activebackground="#103f35",
        ).place(relx=0.3, rely=0.82, anchor="center")
        tk.Radiobutton(
            frame,
            text="Motorista",
            variable=self.tipo_usuario_var,
            value="motorista",
            bg="#103f35",
            fg="white",
            selectcolor="#103f35",
            activebackground="#103f35",
        ).place(relx=0.7, rely=0.82, anchor="center")

        tk.Button(frame, text="Cadastrar", command=self.enviar_cadastro).place(
            relx=0.5, rely=0.93, anchor="center"
        )

    def enviar_cadastro(self):
        nome = self.nome_ent.get()
        email = self.cad_email_ent.get()
        senha = self.cad_senha_ent.get()
        telefone = self.tel_ent.get()
        tipo = self.tipo_usuario_var.get()

        if nome and email and senha and telefone:
            # INTEGRACAO FLASK: Recebe (Sucesso, Mensagem)
            sucesso, mensagem = self.controlador.cadastrar_usuario_controller(
                nome, email, senha, telefone, tipo
            )

            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.controlador.mostrar_frame("TelaLoginFrame")
            else:
                # Mostra o erro exato vindo do servidor (ex: Senha Fraca)
                messagebox.showerror("Erro no Cadastro", mensagem)
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")
