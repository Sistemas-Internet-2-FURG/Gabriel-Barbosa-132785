<template>
    <h1>Login</h1>
        <label>Usuario</label>
        <input type="text" name="usuario" required v-model="nome">
        <label>Senha</label>
        <input type="password" name="senha" required v-model="senha">
        <button @click="banco">Logar</button>
        <br>
        <h2 v-if="erro == true">Usuario ou senha errados</h2>
  </template>
  
  <script>
  export default {
    name: 'loginPage',
    data() {
        return {
            nome: '',
            senha: '',
            erro: false,
        }
    },
    methods: {
      banco() {
        fetch('http://127.0.0.1:5000/login', {method: "POST", body: JSON.stringify({ nome: this.nome, senha: this.senha })})
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            if (data.ok == 1) {
                this.erro = true
            } else {
                sessionStorage.setItem("access_token", data.access_token);
                this.$emit('muda_pagina', 5)
            }
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
      },
      dashboard() {
        const token = sessionStorage.getItem("access_token")
        fetch('http://127.0.0.1:5000/dashboard', {method: "POST",
        headers: {
                "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify({ nome: '' })})
        .then(response => {
            if (!response.ok) {
            throw new Error('Erro na requisição');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            this.$emit('muda_pagina', 5)
        })
        .catch(error => {
            console.error('Erro ao obter os dados:', error);
        });
      }
    },
    mounted() {
        this.dashboard();
    },
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  