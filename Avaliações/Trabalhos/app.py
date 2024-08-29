from flask import Flask,request,render_template, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "nao_Sei"

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./sessoes"

conn = sqlite3.connect("data_base.db")
conn.execute("CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, turno TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS professores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT, id_turma INTEGER, FOREIGN KEY(id_turma) REFERENCES turmas(id))")

chamada = {}

@app.route("/registro", methods = ['POST', 'GET'])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        cargo =  request.form.get("cargo")
        conn = sqlite3.connect("data_base.db")
        conn.execute(f"INSERT INTO usuarios (nome, senha, cargo) VALUES ('{usuario}', '{senha}', '{cargo}')")
        conn.commit()
        dados = conn.execute("SELECT * FROM usuarios")
        for i in dados:
            print(i)
        session["cargo"] = cargo
        session["nome"] =  usuario
        return redirect("/dashboard")
    else:
        return render_template("registro.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        conn = sqlite3.connect("data_base.db")
        dados_p = conn.execute("SELECT * FROM professores")
        dados_a = conn.execute("SELECT * FROM alunos")
        for i in dados_p:
            if usuario == i[1]:
                if senha == i[2]:
                    session["nome"] = usuario
                    session["cargo"] = "professor"
                    return redirect("/dashboard")
        for i in dados_a:
            if usuario == i[1]:
                if senha == i[2]:
                    session["nome"] = usuario
                    session["cargo"] = "aluno"
                    return redirect("/dashboard")
        return render_template('login.html', erro="Usuario ou Senha errados")
    else:
        return render_template('login.html', erro="")

@app.route("/dashboard", methods = ['POST', 'GET'])
def dashboard():
    conn = sqlite3.connect("data_base.db")
    if request.method == "POST":
        if session["cargo"] == "professor":
            nome = request.form.get("nome_turma")
            turno = request.form.get("turno_turma")
            conn.execute(f"INSERT INTO turmas (nome, turno) VALUES ('{nome}', '{turno}')")
            conn.commit()
            dados = conn.execute("SELECT * FROM turmas")
            return render_template('dashboard.html', nome=session["nome"], professor=True, cadastrado=True, turmas=list(dados))
        else:
            turma = request.form.get("turma")
            conn.execute(f"UPDATE usuarios SET id_turma={turma} WHERE nome='{session['nome']}'")
            conn.commit()
            dados = conn.execute("SELECT * FROM usuarios")
            for i in dados:
                print(i)
        return render_template('dashboard.html', nome=session["nome"], professor=False, cadastrado=True)
    else:
        if "nome" in session:
            if session["cargo"] == "professor":
                dados = conn.execute("SELECT * FROM turmas")
                turmas = list(dados)
                return render_template('dashboard.html', nome=session["nome"], professor=True, turmas=turmas)
            else:
                dados = conn.execute(f"SELECT * FROM turmas WHERE id=(SELECT id_turma FROM alunos WHERE nome='{session['nome']}')")
                turma = list(dados)[0]
                return render_template('dashboard.html', nome=session["nome"], professor=False, turma=turma)
        else:
            return "<h1> Voce nao esta logado </h1>"
    
@app.route("/edita_apaga", methods = ["GET", "POST"])
def edita_apaga():
    conn = sqlite3.connect("data_base.db")
    if request.method == "GET":
        turma = conn.execute(f"SELECT * FROM turmas WHERE id = {request.args.get('escolha')}")
        return render_template("edita_apaga.html", turma=list(turma)[0], erro=False)
    if request.method == "POST":
        id = request.form.get("id")
        nome = request.form.get("nome_turma")
        turno = request.form.get("turno")
        opcao = request.form.get("opcao")
        if opcao == "salvar":
            conn.execute(f"UPDATE turmas SET nome='{nome}', turno='{turno}' WHERE id='{id}'")
        if opcao == "deletar":
            dados = conn.execute(f"SELECT * FROM alunos WHERE id_turma='{id}'")
            if len(list(dados)) > 0:
                turma = conn.execute(f"SELECT * FROM turmas WHERE id = {request.args.get('escolha')}")
                return render_template("edita_apaga.html", turma=list(turma)[0], erro=True)
            conn.execute(f"DELETE FROM turmas WHERE id='{id}'")
        conn.commit()
        return redirect("/dashboard")

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/r_professor", methods = ["GET", "POST"])
def registro_p():
    if request.method == "POST":
        conn = sqlite3.connect("data_base.db")
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        dados = conn.execute(f"SELECT nome FROM professores")
        for i in dados:
            if i[0] == nome:
                return render_template("r_professor.html", ja_existe=True)
        dados = conn.execute(f"SELECT nome FROM alunos")
        for i in dados:
            if[0] == nome:
                return render_template("r_professor.html", ja_existe=True)
        conn.execute(f"INSERT INTO professores (nome, senha) VALUES ('{nome}', '{senha}')")
        conn.commit()
        session["nome"] = nome
        session["cargo"] = "professor"
        return redirect("/dashboard")
    else:
        return render_template("r_professor.html", ja_existe=False)

@app.route("/r_aluno", methods = ["GET", "POST"])
def registro_a():
    conn = sqlite3.connect("data_base.db")
    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        escolha = request.form.get("escolha")
        dados = conn.execute(f"SELECT nome FROM professores")
        for i in dados:
            if i[0] == nome:
                return render_template("r_professor.html", ja_existe=True)
        dados = conn.execute(f"SELECT nome FROM alunos")
        for i in dados:
            if[0] == nome:
                return render_template("r_professor.html", ja_existe=True)
        conn.execute(f"INSERT INTO alunos (nome, senha, id_turma) VALUES ('{nome}', '{senha}', '{escolha}')")
        conn.commit()
        session["nome"] = nome
        session["cargo"] = "aluno"
        return redirect("/dashboard")
    else:
        dados = conn.execute("SELECT * FROM turmas")
        turmas = list(dados)
        return render_template("r_aluno.html", turmas=turmas, liberado=len(turmas) > 0)
