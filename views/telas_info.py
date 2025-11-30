import tkinter as tk
from tkinter import messagebox
from models.rotas import Rota
from controllers.controler import encontrar_rotas_por_origem_destino


class TelaPrincipalFrame(tk.Frame):
    """
    Tela inicial (Home) da aplicação.
    Exibe o cabeçalho, a barra de pesquisa principal, os cards de destaque e o acesso aos filtros de rotas.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        try:
            self.logo_img = tk.PhotoImage(file="views/Logo.png")
        except:
            self.logo_img = None
        self.cabecalho()
        self.conteudo_principal()

    def cabecalho(self):
        self.header = tk.Frame(self, bg="#FFFFFF", height=50)
        self.header.pack(fill=tk.X)

        if self.logo_img:
            tk.Label(self.header, image=self.logo_img, bg="white").grid(row=0, column=0)
        else:
            tk.Label(
                self.header,
                text="Van Já",
                font=("Arial", 16, "bold"),
                bg="white",
                fg="#103f35",
            ).grid(row=0, column=0, padx=10)

        frame_btns = tk.Frame(self.header, bg="white")
        frame_btns.grid(row=0, column=1)
        tk.Button(
            frame_btns,
            text="Ajuda",
            bg="white",
            fg="#3A7C63",
            font=("Arial", 12, "bold"),
            command=self.controlador.abrir_tela_ajuda,
        ).pack(side="left", padx=10)

        self.gerenciar_rotas_btn = tk.Button(
            frame_btns,
            text="Cadastrar Rota",
            bg="white",
            fg="#3A7C63",
            font=("Arial", 12, "bold"),
            command=lambda: self.controlador.mostrar_frame("TelaAdicionarRotaFrame"),
        )

        self.login_frame = tk.Frame(self.header, bg="white")
        self.login_frame.grid(row=0, column=2, padx=10)

        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            bg="#3A7C63",
            fg="white",
            font=("Arial", 12, "bold"),
            command=lambda: self.controlador.mostrar_frame("TelaLoginFrame"),
        )
        self.login_button.pack()

        self.welcome_lbl = tk.Label(
            self.login_frame,
            text="",
            bg="white",
            fg="#103f35",
            font=("Arial", 10, "bold"),
        )
        self.logout_button = tk.Button(
            self.login_frame,
            text="Sair",
            bg="#FD0000",
            fg="white",
            command=self.controlador.fazer_logout,
        )

        self.header.grid_columnconfigure(1, weight=1)

    def conteudo_principal(self):
        # Frame Verde (Cabeçalho)
        f = tk.Frame(self, bg="#103f35")
        f.pack(fill=tk.X, ipady=30)

        # titulo
        tk.Label(
            f,
            text="Van Já: Vans de Picos-PI e Região!",
            bg="#103f35",
            fg="white",
            font=("Arial", 22, "bold"),
        ).pack(side="top", pady=(30, 5))

        # Botão Ver Rotas com Filtros
        btn_filtros = tk.Button(
            f,
            text="Ver rotas disponíveis",
            bg="#b2dbc0",
            fg="#103f35",
            font=("Arial", 10, "bold"),
            command=lambda: TelaRotasDisponiveis(self, self.controlador),
        )
        btn_filtros.pack(pady=(10, 10))

        # Titulo Busca
        tk.Label(
            f,
            text="Busque sua rota ideal:",
            bg="#103f35",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side="top", pady=(30, 5))

        # Busca
        search_frame = tk.Frame(f, bg="#103f35")
        search_frame.pack(pady=(10, 5))

        tk.Label(search_frame, text="Origem:", bg="#103f35", fg="white").pack(
            side="left"
        )
        self.origem_ent = tk.Entry(search_frame)
        self.origem_ent.pack(side="left", ipadx=50)

        tk.Label(search_frame, text="Destino:", bg="#103f35", fg="white").pack(
            side="left", padx=(10, 0)
        )
        self.destino_ent = tk.Entry(search_frame)
        self.destino_ent.pack(side="left", ipadx=50)

        tk.Button(
            search_frame,
            text="Buscar",
            bg="#3A7C63",
            fg="white",
            command=self.buscar_rota,
        ).pack(side="left", padx=10)

        # Container dos Cards
        self.container_cards = tk.Frame(self, bg="#F0F8F5")
        self.container_cards.pack(fill="both", expand=True, padx=20, pady=10)
        self.criar_cards_rotas()

    def buscar_rota(self):
        origem = self.origem_ent.get()
        destino = self.destino_ent.get()
        if not origem or not destino:
            messagebox.showerror("Erro", "Preencha origem e destino.")
            return

        # Busca TODAS as rotas que batem
        rotas_encontradas = encontrar_rotas_por_origem_destino(origem, destino)

        if rotas_encontradas:
            # Se achou, abre a tela de resultados
            TelaResultadosBusca(
                self, self.controlador, rotas_encontradas, origem, destino
            )
        else:
            messagebox.showinfo(
                "Busca", f"Nenhuma rota encontrada de {origem} para {destino}."
            )

    def recarregar_cards(self):
        self.criar_cards_rotas()

    def criar_cards_rotas(self):
        for widget in self.container_cards.winfo_children():
            widget.destroy()

        tk.Label(
            self.container_cards,
            text="Rotas em Destaque",
            font=("Arial", 18, "bold"),
            bg="#F0F8F5",
        ).pack(anchor="w", pady=10)

        cards_frame = tk.Frame(self.container_cards, bg="#F0F8F5")
        cards_frame.pack(fill="x")

        rotas = Rota.lista_de_rotas[::1][:3]

        if not rotas:
            tk.Label(
                cards_frame, text="Nenhuma rota encontrada ainda.", bg="#F0F8F5"
            ).pack()
            return

        for rota in rotas:
            self.criar_card_individual(cards_frame, rota)

    def criar_card_individual(self, parent, rota):
        card = tk.Frame(parent, bg="white", relief="solid", bd=1)
        card.pack(side="left", fill="y", padx=15, expand=True)

        tk.Label(
            card,
            text=f"{rota.origem} → {rota.destino}",
            font=("Arial", 14, "bold"),
            bg="white",
        ).pack(pady=10)
        tk.Label(card, text=f"R$ {rota.preco} | {rota.horario}", bg="white").pack()

        raw_dias = getattr(rota, "dias_disponiveis", "")
        dias_txt = raw_dias if raw_dias is not None else ""
        if len(dias_txt) > 20:
            dias_txt = dias_txt[:20] + "..."
        tk.Label(
            card, text=f"({dias_txt})", bg="white", fg="gray", font=("Arial", 8)
        ).pack()

        tk.Button(
            card,
            text="Ver Detalhes",
            bg="#3A7C63",
            fg="white",
            command=lambda r=rota: self.controlador.abrir_tela_detalhes(r),
        ).pack(pady=10)

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
    """
    Janela pop-up simples (modal) que exibe instruções de uso e informações de suporte ao usuário.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ajuda")
        self.geometry("400x300")
        self.resizable(False, False)
        tk.Label(
            self, text="Central de Ajuda", font=("Arial", 16, "bold"), bg="#f0f0f0"
        ).pack(pady=(30, 30))
        texto_ajuda = "Bem-vindo à Central de Ajuda do Van Já!..."
        tk.Label(
            self, text=texto_ajuda, justify="left", wraplength=420, bg="#f0f0f0"
        ).pack(pady=5, padx=10)


