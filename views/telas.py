import tkinter as tk
from models.rotas import Rota
from tkinter import messagebox
from PIL import Image, ImageTk

class VanJaApp:
	def __init__(self, root):
		self.root = root
		self.root.title('Monitoramento de Rotas de Van')
		self.root.geometry('800x500')

		self.cabecalho()

		#titulo do frame verder
		self.f = tk.Frame(self.root, bg="#103F35")
		self.f.pack(fill=tk.X, ipady=100)
		self.title_frame = tk.Label(self.f, text='Van Já: Sua Rota Diária e Segura\n Para Picos-PI', bg='#103f35', fg='white',font=('Arial',22,'bold'))
		self.title_frame.pack(side='top', padx=10,pady=15)

		#frase abaixo do titulo
		self.merchan_lbl = tk.Label(self.f,text='Planos mensais ou passagens diárias. Encontre sua rota universitária.',bg='#103f35',fg='white')
		self.merchan_lbl.pack(side='top')

		#barra de pesquisa
		self.search_frame = tk.Frame(self.f,bg='#103f35')
		self.search_frame.pack(side='top')

		self.search_ent = tk.Entry(self.search_frame)
		self.search_ent.pack(ipadx=200,pady=20,side='left')

		self.search_btn = tk.Button(self.search_frame,text='Buscar',bg='#3A7C63',fg='white',font=('Helvetica',10))
		self.search_btn.pack(padx=5,side='left')

		self.outdoor_fr = tk.Frame(self.f)
		self.outdoor_lbl = tk.Label(self.f, text='Vans Confortáveis   Motoristas Treinados    Suporte Rápido',bg='#B9D9C6',fg='black')
		self.outdoor_lbl.pack(fill='x',side='top')
		# Lista de rotas (pode ser expandida depois)
		# self.routes_listbox = tk.Listbox(self.root, width=50, height=10)
		# self.routes_listbox.pack(pady=10)

		# Botão para ver detalhes (exemplo de callback OO)
		self.details_button = tk.Button(self.root, text='Ver Detalhes', command=self.ver_detalhes)
		self.details_button.pack(pady=10)

	def cabecalho(self):
		self.header = tk.Frame(self.root, bg="#FFFFFF", height=50)
		self.header.pack(fill=tk.X)
		# Logo
		self.logo = tk.PhotoImage(file="views/Logo.png")
		self.logo_lbl = tk.Label(self.header, image=self.logo, bg="white")
		self.logo_lbl.image = self.logo
		self.logo_lbl.grid(row=0, column=0, padx=0)

		# Frame de botões
		self.frame_btns = tk.Frame(self.header, bg='#ffffff')
		self.frame_btns.grid(row=0, column=1)

		self.plans_btn = tk.Button(self.frame_btns, text='Planos/Preços', bg='#ffffff', fg='black', font=('Arial', 12, 'bold'))
		self.plans_btn.pack(side='left', padx=10)

		self.routes_btn = tk.Button(self.frame_btns, text='Rotas/Destinos', bg='#ffffff', fg='black', font=('Arial', 12, 'bold'))
		self.routes_btn.pack(side='left', padx=10)

		self.horarios_btn = tk.Button(self.frame_btns, text='Horários', bg='#ffffff', fg='black', font=('Arial', 12, 'bold'))
		self.horarios_btn.pack(side='left', padx=10)

		self.login_button = tk.Button(self.header, text='Login',bg="#FFFFFF",fg='black',font='bold',command=self.tela_login)
		self.login_button.grid(row=0, column=2, padx=5)

		self.header.grid_columnconfigure(1, weight=1)

	def ver_detalhes(self):
		pass
	def tela_login(self):
		self.login = tk.Toplevel()
		self.login.title('Tela de login')
		self.login.geometry('400x600')
		self.frame = tk.Frame(self.login, bg='#103f35', bd=2, relief='groove')
		self.frame.place(relx=0.5, rely=0.5, anchor='center', width=300, height=350)

		self.close_btn = tk.Button(self.frame, text='X', command=self.login.destroy, bd=0, fg='red', font=('Arial', 10, 'bold'))
		self.close_btn.place(relx=1.0, rely=0.0, anchor='ne')

		self.email_lbl = tk.Label(self.frame, text='Email:', bg='#103f35',fg='white')
		self.email_lbl.place(relx=0.12, rely=0.18, anchor='w')
		self.email_ent = tk.Entry(self.frame, width=28)
		self.email_ent.place(relx=0.5, rely=0.25, anchor='center')

		self.senha_lbl = tk.Label(self.frame, text='Senha:', bg='#103f35',fg='white')
		self.senha_lbl.place(relx=0.12, rely=0.38, anchor='w')
		self.senha_ent = tk.Entry(self.frame, show='*', width=28)
		self.senha_ent.place(relx=0.5, rely=0.45, anchor='center')
		
		self.logar_btn = tk.Button(self.frame,text='Logar', command=self.validar_login)
		self.logar_btn.place(relx=0.5,rely=0.6,anchor='center',height=25)

		#tela de cadastro
		self.cadastro_lbl = tk.Label(self.frame, text='Não é cadastrado ainda? Clique no botão abaixo', bg='#103f35', fg='white', font=('Default',8))
		self.cadastro_lbl.place(relx=0.5, rely=0.80, anchor='center')
		self.cadastrar_btn = tk.Button(self.frame, text='Cadastrar', command=self.tela_cadastro)
		self.cadastrar_btn.place(relx=0.5, rely=0.9, anchor='center',height=20, width=75)
	def validar_login(self):
		from controllers.controler import validar_login
		email = self.email_ent.get()
		senha = self.senha_ent.get()
		if validar_login(email, senha):
			messagebox.showinfo('Login','Login Realizado com Sucesso.')
			self.login.destroy()
		else:
			messagebox.showerror('Erro','Email ou senha incorretos.')

	def tela_cadastro(self):
		self.cadastro = tk.Toplevel()
		self.cadastro.title('Cadastro de Usuário')
		self.cadastro.geometry('400x600')
		frame = tk.Frame(self.cadastro, bg='#103f35', bd=2, relief='groove')
		frame.place(relx=0.5, rely=0.5, anchor='center', width=320, height=350)

		close_btn = tk.Button(frame, text='X', command=self.cadastro.destroy, bd=0, fg='red', font=('Arial', 10, 'bold'))
		close_btn.place(relx=1.0, rely=0.0, anchor='ne')

		nome_lbl = tk.Label(frame, text='Nome:', bg='#103f35', fg='white')
		nome_lbl.place(relx=0.12, rely=0.15, anchor='w')
		self.nome_ent = tk.Entry(frame, width=28)
		self.nome_ent.place(relx=0.5, rely=0.22, anchor='center')

		email_lbl = tk.Label(frame, text='Email:', bg='#103f35', fg='white')
		email_lbl.place(relx=0.12, rely=0.35, anchor='w')
		self.cad_email_ent = tk.Entry(frame, width=28)
		self.cad_email_ent.place(relx=0.5, rely=0.42, anchor='center')

		senha_lbl = tk.Label(frame, text='Senha:', bg='#103f35', fg='white')
		senha_lbl.place(relx=0.12, rely=0.55, anchor='w')
		self.cad_senha_ent = tk.Entry(frame, show='*', width=28)
		self.cad_senha_ent.place(relx=0.5, rely=0.62, anchor='center')

		tel_lbl = tk.Label(frame, text='Telefone:', bg='#103f35', fg='white')
		tel_lbl.place(relx=0.12, rely=0.75, anchor='w')
		self.tel_ent = tk.Entry(frame, width=28)
		self.tel_ent.place(relx=0.5, rely=0.82, anchor='center')

		cadastrar_btn = tk.Button(frame, text='Cadastrar', command=self.cadastrar_usuario)
		cadastrar_btn.place(relx=0.5, rely=0.93, anchor='center')

	def cadastrar_usuario(self):
		from controllers.controler import cadastrar_usuario
		nome = self.nome_ent.get()
		email = self.cad_email_ent.get()
		senha = self.cad_senha_ent.get()
		telefone = self.tel_ent.get()
		if nome and email and senha and telefone:
			sucesso = cadastrar_usuario(nome, email, senha, telefone)
			if sucesso:
				messagebox.showinfo('Cadastro', 'Usuário cadastrado com sucesso!')
				self.cadastro.destroy()
			else:
				messagebox.showerror('Erro', 'Email já cadastrado!')
		else:
			messagebox.showerror('Erro', 'Preencha todos os campos!')
if __name__ == '__main__':
	Rota("Rota 1", ["Parada A", "Parada B"], "08:00 - 18:00")
	Rota("Rota 2", ["Parada C", "Parada D"], "09:00 - 19:00")
	root = tk.Tk()
	app = VanJaApp(root)
	root.mainloop()