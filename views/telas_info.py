import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from models.rotas import Rota
from controllers.controler import encontrar_rota_por_origem_destino


class TelaPrincipalFrame(tk.Frame):

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.logo_img = tk.PhotoImage(file="views/Logo.png")

        self.cabecalho()
        self.conteudo_principal()

    def cabecalho(self):
        self.header = tk.Frame(self, bg="#FFFFFF", height=50)
        self.header.pack(fill=tk.X)

        logo_lbl = tk.Label(self.header, image=self.logo_img, bg="white")
        logo_lbl.image = self.logo_img
        logo_lbl.grid(row=0, column=0, padx=0)

        frame_btns = tk.Frame(self.header, bg="#ffffff")
        frame_btns.grid(row=0, column=1)

        horarios_btn = tk.Button(
            frame_btns,
            text="Ajuda",
            bg="#ffffff",
            fg="black",
            font=("Arial", 12, "bold"),
            command=self.controlador.abrir_tela_ajuda,
        )
        horarios_btn.pack(side="left", padx=10)

        self.gerenciar_rotas_btn = tk.Button(
            frame_btns,
            text="Cadastrar Rota",
            bg="#ffffff",
            fg="#3A7C63",
            font=("Arial", 12, "bold"),
            command=lambda: self.controlador.mostrar_frame("TelaAdicionarRotaFrame"),
        )

        self.login_frame = tk.Frame(self.header, bg="#FFFFFF")
        self.login_frame.grid(row=0, column=2, padx=10)

        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            bg="#FFFFFF",
            fg="black",
            font="bold",
            command=lambda: self.controlador.mostrar_frame("TelaLoginFrame"),
        )
        self.login_button.pack()

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
            command=self.controlador.fazer_logout,
        )

        self.header.grid_columnconfigure(1, weight=1)

    def conteudo_principal(self):
        f = tk.Frame(self, bg="#103f35")
        f.pack(fill=tk.X, ipady=30)

        title_frame = tk.Label(
            f,
            text="Van Já: sua rota diária e segura\n em Picos-PI e Região",
            bg="#103f35",
            fg="white",
            font=("Arial", 22, "bold"),
        )
        title_frame.pack(side="top", padx=10, pady=15)
        merchan_lbl = tk.Label(
            f,
            text="Passagens diárias! Encontre a rota necessária para você!.",
            bg="#103f35",
            fg="white",
        )
        merchan_lbl.pack(side="top")

        search_frame = tk.Frame(f, bg="#103f35")
        search_frame.pack(side="top", pady=20)
        origem_lbl = tk.Label(search_frame, text="Origem:", bg="#103f35", fg="white")
        origem_lbl.pack(side="left", padx=(0, 5))
        self.origem_ent = tk.Entry(search_frame)
        self.origem_ent.pack(side="left", ipadx=50)
        destino_lbl = tk.Label(search_frame, text="Destino:", bg="#103f35", fg="white")
        destino_lbl.pack(side="left", padx=(10, 5))
        self.destino_ent = tk.Entry(search_frame)
        self.destino_ent.pack(side="left", ipadx=50)
        search_btn = tk.Button(
            search_frame,
            text="Buscar",
            bg="#3A7C63",
            fg="white",
            font=("Helvetica", 10),
            command=self.buscar_rota,
        )
        search_btn.pack(side="left", padx=10)

        outdoor_lbl = tk.Label(
            f,
            text="Vans Confortáveis   Motoristas Treinados    Suporte Rápido",
            bg="#B9D9C6",
            fg="black",
        )
        outdoor_lbl.pack(fill="x", side="top")

        self.container_cards = tk.Frame(self, bg="#F0F8F5")
        self.container_cards.pack(fill="both", expand=True, padx=20, pady=10)

        self.criar_cards_rotas()

    def buscar_rota(self):
        origem = self.origem_ent.get()
        destino = self.destino_ent.get()
        if not origem or not destino:
            messagebox.showerror("Erro", "Preencha os campos de origem e destino.")
            return

        rota_encontrada = encontrar_rota_por_origem_destino(origem, destino)
        if rota_encontrada:
            self.controlador.abrir_tela_detalhes(rota_encontrada)
        else:
            messagebox.showinfo(
                "Busca de Rotas",
                f"Ainda não há rotas disponíveis entre {origem} e {destino}.",
            )

    def recarregar_cards(self):
        self.container_cards.destroy()

        self.container_cards = tk.Frame(self, bg="#F0F8F5")
        self.container_cards.pack(fill="both", expand=True, padx=20, pady=10)

        self.criar_cards_rotas()

    def criar_cards_rotas(self):
        titulo_secao = tk.Label(
            self.container_cards,
            text="Rotas em Destaque",
            font=("Arial", 18, "bold"),
            bg="#F0F8F5",
            fg="#103F35",
        )
        titulo_secao.pack(anchor="w", padx=15, pady=(5, 15))

        cards_frame = tk.Frame(self.container_cards, bg="#F0F8F5")
        cards_frame.pack(fill="x")

        # Limita a 3 cards para não quebrar o layout
        rotas_para_exibir = Rota.lista_de_rotas[:3]

        if not rotas_para_exibir:
            tk.Label(
                cards_frame, text="Nenhuma rota cadastrada no momento.", bg="#F0F8F5"
            ).pack()
            return

        for rota in rotas_para_exibir:
            card = tk.Frame(cards_frame, bg="white", relief="solid", borderwidth=1)
            card.pack(side="left", fill="y", padx=15, pady=5, expand=True)

            origem_destino = f"{rota.origem} → {rota.destino}"
            rota_lbl = tk.Label(
                card, text=origem_destino, font=("Arial", 14, "bold"), bg="white"
            )
            rota_lbl.pack(anchor="w", padx=10, pady=(10, 5))

            bottom_frame = tk.Frame(card, bg="white")
            bottom_frame.pack(fill="x", side="bottom", padx=10, pady=10)

            preco_lbl = tk.Label(
                bottom_frame, text=rota.preco, font=("Arial", 12, "bold"), bg="white"
            )
            preco_lbl.pack(side="left")

            ver_rota_btn = tk.Button(
                bottom_frame,
                text="Ver rota",
                bg="#3A7C63",
                fg="white",
                command=lambda r=rota: self.controlador.abrir_tela_detalhes(r),
            )
            ver_rota_btn.pack(side="right")

    # --- Métodos de atualização do cabeçalho  ---
    def atualizar_interface_login(self, usuario):
        self.login_button.pack_forget()
        primeiro_nome = usuario["nome"].split()[0]
        tipo_usuario = usuario.get("tipo_usuario", "cliente")
        self.welcome_lbl.config(text=f"Olá, {primeiro_nome} ({tipo_usuario})")
        self.welcome_lbl.pack(side="left", padx=5)
        self.logout_button.pack(side="left")

        if tipo_usuario == "motorista":
            self.gerenciar_rotas_btn.pack(side="left", padx=10)

    def atualizar_interface_logout(self):
        self.welcome_lbl.pack_forget()
        self.logout_button.pack_forget()
        self.gerenciar_rotas_btn.pack_forget()
        self.login_button.pack()


