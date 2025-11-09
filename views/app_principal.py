import tkinter as tk
from tkinter import messagebox
from models.rotas import Rota

# Importa os FRAMES (páginas)
from .telas_usuario import TelaLoginFrame, TelaCadastroFrame
from .telas_info import TelaPrincipalFrame, TelaAjuda, TelaDetalhes
from .telas_motorista import TelaAdicionarRotaFrame
from controllers.controler import validar_login

"""classe 'VanJaApp': controlador central da interface.
Gerencia e exibe todas as outras páginas (Frames)."""


class VanJaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Van Já - Monitoramento de Rotas")
        self.root.geometry("800x600")
        self.usuario_logado = None

        # Cria o container que conterá todas as páginas (Frame)
        container = tk.Frame(root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (
            TelaPrincipalFrame,
            TelaLoginFrame,
            TelaCadastroFrame,
            TelaAdicionarRotaFrame,
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.frame_principal = self.frames["TelaPrincipalFrame"]

        self.mostrar_frame("TelaPrincipalFrame")

    def mostrar_frame(self, nome_da_classe_str):
        """Traz um frame para a frente (muda de 'página')."""
        frame = self.frames[nome_da_classe_str]
        frame.tkraise()

    def tentar_login(self, email, senha):
        usuario = validar_login(email, senha)
        if usuario:
            self.usuario_logado = usuario
            self.frame_principal.atualizar_interface_login(usuario)
            self.mostrar_frame("TelaPrincipalFrame")
            messagebox.showinfo("Login", "Login Realizado com Sucesso.")
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")

    def fazer_logout(self):
        self.usuario_logado = None
        self.frame_principal.atualizar_interface_logout()
        messagebox.showinfo("Logout", "Você saiu da sua conta.")

    def abrir_tela_ajuda(self):
        TelaAjuda(self.root)

    def abrir_tela_detalhes(self, rota):
        TelaDetalhes(self.root, rota)


# --- PONTO DE ENTRADA DA APLICAÇÃO ---
if __name__ == "__main__":
    root = tk.Tk()
    app = VanJaApp(root)
    root.mainloop()
