import sqlite3
import re

conexao = sqlite3.connect('info.sqlite')
jarvis = conexao.cursor()

jarvis.execute('DROP TABLE IF EXISTS Contagem')

jarvis.execute('CREATE TABLE Contagem (organização TEXT, contado INTEGER)')


while True:
    arqnome = input('Digite o nome do arquivo para extrair os dados: ')
    if(len(arqnome) < 1):
        print('Tente novamente!!!')
    else:
        arquivo = open(arqnome)
        break

for linha in arquivo:
    if not re.findall('^From: ', linha): continue
    pedaços = linha.split()
    pedaços = re.findall('@.+\S', pedaços[1])
    endereço = ''.join(pedaços)
    jarvis.execute('SELECT contado FROM Contagem WHERE organização = ?', (endereço,))
    row = jarvis.fetchone()
    if row is None:
        jarvis.execute('''INSERT INTO Contagem (organização, contado) VALUES (?, 1)''', (endereço, ))
    else:
        jarvis.execute('''UPDATE Contagem SET contado = contado + 1 WHERE organização =?''', (endereço,))
    conexao.commit()

    #print(linha)
jarvis.close()
print('Acabei')