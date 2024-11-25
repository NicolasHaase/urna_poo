import tkinter as tk
from tkinter import *
from tkinter import ttk
from Teclado import *
from typing import List
from Pessoas_eleicao import *
from abc import ABC
import pygame
import pickle


class InfoUrna(ABC):
    candidatos: List[Candidato]
    teclado: Teclado # Do arquivo Teclado.py
    eleitores: List[Eleitor]
    votos: List[int]

    def __init__(self):
        self.teclado = Teclado()

        # Cria uma lista de candidatos vazia e carrega ela com carregar_candidatos
        self.candidatos = []
        self.carregar_candidatos()

        # Cria uma lista de eleitores vazia e carrega ela com carregar_eleitores
        self.eleitores = []
        self.carregar_eleitores()

        # Cria uma lista de votos vazia (esses são os votos apenas da sessão atual)
        self.votos = []

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
            self.candidatos = pickle.load(arquivo) # Carrega os candidatos


    # Esse método NÃO é utilizado, é apenas para registrar uma lista nova caso queira testar novos candidatos
    def registrar_candidatos(self):
        with open('candidatos', 'wb') as arquivo:
            pickle.dump(self.candidatos, arquivo) # Manda os candidatos para o arquivo

    def carregar_eleitores(self):
        with open('eleitores', 'rb') as arquivo:
            self.eleitores = pickle.load(arquivo) # Carrega os eleitores

    # Esse método NÃO é utilizado, é apenas para registrar uma lista nova caso queira testar novos eleitores
    def registrar_eleitores(self):
        with open('eleitores', 'wb') as arquivo:
            pickle.dump(self.eleitores, arquivo) # Manda os eleitores para o arquivo


    # Método para registrar os votos, pode receber uma variável booleana "branco" para saber se o voto é branco
    def registrar_voto(self, branco:bool = False):
        if not branco:
            self.votos.append(int(self.teclado.voto)) # se não for voto branco, vai dar um .append no voto do teclado
        else:
            self.votos.append(-1) # Se for voto branco, ele armazena como −1, já que nenhum candidato pode ter o número
            # eleitoral como -1

    # Esse método é utilizado quando o aplicativo é fechado, ele salva os votos da sessão atual
    def salvar_votos(self):
        try: # Tenta abrir o arquivo
            with open('votos', 'rb') as arquivo:
                votos_existentes = pickle.load(arquivo) # Carrega uma lista de votos do arquivo
        except (FileNotFoundError, EOFError): # Se o arquivo não existir, ele cria uma lista vazia
            votos_existentes = []

        votos_existentes += self.votos # Adiciona os votos da sessão atual aos votos existentes

        with open('votos', 'wb') as arquivo:
            pickle.dump(votos_existentes, arquivo) # Salva os votos para dentro do arquivo



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
        self.passo = 'titulo'

        # Isso mostra todos títulos de eleitores "válidos" para a urna
        print('Títulos de eleitores "válidos":')
        for eleitor in self.eleitores:
            print(eleitor.titulo)

        # Isso mostra todos os números eleitorais "válidos" para a urna
        print('Números Eleitorais "válidos":')
        for candidato in self.candidatos:
            print(candidato.numero_eleitoral)

        pygame.mixer.init()
        self.iniciar()

    def iniciar(self):
        self.janela = tk.Tk() # Cria a janela, mas não executa ela
        self.janela.title('Urna Eletrônica') # Muda o título da janela
        self.janela.geometry(self.size) # Passa a largura e altura da janela
        self.janela.resizable (False, False) # Impede que a janela mude de tamanho
        self.janela.configure(bg=self.cores['FUNDO_URNA'])

        self.iniciar_teclado() # Inicia o teclado com todas as teclas com as cores certas
        self.iniciar_tela() # Inicia a tela com os textos de instrução
        self.janela.protocol('WM_DELETE_WINDOW', self.desligar_urna) # Quando X for apertado, ele manda para o método desligar_urna
        self.janela.mainloop() # Executa a janela

    def iniciar_tela(self):
        estilo = ttk.Style() # Cria um objeto
        estilo.configure('Tela.TFrame', background=self.cores['COR_TELA']) # adiciona o estilo Tela.TFrame com o
        # background de da cor correspondente a 'COR_TELA'
        estilo.configure('Tela.TLabel', font=('Arial', 30), foreground='black', background=self.cores['COR_TELA'])
        # adiciona o estilo Tela.TLabel com a fonte, a cor do texto e a cor do fundo da tela

        self.frame_tela = ttk.Frame(self.janela, width=550, height=475, style='Tela.TFrame') # Cria o frame da tela com
        # o estilo Tela.TFrame, criado anteriormente
        self.frame_tela.pack(side='left', pady=(50, 50), padx=(50, 50)) # "Joga" a tela para a esquerda e dá uma distância de 50px em todas as direções
        self.frame_tela.pack_propagate(False)

        self.instrucao = StringVar() # Cria a instrução que o eleitor deverá seguir, ela não é uma string, é uma classe específica
        # do tkinter chamada StringVar
        self.instrucao.set('Digite seu título de eleitor') # .set é para configurar qual será a string de instrução
        self.label_instrucao = ttk.Label(self.frame_tela, textvariable=self.instrucao, style='Tela.TLabel') # Cria o label da instrução
        self.label_instrucao.pack(pady=(50, 0)) # Coloca o label na tela com 50px de distancia em cima

        self.voto = StringVar() # Cria o voto que aparece na tela
        self.voto.set('') # Zera o voto
        self.label_voto = ttk.Label(self.frame_tela, textvariable=self.voto, style='Tela.TLabel') # Cria o label do voto
        self.label_voto.pack(pady=(50, 0)) # Coloca o voto 50px abaixo da label da instrução

    def iniciar_teclado(self):

        estilo = ttk.Style()
        estilo.configure('Teclado.TFrame', background=self.cores['FUNDO_TECLADO']) # Configura um estilo 'Teclado.TFrame' para ter a cor de fundo
        # como a cor do fundo do teclado

        self.frame_fundo_teclado = ttk.Frame(self.janela, width=400, height=475, style='Teclado.TFrame') # Cria o frame do fundo do teclado
        self.frame_fundo_teclado.pack(side='right', pady=(125, 0), padx=(0, 0)) # Manda o frame do fundo do teclado para a direita e deixa um espaço de 100px em cima e 0 em baixo
        self.frame_fundo_teclado.pack_propagate(False)

        # O objetivo de criar um frame para o fundo do teclado e outro para o teclado é que as teclas na urna tem um
        # espaçamento diferente se elas estão na primeira ou última coluna/linha

        self.frame_teclado = ttk.Frame(self.frame_fundo_teclado, width=300, height=600, style='Teclado.TFrame') # Cria o frame do teclado
        self.frame_teclado.pack(pady='50', padx='50') # Deixa uma distância de 50px em todos os lados

        # Isso diz que tudo tem o mesmo peso, então os botões devem ser do mesmo tamanho, independentemente do texto
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

        # Cria um dicionário para cada tipo de tecla
        confirma = {"bg": self.cores['CONFIRMA'], "fg": "white", "activebackground": self.cores['CONFIRMA'], "activeforeground": "white"}
        branco = {"bg": "white", "fg": "gray", "activebackground": "white", "activeforeground": "gray"}
        corrige = {"bg": self.cores['CORRIGE'], "fg": "white", "activebackground": self.cores['CORRIGE'], "activeforeground": "white"}
        numero = {"bg": self.cores['NUMERO'], "fg": "white", "activebackground": self.cores['NUMERO'], "activeforeground": "white"}

        for i in range(0, 5):
            for j in range(0, 3):
                if self.teclado.teclas[i][j]: # Verifica se não é None, já que o teclado não é um 5x3 perfeito
                    if self.teclado.teclas[i][j] == 'CONFIRMA':
                        # Se for confirma, o dicionário de "confirma" será utilizado, e assim por diante
                        estilo_botao = confirma

                    elif self.teclado.teclas[i][j] == 'BRANCO':
                        estilo_botao = branco

                    elif self.teclado.teclas[i][j] == 'CORRIGE':
                        estilo_botao = corrige

                    else: # Esse else é para todos os números de 0 a 9
                        estilo_botao = numero

                    button = tk.Button( # Cria o botão
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
        self.voto.set(self.teclado.voto) # Muda a string de voto que aparece na tela para a string de voto do teclado

    def add_numero(self, texto):

        # Impede que o usuário digite algo em quanto "FIM" está na tela
        if self.instrucao.get() == 'FIM':
            return

        # Esse retorno é importante, já que o método clicar de teclado nem sempre retorna algo
        retorno = self.teclado.clicar(texto)

        if self.instrucao == 'voto' and super().verificar_voto():
                print('Candidato Verdadeiro')  # Apenas por agora, mostraremos a "foto" do candidato depois

        # Verifica se retornou alguma coisa, as únicas vezes que não retorna nada é quando é um dígito (que será apenas adicionado ao voto)
        # ou se foi apertado 'CORRIGE', que apenas limpa a string de voto

        if retorno is not None:  # Se retornar algo, significa que o eleitor
            # apertou ou em BRANCO, ou em CONFIRMA
            if retorno == 'BRANCO':
                som = pygame.mixer.Sound('sons/som_botao.wav')
                som.play()
                if self.passo == 'voto':
                    self.passo = 'titulo'
                    self.registrar_voto(branco=True)
                    print(f'Voto registrado: BRANCO (-1)') # Essa linha é apenas para ajudar com debug
                    self.resetar_urna()

            elif retorno == 'CONFIRMA': # Apenas uma verificação adicional, poderia ser apenas else
                # Se a "instrução" atual for para informar o título
                if self.passo == 'titulo':
                    if super().verificar_titulo(): # Verifica se o título está presente nos eleitores daquela urna
                        som = pygame.mixer.Sound('sons/confirma.wav')
                        som.play()
                        self.instrucao.set('Digite seu voto') # Muda a instrução caso o título seja validado
                        self.passo = 'voto' # Muda a "instrução" para voto
                        # Por ser elif em baixo, ele não cai em self.passo == 'voto'
                    else: # Se o título de eleitor não estiver na lista de eleitores
                        self.instrucao.set('Título não encontrado')

                # Se a "instrução" atual for para votar
                elif self.passo == 'voto':
                    if super().verificar_voto():
                        self.passo = 'titulo' # Muda a instrução para 'titulo', então cai no if de cima e verifica se o título é valido
                        som = pygame.mixer.Sound('sons/confirma.wav')
                        som.play()
                        self.registrar_voto() # Registra o voto em self.votos
                        print (f'Voto registrado: {self.teclado.voto}') # Essa linha é apenas para ajudar com debug
                        self.resetar_urna()  # Reseta os parâmetros da urna
                    else:
                        self.instrucao.set('Candidato não encontrado')

                self.teclado.voto = ''
                # Limpa o voto caso seja confirmado, independente se o voto foi válido ou não
        else:
            som = pygame.mixer.Sound('sons/som_botao.wav')
            som.play()

        self.atualizar_voto()


    def resetar_urna(self):
        self.instrucao.set('FIM')
        self.teclado.voto = ''
        self.janela.after(5000, self.aux) # 5000 ms = 5s
        # O código precisa ser escrito dessa forma porque a janela não "trava" por 5 segundos, ela "agenda" o método para daqui 5 segundos

    # Método auxiliar para mudar a instrução na tela
    def aux(self):
        self.instrucao.set('Digite seu título de eleitor')


    # Esse método salva os votos e fecha a janela
    def desligar_urna(self):
        self.salvar_votos()
        self.janela.quit()


