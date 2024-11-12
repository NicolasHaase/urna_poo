from tkinter import *
from tkinter import ttk
from Teclado import *

def print_numero(texto, teclado: Teclado):
        retorno = teclado.clicar(texto)
        if retorno is not None:
            print (retorno)
        print(teclado.voto)


janela = Tk()
frame = ttk.Frame(janela, padding=50)
frame.grid()

teclado = Teclado()

for i in range(0, 5):
    for j in range(0, 3):
        if teclado.teclas[i][j]:
            ttk.Button(frame, text=teclado.teclas[i][j], command=lambda texto=teclado.teclas[i][j]: print_numero(texto, teclado)).grid(column=j, row=i)

janela.mainloop()
