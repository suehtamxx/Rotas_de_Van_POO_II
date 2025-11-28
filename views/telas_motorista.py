import tkinter as tk
from tkinter import messagebox
from controllers.controler import cadastrar_nova_rota

class TelaAdicionarRotaFrame(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent, bg="#F0F8F5")
        self.controlador = controlador

        frame = tk.Frame(self, bg="#103f35", bd=2, relief="groove")
        frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=550)

        tk.Label(frame, text="Cadastrar Nova Rota", font=("Arial", 18, "bold"), bg="#103f35", fg="white").place(relx=0.5, rely=0.07, anchor="center")
        tk.Button(frame, text="X", command=lambda: controlador.mostrar_frame("TelaPrincipalFrame"), bd=0, fg="red", font=("Arial", 10, "bold")).place(relx=1.0, rely=0.0, anchor="ne")

        form_frame = tk.Frame(frame, bg="#103f35")
        form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400)

        labels = ["Origem:", "Destino:", "Horário (HH:MM):", "Duração:", "Preço:", "Ponto de Embarque:", "Ponto de Desembarque:"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(form_frame, text=text, bg="#103f35", fg="white").grid(row=i, column=0, sticky="w", pady=8)
            ent = tk.Entry(form_frame, width=35)
            ent.grid(row=i, column=1, sticky="w", pady=8)
            self.entries[text] = ent

        tk.Button(frame, text="Cadastrar Rota", command=self.enviar_cadastro_rota, bg="#3A7C63", fg="white").place(relx=0.5, rely=0.9, anchor="center", height=40, width=200)

    def enviar_cadastro_rota(self):
        # Validação básica
        if not self.controlador.usuario_logado:
            messagebox.showerror("Erro", "Você precisa estar logado.")
            return

        dados = {k: v.get() for k, v in self.entries.items()}
        if not all(dados.values()):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        # Chama o controler (que adiciona na lista local IMEDIATAMENTE e manda pro server em background)
        cadastrar_nova_rota(
            dados["Origem:"], dados["Destino:"], dados["Horário (HH:MM):"],
            dados["Duração:"], dados["Preço:"], self.controlador.usuario_logado["nome"],
            dados["Ponto de Embarque:"], dados["Ponto de Desembarque:"]
        )

        messagebox.showinfo("Sucesso", "Solicitação de cadastro enviada!\nA rota aparecerá em breve.")
        
        # Limpa os campos
        for ent in self.entries.values(): ent.delete(0, tk.END)
        
        # Volta para a tela principal
        self.controlador.mostrar_frame("TelaPrincipalFrame")
        # para recarregar os cards das rotas na tela principal
        if hasattr(self.controlador.frame_principal, 'recarregar_cards'):
            self.controlador.frame_principal.recarregar_cards()