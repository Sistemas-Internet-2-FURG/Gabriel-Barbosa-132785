<template>
    <h1>Registro</h1>
    <a @click="tela_professor($event)" href="/">PROFESSOR?</a>
    ou
    <a @click="tela_aluno($event)" href="/">ALUNO?</a>
</template>
  
  <script>
  export default {
    name: 'cadastroPage',
    methods: {
    tela_professor(event) {
        event.preventDefault();
        this.$emit('muda_pagina', 4);
    },
    tela_aluno(event) {
        event.preventDefault();
        this.$emit('muda_pagina', 3);
    },
  }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  