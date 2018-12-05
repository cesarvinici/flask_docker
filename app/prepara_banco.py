# -*- coding: utf-8 -*-
from flask import Flask
from flaskext.mysql import MySQL

print('Conectando...')
#conn = MySQL.connect(user='cesar', passwd='password', MYSQL_DATABASE_HOST='lab12.dev.iesde.com.br', MYSQL_DATABASE_PORT=3306)

# Descomente se quiser desfazer o banco...
#conn.cursor().execute("DROP DATABASE `jogoteca`;")
#conn.commit()

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'lab12.dev.iesde.com.br'
app.config['MYSQL_DATABASE_USER'] = 'cesar'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'jogoteca'
mysql.init_app(app)
conn = mysql.connect()


@app.route('/')
def index():
      print("conectando...")
      criar_tabela_jogo = ("CREATE TABLE IF NOT EXISTS `jogo` ("
                  "`id` int(11) NOT NULL AUTO_INCREMENT,"
                  "`nome` varchar(50) COLLATE utf8_bin NOT NULL,"
                  "`categoria` varchar(40) COLLATE utf8_bin NOT NULL,"
                  "`console` varchar(20) NOT NULL,"
                  "PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"
             )
      cria_tabela_usuarios = (
            "CREATE TABLE IF NOT EXISTS `usuario` ("
                  "`id` varchar(8) COLLATE utf8_bin NOT NULL,"
                 " `nome` varchar(20) COLLATE utf8_bin NOT NULL,"
                  " `senha` varchar(8) COLLATE utf8_bin NOT NULL,"
                 "PRIMARY KEY (`id`)"
            ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;"
      )

      conn.cursor().execute(criar_tabela_jogo)
      conn.cursor().execute(cria_tabela_usuarios)

      # inserindo usuarios
      cursor = conn.cursor()
      cursor.executemany(
            'INSERT INTO jogoteca.usuario (id, nome, senha) VALUES (%s, %s, %s)',
            [
                  ('luan', 'Luan Marques', 'flask'),
                  ('nico', 'Nico', '7a1'),
                  ('danilo', 'Danilo', 'vegas')
            ])

      cursor.execute('select * from jogoteca.usuario')
      print(' -------------  Usuarios:  -------------')
      for user in cursor.fetchall():
            print(user[1])

      # inserindo jogos
      cursor.executemany(
            'INSERT INTO jogoteca.jogo (nome, categoria, console) VALUES (%s, %s, %s)',
            [
                  ('God of War 4', 'Ação', 'PS4'),
                  ('NBA 2k18', 'Esporte', 'Xbox One'),
                  ('Rayman Legends', 'Indie', 'PS4'),
                  ('Super Mario RPG', 'RPG', 'SNES'),
                  ('Super Mario Kart', 'Corrida', 'SNES'),
                  ('Fire Emblem Echoes', 'Estratégia', '3DS'),
            ])

      cursor.execute('select * from jogoteca.jogo')
      print(' -------------  Jogos:  -------------')
      for jogo in cursor.fetchall():
            print(jogo[1])

      # commitando senão nada tem efeito
      conn.commit()
      cursor.close()

if __name__ == '__main__':
      app.run(host="0.0.0.0", debug=True)