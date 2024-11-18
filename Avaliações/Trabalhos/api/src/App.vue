<template>
  <indexPage v-if="page == 0" @muda_pagina="troca($event)"/>
  <loginPage v-if="page == 1" @muda_pagina="troca($event)"/>
  <cadastroPage v-if="page == 2" @muda_pagina="troca($event)"/>
  <alunoPage v-if="page == 3" @muda_pagina="troca($event)"/>
  <professorPage v-if="page == 4" @muda_pagina="troca($event)"/>
  <dashboardPage v-if="page == 5" @muda_pagina="troca($event)"/>
</template>

<script>
import indexPage from './components/indexPage.vue'
import cadastroPage from './components/cadastroPage.vue'
import professorPage from './components/professorPage.vue'
import alunoPage from './components/alunoPage.vue'
import dashboardPage from './components/dashboardPage.vue'
import loginPage from './components/loginPage.vue'


export default {
  name: 'App',
  components: {
    indexPage,
    cadastroPage,
    alunoPage,
    professorPage,
    dashboardPage,
    loginPage,
  },
  data() {
    return {
      page: 0,
    }
  },
  methods: {
    troca(num){
      this.page = num
    },
  }
}
</script>

<style>

</style>
