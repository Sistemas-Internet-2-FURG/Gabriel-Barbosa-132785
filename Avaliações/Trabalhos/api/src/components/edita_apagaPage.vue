<template>
    <h1>Editar turma</h1>
        <label>Nome da turma:</label>
        <input type="text" name="nome_turma" value={{ nome }} v-model="nome">
        <label>Turno:</label>
        <input type="text" name="turno" value={{ turno }} v-model="turno">
        <button @click="salvar" name="opcao" value="salvar">Salvar</button>
        <button @click="deletar" name="opcao" value="deletar">Deletar</button>
        <h3 v-if="erro == true">Você não pode apagar uma turma que possui alunos</h3>
</template>
  
  <script>
  export default {
    name: 'edita_apagaPage',
    props: {
        id: null,
    },
    data() {
        return {
            nome: '',
            turno: '',
            erro: false,
        }
    },
    methods: {
        carrega() {
            const token = sessionStorage.getItem("access_token")
            console.log(token)
            fetch('http://127.0.0.1:5000/get;-edita_apaga', {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ id: this.id })
            })
            .then(response => {
                if (!response.ok) {
                throw new Error('Erro na requisição');
                }
                return response.json();
            })
            .then(data => {
                console.log(data)
                
            })
            .catch(error => {
                console.error('Erro ao obter os dados:', error);
            });
        }
    },
    mounted() {
        this.carrega()
    }
  }
  </script>
  
  <!-- Add "scoped" attribute to limit CSS to this component only -->
  <style scoped>
  
  </style>
  