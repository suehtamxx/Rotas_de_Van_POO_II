import tkinter as tk
from tkinter import messagebox
from controllers.controler import cadastrar_nova_rota


class TelaAdicionarRotaFrame(tk.Frame):
    """
    Página (Frame) para motoristas adicionarem novas rotas.
    """

    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#F0F8F5")
        self.controlador = controlador

        frame = tk.Frame(self, bg="#103f35", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=550)

        titulo_lbl = tk.Label(
            frame,
            text="Cadastrar Nova Rota",
            font=("Arial", 18, "bold"),
            bg="#103f35",
            fg="white",
        )
        titulo_lbl.place(relx=0.5, rely=0.07, anchor="center")

        close_btn = tk.Button(
            frame,
            text="X",
            command=lambda: controlador.mostrar_frame("TelaPrincipalFrame"),
            bd=0,
            fg="red",
            font=("Arial", 10, "bold"),
        )
        close_btn.place(relx=1.0, rely=0.0, anchor="ne")

        # --- Campos do Formulário ---
        form_frame = tk.Frame(frame, bg="#103f35")
        form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400)

        labels = [
            "Origem:",
            "Destino:",
            "Horário (HH:MM):",
            "Duração (ex: 90 min):",
            "Preço (R$ 00,00):",
            "Ponto de Embarque:",
            "Ponto de Desembarque:",
        ]

        self.entries = {}  # Dicionário para guardar os campos Entry

        for i, label_text in enumerate(labels):
            lbl = tk.Label(form_frame, text=label_text, bg="#103f35", fg="white")
            lbl.grid(row=i, column=0, sticky="w", padx=5, pady=8)

            ent = tk.Entry(form_frame, width=35)
            ent.grid(row=i, column=1, sticky="w", padx=5, pady=8)
            self.entries[label_text] = ent

        cadastrar_btn = tk.Button(
            frame,
            text="Cadastrar Rota",
            command=self.enviar_cadastro_rota,
            bg="#3A7C63",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        cadastrar_btn.place(relx=0.5, rely=0.9, anchor="center", height=40, width=200)

    def enviar_cadastro_rota(self):
        origem = self.entries["Origem:"].get()
        destino = self.entries["Destino:"].get()
        horario = self.entries["Horário (HH:MM):"].get()
        duracao = self.entries["Duração (ex: 90 min):"].get()
        preco = self.entries["Preço (R$ 00,00):"].get()
        ponto_embarque = self.entries["Ponto de Embarque:"].get()
        ponto_desembarque = self.entries["Ponto de Desembarque:"].get()

        if not self.controlador.usuario_logado:
            messagebox.showerror(
                "Erro", "Você precisa estar logado para cadastrar uma rota."
            )
            return

        motorista_nome = self.controlador.usuario_logado["nome"]

        if not all(
            [
                origem,
                destino,
                horario,
                duracao,
                preco,
                ponto_embarque,
                ponto_desembarque,
            ]
        ):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        sucesso = cadastrar_nova_rota(
            origem,
            destino,
            horario,
            duracao,
            preco,
            motorista_nome,
            ponto_embarque,
            ponto_desembarque,
        )

        if sucesso:
            messagebox.showinfo("Cadastro de Rota", "Rota cadastrada com sucesso!")
            for ent in self.entries.values():
                ent.delete(0, tk.END)
            self.controlador.mostrar_frame("TelaPrincipalFrame")

            self.controlador.frame_principal.recarregar_cards()
        else:
            messagebox.showerror("Erro", "Ocorreu um erro ao cadastrar a rota.")
