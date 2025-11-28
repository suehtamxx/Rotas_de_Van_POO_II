import tkinter as tk
from tkinter import messagebox
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

        tk.Label(self.header, image=self.logo_img, bg="white").grid(row=0, column=0)
        
        frame_btns = tk.Frame(self.header, bg="white")
        frame_btns.grid(row=0, column=1)
        tk.Button(frame_btns, text="Ajuda", bg="white", command=self.controlador.abrir_tela_ajuda).pack(side="left", padx=10)
        
        # Botão dinâmico (só aparece pra motorista no login)
        self.gerenciar_rotas_btn = tk.Button(frame_btns, text="Cadastrar Rota", bg="white", fg="#3A7C63", font=("Arial", 12, "bold"), command=lambda: self.controlador.mostrar_frame("TelaAdicionarRotaFrame"))

        self.login_frame = tk.Frame(self.header, bg="white")
        self.login_frame.grid(row=0, column=2, padx=10)

        self.login_button = tk.Button(self.login_frame, text="Login", bg="white", command=lambda: self.controlador.mostrar_frame("TelaLoginFrame"))
        self.login_button.pack()

        self.welcome_lbl = tk.Label(self.login_frame, text="", bg="white", fg="green", font=("Arial", 10, "bold"))
        self.logout_button = tk.Button(self.login_frame, text="Sair", bg="white", fg="red", command=self.controlador.fazer_logout)
        
        self.header.grid_columnconfigure(1, weight=1)

    def conteudo_principal(self):
        f = tk.Frame(self, bg="#103f35")
        f.pack(fill=tk.X, ipady=30)
        tk.Label(f, text="Van Já: Picos-PI e Região", bg="#103f35", fg="white", font=("Arial", 22, "bold")).pack(pady=15)

        # Busca
        search_frame = tk.Frame(f, bg="#103f35")
        search_frame.pack(pady=20)
        tk.Label(search_frame, text="Origem:", bg="#103f35", fg="white").pack(side="left")
        self.origem_ent = tk.Entry(search_frame); self.origem_ent.pack(side="left", ipadx=50)
        tk.Label(search_frame, text="Destino:", bg="#103f35", fg="white").pack(side="left")
        self.destino_ent = tk.Entry(search_frame); self.destino_ent.pack(side="left", ipadx=50)
        tk.Button(search_frame, text="Buscar", bg="#3A7C63", fg="white", command=self.buscar_rota).pack(side="left", padx=10)

        self.container_cards = tk.Frame(self, bg="#F0F8F5")
        self.container_cards.pack(fill="both", expand=True, padx=20, pady=10)
        self.criar_cards_rotas()

    def buscar_rota(self):
        origem = self.origem_ent.get()
        destino = self.destino_ent.get()
        if not origem or not destino:
            messagebox.showerror("Erro", "Preencha origem e destino.")
            return

        # Usa a busca local (já carregada do servidor) ou remota
        rota = encontrar_rota_por_origem_destino(origem, destino)
        if rota:
            self.controlador.abrir_tela_detalhes(rota)
        else:
            messagebox.showinfo("Info", "Nenhuma rota encontrada.")
    def recarregar_cards(self):
        """Chamado pelo controler ou outras telas para atualizar a grid."""
        self.criar_cards_rotas()

    def criar_cards_rotas(self):
        # Limpa cards antigos
        for widget in self.container_cards.winfo_children(): widget.destroy()

        tk.Label(self.container_cards, text="Rotas em Destaque", font=("Arial", 18, "bold"), bg="#F0F8F5").pack(anchor="w", pady=10)
        
        cards_frame = tk.Frame(self.container_cards, bg="#F0F8F5")
        cards_frame.pack(fill="x")

        # Exibe rotas que vieram da API
        rotas = Rota.lista_de_rotas[::1][:3]

        if not rotas:
            tk.Label(cards_frame, text="Nenhuma rota encontrada", bg="#F0F8F5").pack()
            return

        for rota in rotas:
            card = tk.Frame(cards_frame, bg="white", relief="solid", bd=1)
            card.pack(side="left", fill="y", padx=15, expand=True)
            
            tk.Label(card, text=f"{rota.origem} → {rota.destino}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
            tk.Label(card, text=f"R$ {rota.preco} | {rota.horario}", bg="white").pack()
            tk.Button(card, text="Ver Detalhes", bg="#3A7C63", fg="white", command=lambda r=rota: self.controlador.abrir_tela_detalhes(r)).pack(pady=10)

    # Métodos auxiliares de Login/Logout 
    def atualizar_interface_login(self, usuario):
        self.login_button.pack_forget()
        nome = usuario["nome"].split()[0]
        self.welcome_lbl.config(text=f"Olá, {nome} ({usuario['tipo_usuario']})")
        self.welcome_lbl.pack(side="left", padx=5)
        self.logout_button.pack(side="left")
        if usuario.get("tipo_usuario") == "motorista":
            self.gerenciar_rotas_btn.pack(side="left", padx=10)

    def atualizar_interface_logout(self):
        self.welcome_lbl.pack_forget()
        self.logout_button.pack_forget()
        self.gerenciar_rotas_btn.pack_forget()
        self.login_button.pack()
    

class TelaAjuda(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajuda"); self.geometry("400x300")
        self.resizable(False, False)

        tk.Label(self, text="Central de Ajuda", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=(30,30))

        texto_ajuda = (
            "Bem-vindo à Central de Ajuda do Van Já!\n\n"
            "• Para buscar uma rota, utilize os campos 'Origem' e\n 'Destino' na tela principal.\n\n"
            "• Para fazer login ou se cadastrar, clique no botão 'Login'\n no canto superior direito.\n\n"
            "• Em Rotas em Destaque, clique em Ver Rota para detalhes."
        )
        tk.Label(self, text=texto_ajuda, justify="left", wraplength=420, bg="#f0f0f0").pack(pady=5, padx=10)

        self.transient(parent)
        self.grab_set()

class TelaDetalhes(tk.Toplevel):
    def __init__(self, parent, rota):
        super().__init__(parent)
        self.title("Detalhes")
        self.geometry("400x200")
        self.resizable(False,False)
        tk.Label(self, text=f"{rota.origem.upper()} -> {rota.destino.upper()}").pack(pady=15)
        tk.Label(self, text=f"Motorista: {rota.motorista}").pack()
        tk.Label(self, text=f"Horario: {rota.horario}").pack()
        tk.Label(self, text=f"Duracao: {rota.duracao}").pack()
        tk.Label(self, text=f"Preço: R${rota.preco}").pack()
        tk.Label(self, text=f"Ponto de Embarque: {rota.ponto_embarque}").pack()
        tk.Label(self, text=f"Ponto de Desembarque: {rota.ponto_desembarque}").pack()
