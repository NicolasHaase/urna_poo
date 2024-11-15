import tkinter as tk
from tkinter import *
from tkinter import ttk
from Teclado import *

class Urna:
    janela: tk.Tk # Janela principal (A urna em si)
    teclado: Teclado # Do arquivo Teclado.py
    voto: StringVar # StringVar é uma forma de modificar textos dentro da janela
    frame: ttk.Frame # Até onde entendi, ttk.Frame é a distância que a borda da tela fica dos botões

    def __init__(self):
        self.teclado = Teclado()
        self.janela = Tk()
        self.frame = ttk.Frame(self.janela, padding=0)
        self.frame.grid()

        self.voto = StringVar() # Criação do texto do voto
        self.voto.set('_ _')
        """self.voto.grid(row=0, column=0, columnspan=3, pady=20) """
    
    def add_numero(self, texto):

        retorno = self.teclado.clicar(texto)
        self.atualizar_voto()

        if retorno is not None: # Se não retornar nada, significa que o eleitor 
            #apertou em algum número ou em 'CORRIGE' ou em 'BRANCO'
            if retorno == 'BRANCO':
                pass # O voto tem que ser "anulado" ainda

            else:
                pass # Aqui é o voto final, é quando clica em 'CONFIRMA'

    def iniciar_teclado(self):

        label_voto = ttk.Label(self.frame, textvariable=self.voto, font=("Arial", 20))
        label_voto.grid(row=0, column=0, columnspan=3, pady=20)

        for i in range(0, 5):
            for j in range(0, 3):
                if self.teclado.teclas[i][j]: # Verifica se não é None, já que o teclado não é um 5x3 perfeito
                    ttk.Button(self.frame, text=self.teclado.teclas[i][j], 
                    command=lambda texto=self.teclado.teclas[i][j]:
                    self.add_numero(texto=texto)).grid(column=j, row=i+1) #i+1 pra não sobrepor o label
                # Esse 'command=[...]' é dizendo que quando o botão for apertado, ele vai para esse método "add_numero"
                #que vai adicionando o número em uma string dos votos
                
    def iniciar_urna(self):
        self.iniciar_teclado()
        self.janela.mainloop()
    
    # Método para atualizar o voto, se for vazio, ele coloca '_ _' Para indicar que um número pode ser digitado
    def atualizar_voto(self):
        if self.teclado.voto == '':
            self.voto.set('_ _')
        else:
            self.voto.set(self.teclado.voto)
        
    
