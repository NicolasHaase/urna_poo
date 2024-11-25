from Urna import *

# Apenas mostra os votos
with open('votos', 'rb') as arquivo:
    votos:List[int] = pickle.load(arquivo)

print ('Os votos são:')
for voto in votos:
    print (voto)

urna = Urna()