class TelaResultadosBusca(tk.Toplevel):
    """
    Janela de listagem específica.
    Exibe todas as opções de rotas encontradas que correspondem exatamente à Origem e Destino pesquisados pelo usuário.
    """

    def __init__(self, parent, controlador, lista_rotas, origem, destino):
        super().__init__(parent)
        self.controlador = controlador
        self.title(f"Busca: {origem} -> {destino}")
        self.geometry("800x500")
        self.configure(bg="#F0F8F5")

        # Cabeçalho
        top_frame = tk.Frame(self, bg="#103f35", height=60)
        top_frame.pack(fill="x")
        tk.Label(
            top_frame,
            text=f"Resultados para: {origem} ➔ {destino}",
            font=("Arial", 16, "bold"),
            bg="#103f35",
            fg="white",
        ).pack(pady=15)

        tk.Label(
            top_frame,
            text=f"{len(lista_rotas)} opções encontradas",
            font=("Arial", 10),
            bg="#103f35",
            fg="#bdc3c7",
        ).pack(side="bottom", pady=(0, 10))

        # Área de Scroll
        self.container_resultados = tk.Frame(self, bg="#F0F8F5")
        self.container_resultados.pack(fill="both", expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(
            self.container_resultados, bg="#F0F8F5", highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.container_resultados, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F0F8F5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Popular a lista
        for rota in lista_rotas:
            self.criar_card_resultado(rota)

    def criar_card_resultado(self, rota):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5, padx=5)

        info_principal = f"Motorista: {rota.motorista} | 🕒 Saída: {rota.horario}"
        tk.Label(
            card,
            text=info_principal,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#103f35",
        ).pack(side="left", padx=15, pady=15)

        tk.Label(
            card,
            text=f"💰 R$ {rota.preco}",
            font=("Arial", 11, "bold"),
            fg="green",
            bg="white",
        ).pack(side="left", padx=15)

        raw_dias = getattr(rota, "dias_disponiveis", "")
        dias_texto = raw_dias if raw_dias else "Todos"
        tk.Label(card, text=f"({dias_texto})", fg="gray", bg="white").pack(
            side="left", padx=10
        )

        tk.Button(
            card,
            text="Ver Detalhes",
            bg="#3A7C63",
            fg="white",
            command=lambda: self.controlador.abrir_tela_detalhes(rota),
        ).pack(side="right", padx=15)


class TelaDetalhes(tk.Toplevel):
    """
    Janela de visualização detalhada.
    Apresenta todas as informações de uma rota específica, incluindo motorista, preço, lista de paradas e dias de funcionamento.
    """

    def __init__(self, parent, rota):
        super().__init__(parent)
        self.title(f"Detalhes da Viagem")
        self.geometry("500x500")
        self.configure(bg="#F0F8F5")
        self.resizable(False, True)

        header_frame = tk.Frame(self, bg="#103f35", height=60)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text=f"{rota.origem.upper()}  ➔  {rota.destino.upper()}",
            font=("Arial", 16, "bold"),
            bg="#103f35",
            fg="white",
        ).pack(pady=15)

        container = tk.Frame(self, bg="#F0F8F5")
        container.pack(fill="both", expand=True, padx=20, pady=15)

        info_frame = tk.LabelFrame(
            container,
            text="Informações da Viagem",
            font=("Arial", 10, "bold"),
            bg="#F0F8F5",
            fg="#103f35",
            bd=2,
            relief="groove",
        )
        info_frame.pack(fill="x", pady=(0, 15), ipadx=10, ipady=5)

        tk.Label(
            info_frame, text="Motorista:", font=("Arial", 10, "bold"), bg="#F0F8F5"
        ).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(
            info_frame, text=rota.motorista, font=("Arial", 10), bg="#F0F8F5"
        ).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(
            info_frame, text="Preço:", font=("Arial", 10, "bold"), bg="#F0F8F5"
        ).grid(row=0, column=2, sticky="e", padx=(40, 5))
        tk.Label(
            info_frame,
            text=f"R$ {rota.preco}",
            font=("Arial", 12, "bold"),
            fg="#3A7C63",
            bg="#F0F8F5",
        ).grid(row=0, column=3, sticky="w")

        tk.Label(
            info_frame, text="Saída:", font=("Arial", 10, "bold"), bg="#F0F8F5"
        ).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(
            info_frame,
            text=f"{rota.horario} (Duração: {rota.duracao})",
            font=("Arial", 10),
            bg="#F0F8F5",
        ).grid(row=1, column=1, columnspan=3, sticky="w", padx=5)

        tk.Label(
            info_frame, text="Dias:", font=("Arial", 10, "bold"), bg="#F0F8F5"
        ).grid(row=2, column=0, sticky="w", pady=5)

        raw_dias = getattr(rota, "dias_disponiveis", "")
        dias_str = raw_dias if raw_dias is not None else "Todos"

        tk.Label(
            info_frame, text=dias_str, font=("Arial", 9), bg="#F0F8F5", fg="#e67e22"
        ).grid(row=2, column=1, columnspan=3, sticky="w", padx=5)

        route_frame = tk.LabelFrame(
            container,
            text="Itinerário Completo",
            font=("Arial", 10, "bold"),
            bg="#F0F8F5",
            fg="#103f35",
            bd=2,
            relief="groove",
        )
        route_frame.pack(fill="both", expand=True, ipadx=10, ipady=5)

        tk.Label(
            route_frame,
            text="📍 Embarque:",
            font=("Arial", 10, "bold"),
            fg="green",
            bg="#F0F8F5",
        ).pack(anchor="w", pady=(5, 0))
        tk.Label(
            route_frame,
            text=f"   {rota.ponto_embarque}",
            bg="#F0F8F5",
            font=("Arial", 10),
        ).pack(anchor="w", pady=(0, 5))

        if hasattr(rota, "paradas") and rota.paradas and rota.paradas.strip():
            tk.Label(
                route_frame,
                text="🛑 Paradas Intermediárias:",
                font=("Arial", 10, "bold"),
                fg="#e67e22",
                bg="#F0F8F5",
            ).pack(anchor="w", pady=(5, 2))

            lista_paradas = rota.paradas.split(" ➔ ")

            for parada in lista_paradas:
                frame_p = tk.Frame(route_frame, bg="#F0F8F5")
                frame_p.pack(anchor="w", padx=10)
                tk.Label(
                    frame_p, text="⬇", font=("Arial", 8), fg="gray", bg="#F0F8F5"
                ).pack(side="left")
                tk.Label(frame_p, text=parada, font=("Arial", 10), bg="#F0F8F5").pack(
                    side="left", padx=5
                )

        else:
            tk.Label(
                route_frame,
                text="   (Direto sem paradas)",
                font=("Arial", 9, "italic"),
                fg="gray",
                bg="#F0F8F5",
            ).pack(anchor="w", pady=5)

        tk.Label(
            route_frame,
            text="🏁 Desembarque:",
            font=("Arial", 10, "bold"),
            fg="red",
            bg="#F0F8F5",
        ).pack(anchor="w", pady=(10, 0))
        tk.Label(
            route_frame,
            text=f"   {rota.ponto_desembarque}",
            bg="#F0F8F5",
            font=("Arial", 10),
        ).pack(anchor="w")

        tk.Button(
            self,
            text="Fechar",
            command=self.destroy,
            bg="#3A7C63",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
        ).pack(side="bottom", pady=15)


