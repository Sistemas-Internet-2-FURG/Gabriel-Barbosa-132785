<template>
    <h1>Dashboard</h1>
    Bem-vindo {{nome}}
    <br>
    <button @click="off">Desconectar</button>
    <div v-if="user == 1">

            <h1>Cadastrar turma</h1>
            <label>Nome da turma</label>
            <input type="text" required v-model="nome_turma">
            <label>Turno</label>
            <input type="text" required v-model="turno">
            <button @click="nova_turma">Salvar</button>

        <div v-if="ok == 1">
            A turma foi cadastrada com sucesso
        </div>
        <h2>Turmas Cadatradas</h2>
        <div v-if="editar == true">
            <h3>Editar Turma</h3>
            <label>Turma:</label>
            <input type="text" v-model="edita_nome">
            <label>Turno</label>
            <input type="text" v-model="edita_turno">
            <button @click="salvar(0)">Salvar</button>
            <button @click="salvar(1)">Deletar</button>
            <br>
            <br>
        </div>
        <div v-for="(turma, index) in turmas" v-bind:key="index">
            <button @click="edita($event)" name="escolha" :value=turma.id>Nome: {{turma.nome}}, Turno: {{turma.turno}}</button>
            <br>
        </div>
    </div>
    <div v-if="user == 0">
        <br>
        <label>Sua turma é: {{ nome_turma }}, Turno: {{ turno }}</label>
    </div>
  </template>
  
  <script>
  export default {
    name: 'dashboardPage',
    data() {
        return {
            nome: '',
            user: 0,
            nome_turma: '',
            turno: '',
            turmas: {},
            ok: 0,
            editar: false,
            id: null,
            edita_turno: '',
            edita_nome: '',
        }
    },
    methods: {
        off() {
            sessionStorage.removeItem("access_token")
            this.$emit('muda_pagina', 0)
        },
        salvar(op) {
        const token = sessionStorage.getItem("access_token")
        fetch('http://127.0.0.1:5000/att', {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ id: this.id, nome: this.edita_nome, turno: this.edita_turno, op: op})
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            this.carrega_dash()
            this.editar = false
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
        },
      edita(event) {
        this.editar = true
        this.id = event.target.value
        console.log(this.turmas)
        for (let i = 0; i < 20; i++) {
            if (this.turmas[i].id == this.id) {
                this.edita_nome = this.turmas[i].nome
                this.edita_turno = this.turmas[i].turno
                i = 30
            }
        }
        console.log(event.target.value)
      },
      nova_turma() {
        const token = sessionStorage.getItem("access_token")
        fetch('http://127.0.0.1:5000/nova_turma', {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ nome: this.nome_turma, turno: this.turno })
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            if (data.ok == 1) {
                this.ok = 1
            }
            this.carrega_dash()
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
      },
      tela_cadastro(event) {
          event.preventDefault();
          this.$emit('muda_pagina', 2);
      },
      carrega_dash() {
        const token = sessionStorage.getItem("access_token")
        console.log(token)
        fetch('http://127.0.0.1:5000/dashboard', {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ nome: '' })
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            if (data.user == 0) {
                this.user = data.user
                this.nome_turma = data.turma.nome
                this.turno = data.turma.turno
                this.nome = data.nome
            } else {
                this.user = 1
                this.nome = data.nome
                this.turmas = data.turmas
            }
        
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
      }
    },
    mounted() {
        this.carrega_dash();
    },
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  