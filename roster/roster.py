import json
import sqlite3

conexao = sqlite3.connect('rosterdb2.sqlite')
jarvis = conexao.cursor()

jarvis.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE MEMBER (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

nomearquivo = input('Ex: roster_data_sample.json --- Digite o nome do arquivo: ')

if len(nomearquivo) < 1:
    nomearquivo = 'roster_data.json'

# esse é o JSON que estamos trabalhando por padrão no roster
# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(nomearquivo).read()
json_data = json.loads(str_data)

for entrada in json_data:

    nome = entrada[0]
    titulo = entrada[1]
    role = entrada[2]
    # if role == 0:
    #     role = 'Student'
    # else:
    #     role = 'Teacher'

    print((nome, titulo, role))

    # Aqui inserimos os dados, se for duplicado, só ignora, para não dar erro.
    jarvis.execute('INSERT OR IGNORE INTO User (name) VALUES(?)', (nome, ))
    # Encontramos o ID do dado já inserido.
    jarvis.execute('SELECT id FROM User WHERE name =?', (nome, ))
    # Se tiver encontrado vários dados iguais, o primeiro ID é o que vai valer, por isso 0.
    user_id = jarvis.fetchone()[0]

    jarvis.execute('INSERT OR IGNORE INTO Course (title) VALUES(?)', (titulo, ))
    jarvis.execute('SELECT ID FROM Course WHERE title=?', (titulo, ))
    title_id = jarvis.fetchone()[0]

    jarvis.execute('INSERT OR IGNORE INTO MEMBER (user_id, course_id, role) VALUES(?, ?, ?)', (user_id, title_id, role))

    conexao.commit()