class TelaRotasDisponiveis(tk.Toplevel):
    """
    Tela de listagem geral com filtros.
    Permite ao usuário visualizar todas as rotas do sistema e filtrá-las dinamicamente por dia da semana.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Rotas Disponíveis - Filtro por Dia")
        self.geometry("900x600")
        self.configure(bg="#F0F8F5")

        top_frame = tk.Frame(self, bg="#103f35", height=60)
        top_frame.pack(fill="x")
        tk.Label(
            top_frame,
            text="Selecione o dia da sua viagem",
            font=("Arial", 16, "bold"),
            bg="#103f35",
            fg="white",
        ).pack(pady=15)

        filter_frame = tk.Frame(self, bg="#F0F8F5")
        filter_frame.pack(fill="x", pady=20)

        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
        tk.Button(
            filter_frame,
            text="Todos",
            width=10,
            bg="#34495e",
            fg="white",
            command=lambda: self.filtrar_rotas("Todos"),
        ).pack(side="left", padx=10, expand=True)

        for dia in dias:
            tk.Button(
                filter_frame,
                text=dia,
                width=8,
                bg="#3A7C63",
                fg="white",
                font=("Arial", 10, "bold"),
                command=lambda d=dia: self.filtrar_rotas(d),
            ).pack(side="left", padx=5, expand=True)

        self.container_resultados = tk.Frame(self, bg="#F0F8F5")
        self.container_resultados.pack(fill="both", expand=True, padx=20)

        self.canvas = tk.Canvas(
            self.container_resultados, bg="#F0F8F5", highlightthickness=0
        )
        self.scrollbar = tk.Scrollbar(
            self.container_resultados, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F0F8F5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.filtrar_rotas("Todos")

    def filtrar_rotas(self, dia_escolhido):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        from models.rotas import Rota

        contador = 0
        for rota in Rota.lista_de_rotas:
            dias_da_rota = getattr(rota, "dias_disponiveis", "")
            if dias_da_rota is None:
                dias_da_rota = ""

            if dia_escolhido == "Todos" or (
                dias_da_rota and dia_escolhido in dias_da_rota
            ):
                self.criar_card_simples(rota)
                contador += 1

        if contador == 0:
            tk.Label(
                self.scrollable_frame,
                text=f"Nenhuma rota encontrada para {dia_escolhido}.",
                bg="#F0F8F5",
                font=("Arial", 12),
            ).pack(pady=20)

    def criar_card_simples(self, rota):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5, padx=5)

        info = (
            f"{rota.origem} ➔ {rota.destino} | 🕒 {rota.horario} | 💰 R$ {rota.preco}"
        )
        tk.Label(card, text=info, font=("Arial", 11, "bold"), bg="white").pack(
            side="left", padx=15, pady=15
        )

        raw_dias = getattr(rota, "dias_disponiveis", "")
        dias_texto = raw_dias if raw_dias is not None else ""

        tk.Label(card, text=f"({dias_texto})", fg="gray", bg="white").pack(
            side="left", padx=5
        )

        tk.Button(
            card,
            text="Ver Detalhes",
            bg="#3A7C63",
            fg="white",
            command=lambda: self.controlador.abrir_tela_detalhes(rota),
        ).pack(side="right", padx=15)
