import tkinter as tk
from tkinter import *
from tkinter import ttk
from Teclado import *
from typing import List
from Pessoas_eleicao import *
from abc import ABC
import pickle


class InfoUrna(ABC):
    candidatos: List[Candidato]
    teclado: Teclado # Do arquivo Teclado.py
    eleitores: List[Eleitor]

    def __init__(self):
        self.teclado = Teclado()
        self.candidatos = []
        self.carregar_candidatos()
        self.eleitores = []
        self.carregar_eleitores()

    def verificar_voto(self):
        for candidato in self.candidatos:
            if self.teclado.voto == str(candidato.numero_eleitoral):
                return True
        return False

    def verificar_titulo(self):
        for eleitor in self.eleitores:
            if self.teclado.voto == str(eleitor.titulo.replace(' ', '')): # .strip() não funciona pois
                # remove apenas os espaços antes e depois da string, mas não no meio
                return True
        return False


    def carregar_candidatos(self):
        with open('candidatos', 'rb') as arquivo:
            self.candidatos = pickle.load(arquivo)

    def registrar_candidatos(self):
        with open('candidatos', 'wb') as arquivo:
            pickle.dump(self.candidatos, arquivo)

    def carregar_eleitores(self):
        with open('eleitores', 'rb') as arquivo:
            self.eleitores = pickle.load(arquivo)

    def registrar_eleitores(self):
        with open('eleitores', 'wb') as arquivo:
            pickle.dump(self.eleitores, arquivo)

    def registrar_voto(self):
        pass


