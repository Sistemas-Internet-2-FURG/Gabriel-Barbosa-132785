<template>
  <h1>Bem-Vindo ao Sitema</h1>
	<hr>
	<a @click="tela_login($event)" href="/">LOGAR?</a>
	ou
	<a @click="tela_cadastro($event)" href="/">CADASTRAR?</a>
</template>

<script>
export default {
  name: 'indexPage',
  methods: {
    tela_cadastro(event) {
        event.preventDefault();
        this.$emit('muda_pagina', 2);
    },
	tela_login(event) {
		event.preventDefault();
        this.$emit('muda_pagina', 1);
	}
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
