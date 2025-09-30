import tkinter as tk
from models.rotas import Rota
from tkinter import messagebox
import sys
import os
# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def cabeçalho(root):
		header = tk.Frame(root, bg="#FFFFFF", height=50)
		header.pack(fill=tk.X)
		#login
		login_button = tk.Button(header, text='Login')
		login_button.pack(pady=10, side=tk.RIGHT, padx=10)
		login_button.config(border=2)
		logo = tk.Label(header,text='Van Já', bg="#FFFFFF", fg="black", font=("Arial", 20, "bold"))
		logo.pack(pady=5, side=tk.LEFT, padx=30)
		return header
#mostrar detalhes da rota
def ver_detalhes(routes_listbox):
		
		selecionado = routes_listbox.curselection()
		if selecionado:
			rota = Rota.rotas[selecionado[0]]
			detalhes = f'Paradas: {','.join(rota.paradas)}\nHorário: {rota.horario}'
			tk.messagebox.showinfo('Detalhes da Rota', detalhes)

def main():
	
	root = tk.Tk()
	root.title('Monitoramento de Rotas de Van')
	root.geometry('800x500')
	f = tk.Frame(root, height=350, bg="#1E6B2F")
	cabeçalho(root)
	f.pack(fill=tk.X)

	#titulo
	title_label = tk.Label(root, text='Van Já: Sua Rota Diária e Segura', font=('Arial',18,'bold'))
	title_label.pack(pady=10)

	#lista de rotas
	
	#botao para ver detalhes
	details_button = tk.Button(root, text='Ver Detalhes', command=ver_detalhes)
	details_button.pack(pady=10)

	root.mainloop()


if __name__ == '__main__':
  Rota("Rota 1", ["Parada A", "Parada B"], "08:00 - 18:00")
  Rota("Rota 2", ["Parada C", "Parada D"], "09:00 - 19:00")
	
  main()