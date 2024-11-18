from flask import Flask,request, session, redirect, jsonify
import sqlite3
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

CORS(app)

app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_aqui'
jwt = JWTManager(app)

conn = sqlite3.connect("data_base.db")
conn.execute("CREATE TABLE IF NOT EXISTS turmas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, turno TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS professores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, senha TEXT, id_turma INTEGER, FOREIGN KEY(id_turma) REFERENCES turmas(id))")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.get_json('nome')
        print(data)
        conn = sqlite3.connect("data_base.db")
        dados_p = conn.execute("SELECT * FROM professores")
        dados_a = conn.execute("SELECT * FROM alunos")
        for i in dados_p:
            if data['nome'] == i[1]:
                if data['senha'] == i[2]:
                    access_token = create_access_token(identity=data["nome"])
                    return jsonify(access_token=access_token)
        for i in dados_a:
            if data['nome'] == i[1]:
                if data['senha'] == i[2]:
                    access_token = create_access_token(identity=data["nome"])
                    return jsonify(access_token=access_token)
        
        return jsonify({'ok': 1})

@app.route("/dashboard", methods = ['POST', 'GET'])
@jwt_required()
def dashboard():
    conn = sqlite3.connect("data_base.db")
    if request.method == "POST":
        current_user = get_jwt_identity()
        
        dados = conn.execute(f"SELECT nome FROM professores")
        for i in dados:
            if i[0] == current_user:
                user = 1
                data = conn.execute(f"SELECT * FROM turmas")
                turmas = {}
                for id, i in enumerate(data):
                    turmas[id] = {'id': i[0],'nome': i[1], 'turno': i[2]}
                return jsonify({'user': user, 'turmas': turmas, 'nome': current_user})
        dados = conn.execute(f"SELECT nome FROM alunos")
        for i in dados:
            if i[0] == current_user:
                user = 0
                data = conn.execute(f"SELECT id_turma FROM alunos WHERE nome='{current_user}'")
                id = list(data)[0][0]
                data = conn.execute(f"SELECT * FROM turmas WHERE id='{id}'")
                valor = list(data)[0]
                return jsonify({'user': user, 'turma': {'nome': valor[1], 'turno': valor[2]}, 'nome': current_user})

@app.route("/nova_turma", methods = ["GET", "POST"])
def nova_turma():
    conn = sqlite3.connect("data_base.db")
    if request.method == "POST":
        data = request.get_json('nome')
        conn.execute(f"INSERT INTO turmas (nome, turno) VALUES ('{data['nome']}', '{data['turno']}')")
        conn.commit()
        return jsonify({'ok': 1})

@app.route("/att", methods = ["GET", "POST"])
def edita_apaga():
    conn = sqlite3.connect("data_base.db")
    if request.method == "POST":
        data = request.get_json('id')
        print(data)
        if data['op'] == 0:
            conn.execute(f"UPDATE turmas SET nome='{data['nome']}', turno='{data['turno']}' WHERE id='{data['id']}'")
            conn.commit()
        if data['op'] == 1:
            turma = conn.execute(f"SELECT * FROM alunos WHERE id_turma={data['id']}")
            turma = list(turma)
            print(turma)
            if (len(turma) > 0):
                return jsonify({'ok': 1})
            conn.execute(f"DELETE FROM turmas WHERE id='{data['id']}'")
            conn.commit()
        return jsonify({'ok': 0})

@app.route("/get_turmas", methods = ["GET", "POST"])
def get_turmas():
    conn = sqlite3.connect("data_base.db")
    dados = conn.execute("SELECT * FROM turmas")
    turmas = list(dados)
    if len(turmas) < 0:
        return jsonify({"ok": 0})
    else:
        data = {"ok": 1, "num": len(turmas)}
        turm = {}
        for i in turmas:
            turm[i[0]] = {'id': i[0],'turma': i[1], 'turno': i[2]}
        data["turmas"] = turm
        return jsonify(data)

@app.route("/r_aluno", methods = ["GET", "POST"])
def r_aluno():
    if request.method == "POST":
        conn = sqlite3.connect("data_base.db")
        data = request.get_json("nome")
        print(data)
        dados = conn.execute(f"SELECT nome FROM professores")
        for i in dados:
            if i[0] == data["nome"]:
                return jsonify({'ok': 1})
        dados = conn.execute(f"SELECT nome FROM alunos")
        for i in dados:
            if i[0] == data["nome"]:
                return jsonify({'ok': 1})
        conn.execute(f"INSERT INTO alunos (nome, senha, id_turma) VALUES ('{data['nome']}', '{data['senha']}', '{data['turma']}')")
        conn.commit()
        return jsonify({'ok': 2})

@app.route("/r_professor", methods = ["GET", "POST"])
def r_professor():
    if request.method == "POST":
        conn = sqlite3.connect("data_base.db")
        data = request.get_json('nome')
        print(data)
        dados = conn.execute(f"SELECT nome FROM professores")
        ok = 1
        for i in dados:
            if i[0] == data['nome']:
                ok = 0
        dados = conn.execute(f"SELECT nome FROM alunos")
        for i in dados:
            if i[0] == data['nome']:
                ok = 0
        
        if ok == 1:
            conn.execute(f"INSERT INTO professores (nome, senha) VALUES ('{data['nome']}', '{data['senha']}')")
            conn.commit()

        return jsonify({'ok': ok})