import sqlite3
import xml.etree.ElementTree as ET

conexao = sqlite3.connect('musicas3.sqlite')

jarvees = conexao.cursor()

jarvees.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);

CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);''')

def verificar(dados, chave):
    encontrou = False
    for child in dados:
        if encontrou: return child.text
        if child.tag == 'key' and child.text == chave:
            encontrou = True
    return None


while True:
    arqnome = input('Enter file name: ')
    if len(arqnome) < 1:
        print('Digite novamente')
    else:
        break

dados = ET.parse(arqnome)
filtrado = dados.findall('dict/dict/dict')
print('Dict count:', len(filtrado))

for entrada in filtrado:
    if(verificar(entrada, 'Track ID') is None): continue

    name = verificar(entrada, 'Name')
    artist = verificar(entrada, 'Artist')
    album = verificar(entrada, 'Album')
    genre = verificar(entrada, 'Genre')
    count = verificar(entrada, 'Play Count')
    rating = verificar(entrada, 'Rating')
    length = verificar(entrada, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    print(name, artist, album, genre, count, rating, length)

    jarvees.execute('INSERT OR IGNORE INTO Artist(name) VALUES (?)', (artist, ))
    jarvees.execute('SELECT id FROM Artist WHERE name = ?', (artist, ))
    artist_id = jarvees.fetchone()[0]

    jarvees.execute('INSERT OR IGNORE INTO Genre(name) VALUES(?)', (genre, ))
    jarvees.execute('SELECT id FROM Genre WHERE name = ?', (genre, ))
    genre_id = jarvees.fetchone()[0]

    jarvees.execute('''INSERT OR IGNORE INTO Album(title, artist_id) VALUES(?, ?)''', (album, artist_id))
    jarvees.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = jarvees.fetchone()[0]

    jarvees.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        (name, album_id, genre_id, length, rating, count))

    conexao.commit()

