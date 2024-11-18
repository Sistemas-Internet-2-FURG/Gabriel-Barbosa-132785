<template>
    <h1>Registro de Aluno</h1>
    <div v-if="erro_turma == false">
        <label>Usuario:</label>
        <input type="text" name="nome" required v-model="nome">
        <label>Senha:</label>
        <input type="password" name="senha" required v-model="senha">
        <div v-for="(turma, index) in turmas" v-bind:key="index">
            <input type="radio" name="escolha" :value="turma.id" required v-model="turma_escolhida">
            <label>Turma: {{ turma.turma }}, Turno: {{ turma.turno }}</label>
            <br>
        </div>
        <button @click="banco">Salvar</button>
        <h3 v-if="erro_nome == true">Esse usuario ja existe</h3>
    </div>
    <div v-if="erro == true">
        <h2>Não a turmas cadastradas no momentos</h2>
    </div>
</template>
  
  <script>
  export default {
    name: 'alunoPage',
    data() {
        return {
            erro_turma: false,
            erro_nome: false,
            nome: '',
            senha: '',
            turma_escolhida: '',
            turmas: {},
        }
    },
    methods: {
    tela_dashboard(event) {
        event.preventDefault();
        this.$emit('muda_pagina', 5);
    },
    banco() {
        fetch('http://127.0.0.1:5000/r_aluno', {method: "POST", body: JSON.stringify({ nome: this.nome, senha: this.senha, turma: this.turma_escolhida })})
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.ok == 0) {
                this.erro_turma = true
            } else if (data.ok == 1) {
                this.erro_nome = true
            } else {
                this.$emit('muda_pagina', 0)
            }
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
    },
    get_turmas() {
        fetch('http://127.0.0.1:5000/get_turmas', {method: "POST"})
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            if (data.ok == 0) {
                this.erro = true
            } else {
                this.turmas = data.turmas
            }
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
    }
  },
  mounted() {
        this.get_turmas();
    },
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  