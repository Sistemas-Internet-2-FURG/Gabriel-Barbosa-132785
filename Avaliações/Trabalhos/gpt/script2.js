// script.js

function busca(){
    const taskList = document.getElementById("taskList");

    // Envia a tarefa ao servidor
    fetch("http://127.0.0.1:5000/api/tarefas/busca", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    }).then(response => {
        if (!response.ok) {
        throw new Error('Erro ao enviar a tarefa ao servidor.');
        }
        return response.json();
    })
    .then(data => {
        for (var tarefa in data.tarefas) {
            addTaskToList(data.tarefas[tarefa])
            console.log(data.tarefas[tarefa])
        }
        console.log(data);
    })
    .catch(error => {
        console.error('Erro ao obter os dados:', error);
        alert("Não foi possível adicionar a tarefa. Tente novamente.");
    });
}
busca()

function addTaskToList(task) {
    const taskList = document.getElementById("taskList");

    // Criar novo item da lista
    const taskItem = document.createElement("li");
    taskItem.className = "task";
    taskItem.textContent = task;

    // Marcar como concluído ao clicar
    taskItem.onclick = function () {
        taskItem.classList.toggle("completed");
    };

    // Botão de excluir
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Excluir";
    deleteButton.className = "delete-button";
    deleteButton.onclick = async function () {
        await deleteTask(task);
        taskList.removeChild(taskItem);
    };

    taskItem.appendChild(deleteButton);
    taskList.appendChild(taskItem);
}

async function addTask() {
    const taskInput = document.getElementById("taskInput");
    const taskList = document.getElementById("taskList");

    if (taskInput.value === "") {
        alert("Por favor, insira uma tarefa.");
        return;
    }

    const task = taskInput.value;

    try {
        // Envia a tarefa ao servidor
        const response = await fetch("http://127.0.0.1:5000/api/tarefas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ tarefa: task }),
        });

        if (!response.ok) {
            throw new Error("Erro ao enviar a tarefa ao servidor.");
        }

        console.log("Tarefa enviada com sucesso ao servidor!");

        // Adiciona a tarefa localmente na lista
        addTaskToList(task);
    } catch (error) {
        console.error(error.message);
        alert("Não foi possível adicionar a tarefa. Tente novamente.");
    } finally {
        // Limpa o campo de entrada
        taskInput.value = "";
    }
}

function addTaskToList(task) {
    const taskList = document.getElementById("taskList");

    // Criar novo item da lista
    const taskItem = document.createElement("li");
    taskItem.className = "task";
    taskItem.textContent = task;

    // Marcar como concluído ao clicar
    taskItem.onclick = function () {
        taskItem.classList.toggle("completed");
    };

    // Botão de excluir
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Excluir";
    deleteButton.className = "delete-button";
    deleteButton.onclick = async function () {
        await deleteTask(task);
        taskList.removeChild(taskItem);
    };

    taskItem.appendChild(deleteButton);
    taskList.appendChild(taskItem);
}

async function deleteTask(task) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/tarefas/${encodeURIComponent(task)}`, {
            method: "DELETE",
        });

        if (!response.ok) {
            throw new Error("Erro ao remover a tarefa do servidor.");
        }

        console.log("Tarefa removida do servidor com sucesso!");
    } catch (error) {
        console.error(error.message);
        alert("Não foi possível remover a tarefa. Tente novamente.");
    }
}

