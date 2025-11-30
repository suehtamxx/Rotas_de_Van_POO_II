import tkinter as tk
from tkinter import messagebox
from controllers.controler import cadastrar_nova_rota


class TelaAdicionarRotaFrame(tk.Frame):
    """
    Tela exclusiva para motoristas logados.
    Gerencia o cadastro de novas rotas, permitindo a inserção dinâmica de múltiplas paradas e a seleção dos dias da semana disponíveis.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#F0F8F5")
        self.controlador = controlador

        # Frame Principal (Altura aumentada para 700 para caber os novos campos)
        frame = tk.Frame(self, bg="#103f35", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)

        # Título
        tk.Label(
            frame,
            text="Cadastrar Nova Rota",
            font=("Arial", 18, "bold"),
            bg="#103f35",
            fg="white",
        ).place(relx=0.5, rely=0.05, anchor="center")
        tk.Button(
            frame,
            text="X",
            command=lambda: controlador.mostrar_frame("TelaPrincipalFrame"),
            bd=0,
            fg="red",
            font=("Arial", 10, "bold"),
        ).place(relx=1.0, rely=0.0, anchor="ne")

        # Container para o formulário
        self.form_frame = tk.Frame(frame, bg="#103f35")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=460)

        # --- Campos Fixos ---
        self.labels_fixos = [
            "Origem:",
            "Destino:",
            "Horário (HH:MM):",
            "Duração:",
            "Preço:",
            "Ponto de Embarque:",
            "Ponto de Desembarque:",
        ]
        self.entries = {}

        self.linha_atual = 0
        for text in self.labels_fixos:
            tk.Label(self.form_frame, text=text, bg="#103f35", fg="white").grid(
                row=self.linha_atual, column=0, sticky="w", pady=5
            )
            ent = tk.Entry(self.form_frame, width=35)
            ent.grid(row=self.linha_atual, column=1, sticky="w", pady=5)
            self.entries[text] = ent
            self.linha_atual += 1

        # --- SELEÇÃO DE DIAS (NOVO) ---
        tk.Label(
            self.form_frame,
            text="Dias Disponíveis:",
            bg="#103f35",
            fg="#bdc3c7",
            font=("Arial", 9, "bold"),
        ).grid(row=self.linha_atual, column=0, sticky="w", pady=(10, 0))
        self.linha_atual += 1

        self.frame_dias = tk.Frame(self.form_frame, bg="#103f35")
        self.frame_dias.grid(
            row=self.linha_atual, column=0, columnspan=2, sticky="w", pady=5
        )

        self.dias_vars = {}
        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

        # Cria checkboxes lado a lado
        col_dia = 0
        for dia in dias_semana:
            var = tk.IntVar()
            chk = tk.Checkbutton(
                self.frame_dias,
                text=dia,
                variable=var,
                bg="#103f35",
                fg="white",
                selectcolor="#3A7C63",
                activebackground="#103f35",
            )
            chk.grid(row=0, column=col_dia, sticky="w")
            self.dias_vars[dia] = var
            col_dia += 1

        self.linha_atual += 1

        # --- Área de Paradas Dinâmicas ---
        # Rótulo e Botão na mesma linha
        tk.Label(
            self.form_frame,
            text="Paradas Intermediárias:",
            bg="#103f35",
            fg="#bdc3c7",
            font=("Arial", 9, "bold"),
        ).grid(row=self.linha_atual, column=0, sticky="w", pady=(15, 5))

        btn_add = tk.Button(
            self.form_frame,
            text="+ Adicionar",
            command=self.adicionar_campo_parada,
            bg="#5dade2",
            fg="white",
            font=("Arial", 8, "bold"),
            bd=0,
            cursor="hand2",
        )
        btn_add.grid(row=self.linha_atual, column=1, sticky="w", pady=(15, 5), padx=5)
        self.linha_atual += 1

        # Container EXCLUSIVO para as paradas (usa pack dentro para crescer pra baixo)
        self.frame_paradas = tk.Frame(self.form_frame, bg="#103f35")
        self.frame_paradas.grid(
            row=self.linha_atual, column=0, columnspan=2, sticky="we"
        )

        self.lista_entries_paradas = (
            []
        )  # Lista para guardar as referências dos campos criados

        # Botão Cadastrar (no fundo)
        tk.Button(
            frame,
            text="Cadastrar Rota",
            command=self.enviar_cadastro_rota,
            bg="#3A7C63",
            fg="white",
        ).place(relx=0.5, rely=0.96, anchor="center", height=35, width=200)

    def adicionar_campo_parada(self):
        # Limite de segurança visual
        if len(self.lista_entries_paradas) >= 6:
            messagebox.showinfo(
                "Limite", "Você atingiu o limite de visualização de paradas."
            )
            return

        # Cria um sub-frame para a linha (para garantir que fiquem um abaixo do outro)
        row_frame = tk.Frame(self.frame_paradas, bg="#103f35")
        row_frame.pack(
            side="top", fill="x", pady=2
        )  # <--- PACK garante empilhamento vertical

        numero_parada = len(self.lista_entries_paradas) + 1

        # Label (ex: 1ª:)
        lbl = tk.Label(
            row_frame,
            text=f"{numero_parada}ª:",
            bg="#103f35",
            fg="white",
            font=("Arial", 9),
        )
        lbl.pack(
            side="left", padx=(80, 5)
        )  # Ajuste o padx (80) para alinhar com os labels de cima

        # Campo de entrada
        ent = tk.Entry(row_frame, width=28)
        ent.pack(side="left")

        self.lista_entries_paradas.append(ent)

    def enviar_cadastro_rota(self):
        # 1. Validação de Login
        if not self.controlador.usuario_logado:
            messagebox.showerror("Erro", "Você precisa estar logado.")
            return

        # 2. Pegar dados dos campos fixos
        dados = {k: v.get() for k, v in self.entries.items()}

        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        # 3. Processar Dias Selecionados
        dias_selecionados = [
            dia for dia, var in self.dias_vars.items() if var.get() == 1
        ]
        string_dias = ",".join(dias_selecionados)  # Ex: "Seg,Qua,Sex"

        if not string_dias:
            messagebox.showerror("Erro", "Selecione pelo menos um dia da semana!")
            return

        # 4. Processar as Paradas Dinâmicas
        # Pega o texto de cada campo e junta com setas
        paradas_textos = [
            e.get().strip() for e in self.lista_entries_paradas if e.get().strip()
        ]
        string_paradas = " ➔ ".join(paradas_textos)

        # 5. Enviar para o controlador
        try:
            cadastrar_nova_rota(
                dados["Origem:"],
                dados["Destino:"],
                dados["Horário (HH:MM):"],
                dados["Duração:"],
                dados["Preço:"],
                self.controlador.usuario_logado["nome"],
                dados["Ponto de Embarque:"],
                dados["Ponto de Desembarque:"],
                string_paradas,
                string_dias,
            )

            messagebox.showinfo(
                "Sucesso",
                "Solicitação de cadastro enviada!\nA rota aparecerá em breve.",
            )

            # Limpar campos
            for ent in self.entries.values():
                ent.delete(0, tk.END)

            # Limpar checkboxes
            for var in self.dias_vars.values():
                var.set(0)

            # Limpar campos de paradas
            for widget in self.frame_paradas.winfo_children():
                widget.destroy()
            self.lista_entries_paradas = []

            self.controlador.mostrar_frame("TelaPrincipalFrame")
            if hasattr(self.controlador.frame_principal, "recarregar_cards"):
                self.controlador.frame_principal.recarregar_cards()

        except TypeError as e:
            # Caso esqueça de atualizar o controler.py, este erro avisa
            print(e)
            messagebox.showerror(
                "Erro Interno",
                "Atualize o arquivo 'controllers/controler.py' para aceitar os campos 'paradas' e 'dias'.",
            )


class TelaRotasDisponiveis(tk.Toplevel):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.title("Rotas Disponíveis - Filtro por Dia")
        self.geometry("900x600")
        self.configure(bg="#F0F8F5")

        # --- Cabeçalho ---
        top_frame = tk.Frame(self, bg="#103f35", height=60)
        top_frame.pack(fill="x")
        tk.Label(
            top_frame,
            text="Selecione o dia da sua viagem",
            font=("Arial", 16, "bold"),
            bg="#103f35",
            fg="white",
        ).pack(pady=15)

        # --- Área de Filtros (Botões dos Dias) ---
        filter_frame = tk.Frame(self, bg="#F0F8F5")
        filter_frame.pack(fill="x", pady=20)

        dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]

        # Botão "Todos"
        tk.Button(
            filter_frame,
            text="Todos",
            width=10,
            bg="#34495e",
            fg="white",
            command=lambda: self.filtrar_rotas("Todos"),
        ).pack(side="left", padx=10, expand=True)

        # Botões dos Dias
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

        # --- Área dos Cards (Resultados) ---
        self.container_resultados = tk.Frame(self, bg="#F0F8F5")
        self.container_resultados.pack(fill="both", expand=True, padx=20)

        # Scrollbar para os resultados (Caso tenha muitas rotas)
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

        # Carrega todas inicialmente
        self.filtrar_rotas("Todos")

    def filtrar_rotas(self, dia_escolhido):
        # Limpa resultados anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Importa aqui para evitar ciclo
        from models.rotas import Rota

        contador = 0
        for rota in Rota.lista_de_rotas:
            # Lógica de Filtro:
            # Se for "Todos" OU se o dia escolhido estiver dentro da string de dias da rota
            # Ex: "Seg" está dentro de "Seg,Qua,Sex" -> True
            dias_da_rota = getattr(
                rota, "dias_disponiveis", ""
            )  # Garante que não quebra se for None

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
        # Card Visual
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=5, padx=5)

        # Conteúdo do Card
        info = (
            f"{rota.origem} ➔ {rota.destino} | 🕒 {rota.horario} | 💰 R$ {rota.preco}"
        )
        tk.Label(card, text=info, font=("Arial", 11, "bold"), bg="white").pack(
            side="left", padx=15, pady=15
        )

        # Mostra os dias no card também
        dias_texto = rota.dias_disponiveis if hasattr(rota, "dias_disponiveis") else ""
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
