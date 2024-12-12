from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tasks = []

conn = sqlite3.connect("data_base.db")
conn.execute("CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)")

dados = conn.execute("SELECT * FROM tarefas")

dados = list(dados)

for i in dados:
    tasks.append(i[1])

print(tasks)

@app.route('/api/tarefas/busca', methods=['GET'])
def busca():
    return jsonify({"tarefas": tasks}), 201


@app.route('/api/tarefas', methods=['POST'])
def add_task():
    data = request.json
    tasks.append(data['tarefa'])
    conn = sqlite3.connect("data_base.db")
    conn.execute(f"INSERT INTO tarefas (nome) VALUES ('{data['tarefa']}')")
    conn.commit()
    return jsonify({"message": "Tarefa adicionada!"}), 201

@app.route('/api/tarefas/<tarefa>', methods=['DELETE'])
def delete_task(tarefa):
    if tarefa in tasks:
        tasks.remove(tarefa)
        conn = sqlite3.connect("data_base.db")
        conn.execute(f"DELETE FROM tarefas WHERE nome='{tarefa}'")
        conn.commit()
        return jsonify({"message": "Tarefa removida!"}), 200
    return jsonify({"error": "Tarefa não encontrada."}), 404

if __name__ == '__main__':
    app.run(debug=True)