# --- Classes de Pop-up---
class TelaAjuda(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajuda / Suporte")
        self.geometry("450x300")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        titulo_lbl = tk.Label(
            self,
            text="Central de Ajuda",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
        )
        titulo_lbl.pack(pady=(20, 10))
        texto_ajuda = (
            "Bem-vindo à Central de Ajuda do Van Já!\n\n"
            "• Para buscar uma rota, utilize os campos 'Origem' e\n 'Destino' na tela principal.\n\n"
            "• Para fazer login ou se cadastrar, clique no botão 'Login'\n no canto superior direito.\n\n"
            "• Em Rotas em Destaque, clique em Ver Rota para mais detalhes sobre aquela rota"
        )
        ajuda_lbl = tk.Label(
            self,
            text=texto_ajuda,
            justify="left",
            wraplength=400,
            bg="#f0f0f0",
        )
        ajuda_lbl.pack(pady=5, padx=20)
        self.transient(parent)
        self.grab_set()


class TelaDetalhes(tk.Toplevel):
    def __init__(self, parent, rota):
        super().__init__(parent)
        self.title(f"Detalhes da Rota: {rota.origem} → {rota.destino}")
        self.geometry("400x300")
        self.configure(bg="#F0F8F5")
        frame = tk.Frame(self, bg="#F0F8F5")
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        tk.Label(
            frame, text="Motorista:", font=("Arial", 11, "bold"), bg="#F0F8F5"
        ).grid(row=0, column=0, sticky="w")
        tk.Label(frame, text=rota.motorista, font=("Arial", 11), bg="#F0F8F5").grid(
            row=0, column=1, sticky="w", padx=5
        )
        tk.Label(frame, text="Preço:", font=("Arial", 11, "bold"), bg="#F0F8F5").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )
        tk.Label(frame, text=rota.preco, font=("Arial", 11), bg="#F0F8F5").grid(
            row=1, column=1, sticky="w", padx=5, pady=(10, 0)
        )
        tk.Label(
            frame, text="Embarque:", font=("Arial", 11, "bold"), bg="#F0F8F5"
        ).grid(row=2, column=0, sticky="w", pady=(10, 0))
        tk.Label(
            frame, text=rota.ponto_embarque, font=("Arial", 11), bg="#F0F8F5"
        ).grid(row=2, column=1, sticky="w", padx=5, pady=(10, 0))
        tk.Label(
            frame, text="Desembarque:", font=("Arial", 11, "bold"), bg="#F0F8F5"
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))
        tk.Label(
            frame, text=rota.ponto_desembarque, font=("Arial", 11), bg="#F0F8F5"
        ).grid(row=3, column=1, sticky="w", padx=5, pady=(10, 0))
        self.transient(parent)
        self.grab_set()
