<template>
    <h1>Registro de professor</h1>
    <label>Usuario:</label>
    <input type="text" name="nome" required v-model="nome">
    <label>Senha:</label>
    <input type="password" name="senha" required v-model="senha">
    <button @click="banco">Salvar</button>
    <h3 v-if="erro == true">Esse usuario ja existe</h3>
</template>
  
  <script>
  export default {
    name: 'professorPage',
    data() {
        return {
            erro: false,
            nome: '',
            senha: '',
        }
    },
    methods: {
    tela_dashboard(event) {
        event.preventDefault();
        this.$emit('muda_pagina', 5);
    },
    banco() {
        fetch('http://127.0.0.1:5000/r_professor', {method: "POST", body: JSON.stringify({ nome: this.nome, senha: this.senha })})
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.ok == 0) {
                this.erro = true
            } else {
                this.$emit('muda_pagina', 0)
            }
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
    }
  }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  