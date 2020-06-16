import urllib.request, urllib.parse, urllib.error
import sqlite3
import json
import time
import ssl

# Key da API Geocode, do google
api_key = 'AIzaSyAwf6DNCxyJN-0NsaF5iiiCxhvtET7Iupg'

#Link da api
serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

#Conexão e cursor
conexao = sqlite3.connect('dadosMapa.sqlite')
jarvis = conexao.cursor()


jarvis.execute('CREATE TABLE IF NOT EXISTS Locations(endereço TEXT, geodata TEXT)''')

# ignorar os erros de certificado
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


arquivo = open('locais.data')
contador = 0

for linha in arquivo:
    if contador > 200:
        print('200 locais coletados, restarte para coletar mais.')
        break

    endereço = linha.strip()
    print('-='*20)
    jarvis.execute('SELECT geodata FROM Locations WHERE endereço=? ', (memoryview(endereço.encode()), ))

    # mostrando a linha JÁ adicionada
    try:
        dados = jarvis.fetchone()[0]
        print('Encontrado no banco de dados ', endereço)
        continue
    except:
        pass

    parametros = dict()
    parametros['endereço'] = endereço
    parametros['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parametros)

    print('Coletando', url)
    uh = urllib.request.urlopen( url, context=ctx)
    dados = uh.read().decode()
    print('Retrieved', len(dados), 'characters', dados[:].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(dados)
    except:
        print(dados)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('=== Failure To Retrieve ===')
        print(dados)
        break

    jarvis.execute('''INSERT INTO Locations (address, geodata
        VALUES (?, ?)''', (memoryview(endereço.encode()), memoryview(dados.encode())))

    jarvis.commit()
    if count % 10 == 0:
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")




