import tkinter as tk
from tkinter import *
from tkinter import ttk
from Teclado import *
from typing import List
from Pessoas_eleicao import *
from abc import ABC
import pickle


class Info_Urna(ABC):
    candidatos: List[Candidato]

    def __init__(self):
        self.candidatos = []
        self.carregar_candidatos()

    def carregar_candidatos(self):
        with open('candidatos.pkl', 'rb') as arquivo:
            self.candidatos = pickle.load(arquivo)

    def registrar_candidatos(self):
        with open('candidatos.pkl', 'wb') as arquivo:
            pickle.dump(self.candidatos, arquivo)



class Urna(Info_Urna):
    janela: tk.Tk # Janela principal (A urna em si)
    teclado: Teclado # Do arquivo Teclado.py
    voto: StringVar # StringVar é uma forma de modificar textos dentro da janela
    frame: ttk.Frame # Até onde entendi, ttk.Frame é a distância que a borda da tela fica dos botões

    def __init__(self):
        super().__init__()
        self.teclado = Teclado()
        self.janela = Tk()
        self.frame = ttk.Frame(self.janela, padding=0)
        self.frame.grid()
        self.largura = 500
        self.altura = 350

        self.voto = StringVar() # Criação do texto do voto
        self.voto.set('_ _')
    
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
        self.janela.resizable(True, True)
        self.janela.geometry(f'{self.largura}x{self.altura}')

        for i in range (0, 5):
            self.janela.rowconfigure(i, weight=1)
        for i in range (0, 3):
            self.janela.columnconfigure(i, weight=1)

        for i in range(0, 5):
            for j in range(0, 3):
                if self.teclado.teclas[i][j]: # Verifica se não é None, já que o teclado não é um 5x3 perfeito
                    ttk.Button(self.janela, text=self.teclado.teclas[i][j],
                    command=lambda texto=self.teclado.teclas[i][j]:
                    self.add_numero(texto=texto)).grid(column=j, row=i+1, sticky='nsew') #i+1 pra não sobrepor o label
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

urna = Urna()
urna.iniciar_urna()
    
