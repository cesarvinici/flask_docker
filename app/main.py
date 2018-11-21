from flask import Flask, request, render_template, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = "3123ui123hiu12h3iuh123iuh"

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, id, usuario, senha):
        self.id  = id
        self.usuario = usuario
        self.senha = senha

jogo1 = Jogo('Super Mario', 'Aventura', 'SNES')
jogo2 = Jogo('Pokemon GO', 'RPG', 'Disp. Moveis')
jogo3 = Jogo('GoW4', 'Ação', 'PS4')
lista = [jogo1, jogo2, jogo3]

usuario1 = Usuario(1, 'root', '1234')
usuario2 = Usuario(2, 'admin', '321')
usuarios = {usuario1.usuario: usuario1, usuario2.usuario: usuario2}

# ROTAS DO FLASK
@app.route('/')
def index():
    if(usuarioLogado()):
        flash("Necessário realizar login")
        # url for chama o metodo ao invés do endereco
        return redirect(url_for('login'))
    return render_template("lista.html", titulo = "Jogos", jogos = lista) 
   
    
@app.route('/novo')
def create():
    if(usuarioLogado()):
        flash("Necessário realizar login")
        return redirect(url_for('login', prox=url_for('create')))
    
    return render_template('novo.html', titulo="Novo Jogo")


# necessário informar qual metodo http irá receber
@app.route('/criar', methods=["POST",])
def store():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima_pag = request.args.get('prox')
    return render_template('login.html', titulo='Faça seu Login', prox=proxima_pag)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = request.form['usuario']
    senha = request.form['senha']

    if usuario in usuarios:
        if usuarios[usuario].senha == senha:
            session['usuario_logado'] = usuario
            flash(usuario + ' Logado com sucesso!')
            prox = request.form['prox_pag']
            return redirect(prox)

    flash('Dados incorretos, tente novamente.')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Logout efetuado com sucesso.')
    return redirect(url_for('login'))

#METODOS EXTERNO
def usuarioLogado():
    return 'usuario_logado' not in session or session['usuario_logado'] == None


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
