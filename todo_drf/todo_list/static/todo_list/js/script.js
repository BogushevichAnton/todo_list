document.getElementById('addTaskBtn').addEventListener('click', function() {
    const taskInput = document.getElementById('taskInput');
    const taskText = taskInput.value.trim();

    if (taskText) {
        const taskList = document.getElementById('taskList');

        const taskCard = document.createElement('div');
        taskCard.className = 'task-card';

        taskCard.innerHTML =
            `<span>${taskText}</span><button onclick='this.parentElement.remove()'>Удалить</button>`
        ;

        taskList.appendChild(taskCard);
        taskInput.value = '';
    }
});