class Urna(InfoUrna):
    def __init__(self):
        super().__init__()
        self.size = '1100x575' # Define o tamanho (largura x altura)

        self.cores = { # Cores usadas na urna e o código HEX
            'FUNDO_TECLADO': '#181B20',
            'FUNDO_URNA': '#D3D3D3',
            'CONFIRMA': '#6F984A',
            'CORRIGE': '#D06738',
            'NUMERO': '#0C0C0C',
            'COR_TELA': '#EEEEEE'
        }
        # Isso é só para ajudar por agora, na versão final, ambos os for eleitor e for candidato serão removidos
        for eleitor in self.eleitores:
            print (eleitor.titulo)

        for candidato in self.candidatos:
            print (candidato.numero_eleitoral)

        self.passo = 'titulo'
        self.iniciar()

    def iniciar(self):
        self.janela = tk.Tk() # Cria a janela, mas não executa ela
        self.janela.geometry(self.size) # Passa a largura e altura da janela
        self.janela.resizable (False, False) # Impede que a janela mude de tamanho
        self.janela.configure(bg=self.cores['FUNDO_URNA'])

        self.iniciar_teclado() # Inicia o teclado com todas as teclas com as cores certas
        self.iniciar_tela() # Inicia a tela com os textos de instrução

        self.janela.mainloop() # Executa a janela

    def iniciar_tela(self):
        estilo = ttk.Style()
        estilo.configure('Tela.TFrame', background=self.cores['COR_TELA'])
        estilo.configure('Tela.TLabel', font=('Arial', 30), foreground='black', background=self.cores['COR_TELA'])

        self.frame_tela = ttk.Frame(self.janela, width=550, height=475, style='Tela.TFrame')
        self.frame_tela.pack(side='left', pady=(50, 50), padx=(50, 50))
        self.frame_tela.pack_propagate(False)

        self.instrucao = StringVar()
        self.instrucao.set('Digite seu título de eleitor')
        self.label_instrucao = ttk.Label(self.frame_tela, textvariable=self.instrucao, style='Tela.TLabel')
        self.label_instrucao.pack(pady=(50, 0))

        self.voto = StringVar()
        self.voto.set('')
        self.label_voto = ttk.Label(self.frame_tela, textvariable=self.voto, style='Tela.TLabel')
        self.label_voto.pack(pady=(50, 0))

    def iniciar_teclado(self):

        estilo = ttk.Style()
        estilo.configure('Teclado.TFrame', background=self.cores['FUNDO_TECLADO'])

        self.frame_fundo_teclado = ttk.Frame(self.janela, width=400, height=475, style='Teclado.TFrame') # Cria o frame do fundo do teclado
        self.frame_fundo_teclado.pack(side='right', pady=(125, 0), padx=(0, 0)) # Manda o frame do fundo do teclado para a direita e deixa um espaço de 100px em cima e 0 em baixo
        self.frame_fundo_teclado.pack_propagate(False)

        # O objetivo de criar um frame para o fundo do teclado e outro para o teclado é que as teclas na urna tem um
        # espaçamento diferente se elas estão na primeira ou última coluna/linha

        self.frame_teclado = ttk.Frame(self.frame_fundo_teclado, width=300, height=600, style='Teclado.TFrame') # Cria o frame do teclado
        self.frame_teclado.pack(pady='50', padx='50') # Deixa uma distância de 50px em todos os lados

        for i in range (0, 5):
            self.frame_teclado.rowconfigure(i, weight=1)
        for i in range (0, 3):
            self.frame_teclado.columnconfigure(i, weight=1)

        estilo = ttk.Style()
        estilo.theme_use('alt')

        estilo.configure('Custom.TFrame', background=self.cores['FUNDO_TECLADO'])

        # Reinicia os fundos após utilizar 'alt'
        self.frame_fundo_teclado.configure(style='Custom.TFrame')
        self.frame_teclado.configure(style='Custom.TFrame')

        confirma = {"bg": self.cores['CONFIRMA'], "fg": "white", "activebackground": self.cores['CONFIRMA'], "activeforeground": "white"}
        branco = {"bg": "white", "fg": "gray", "activebackground": "white", "activeforeground": "gray"}
        corrige = {"bg": self.cores['CORRIGE'], "fg": "white", "activebackground": self.cores['CORRIGE'], "activeforeground": "white"}
        numero = {"bg": self.cores['NUMERO'], "fg": "white", "activebackground": self.cores['NUMERO'], "activeforeground": "white"}

        for i in range(0, 5):
            for j in range(0, 3):
                if self.teclado.teclas[i][j]: # Verifica se não é None, já que o teclado não é um 5x3 perfeito
                    if self.teclado.teclas[i][j] == 'CONFIRMA':
                        estilo_botao = confirma

                    elif self.teclado.teclas[i][j] == 'BRANCO':
                        estilo_botao = branco

                    elif self.teclado.teclas[i][j] == 'CORRIGE':
                        estilo_botao = corrige

                    else:
                        estilo_botao = numero

                    button = tk.Button(
                        self.frame_teclado, # Onde está localizado o botão
                        text=self.teclado.teclas[i][j], # Qual o texto dele
                        command=lambda texto=self.teclado.teclas[i][j]: self.add_numero(texto=texto), # O que será feito quando for pressionado
                        font=('Arial', 10, 'bold'), # Fonte, tamanho, negrito
                        bg=estilo_botao["bg"], # Cor do background
                        fg=estilo_botao["fg"], # Cor do texto
                        activebackground=estilo_botao["activebackground"], # Cor do background quando clica
                        activeforeground=estilo_botao["activeforeground"], # Cor do texto quando clica
                        width=10, # Largura
                        height=10, # Altura
                        relief='raised', # Deixa mais com "cara de botão"
                        bd=7.5 # Tamanho da borda do botão
                    )
                    button.grid(column=j, row=i, sticky='nsew', padx=7, pady=7)

    def atualizar_voto(self):
        self.voto.set(self.teclado.voto)

    def add_numero(self, texto):

        # Impede que o usuário digite algo em quanto "FIM" está na tela
        if self.instrucao.get() == 'FIM':
            return
        retorno = self.teclado.clicar(texto)


        if self.instrucao == 'voto' and super().verificar_voto():
                print('Candidato Verdadeiro')  # Apenas por agora, mostraremos a "foto" do candidato depois

        if retorno is not None:  # Se não retornar nada, significa que o eleitor
            # apertou em algum número ou em 'CORRIGE' ou em 'BRANCO'
            if retorno == 'BRANCO':
                pass  # O voto tem que ser "anulado" ainda

            elif retorno == 'CONFIRMA':
                if self.passo == 'titulo':
                    if super().verificar_titulo():
                        self.instrucao.set('Digite seu voto')
                        self.passo = 'voto' # Por ser elif em baixo, ele não cai em self.passo == 'voto'
                    else:
                        self.instrucao.set('Título não encontrado')

                elif self.passo == 'voto':
                    if super().verificar_voto():
                        self.passo = 'titulo'
                        self.resetar_urna()  # Reseta os parâmetros da urna

                self.teclado.voto = ''
                # Limpa o voto caso seja confirmado, independente se o voto foi válido ou não
        self.atualizar_voto()


    def resetar_urna(self):
        self.instrucao.set('FIM')
        self.teclado.voto = ''
        self.janela.after(5000, self.aux) # 5000 ms = 5s

    def aux(self):
        self.instrucao.set('Digite seu título de eleitor')

urna = Urna()

