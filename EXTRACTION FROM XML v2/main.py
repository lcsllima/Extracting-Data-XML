import xml.etree.ElementTree as ET
import sqlite3

# Conexão com o BD, musicas.sqlite não existe, então sera criada
conexao = sqlite3.connect('musicas3.sqlite')

# criamos nosso cursor, Jarvees é o cursor, conexao é sqlite3.connect().
jarvees = conexao.cursor()

jarvees.executescript('''
DROP TABLE IF EXISTS Artista;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artista(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    nome TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artista_id INTEGER, 
    titulo TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    titulo TEXT UNIQUE,
    album_id INTEGER, 
    tempo INTEGER, avaliação INTEGER, count INTEGER, genero TEXT
);
''')
# Função, que ira verificar os dados do tópico, VERIFICANDO

def verificar(dado, chave):
    encontrou = False
    for child in dado:
        if encontrou: return child.text # Assim que retornar o dado, CHILD.TEXT, ele já finaliza a função!
        if child.tag == 'key' and child.text == chave:
            encontrou = True # Daqui vai para a linha 38
    return None


while True:
    arqnome = input('Enter file name: ')
    if len(arqnome) < 1:
        print('Digite novamente')
    else:
        break

# SEGUE ABAIXO A ESTRUTURA que queremos DO XML

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>

# "obtendo" os dados do xml
dados = ET.parse(arqnome)

# Assim, obtemos apenas as linhas que queremos, no caso as do exemplo a cima.
filtrado = dados.findall('dict/dict/dict')
print('Total de dicionários: ', filtrado)

# VERIFICANDO
for entrada in filtrado:
    if (verificar(entrada, 'Track ID') is None) : continue

    nome = verificar(entrada, 'Name')
    artista = verificar(entrada, 'Artist')
    album = verificar(entrada, 'Album')
    count = verificar(entrada, 'Play Count')
    avaliação = verificar(entrada, 'Rating')
    tempo = verificar(entrada, 'Total Time')
    genero = verificar(entrada, 'Genre')

    if nome is None or artista is None or album is None:
        continue

    print(nome, artista, album, count, avaliação, tempo)

    jarvees.execute('''INSERT OR IGNORE INTO Artista(nome) VALUES (?)''', (artista, ))
    jarvees.execute('SELECT id FROM Artista WHERE nome = ?', (artista, ))
    artista_id = jarvees.fetchone()[0]

    jarvees.execute('''INSERT OR IGNORE INTO Album(titulo, artista_id) VALUES(?, ?)''', (album, artista_id))
    jarvees.execute('SELECT id FROM Album WHERE titulo = ?', (album, ))
    album_id = jarvees.fetchone()[0]

    jarvees.execute('''INSERT OR REPLACE INTO TRACK (titulo, album_id, tempo, avaliação, count, genero) VALUES (?, ?, ?, ?, ?, ?)''',
                    (nome, album_id, tempo, avaliação, count, genero))

    conexao.commit()
