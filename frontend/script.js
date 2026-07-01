const API_URL = 'http://127.0.0.1:5000/api/tasks';

async function refreshDashboard() {
    const response = await fetch(API_URL);
    const tasks = await response.json();
    
    // Update List
    const list = document.getElementById('taskList');
    const count = document.getElementById('count');
    list.innerHTML = '';
    count.innerText = tasks.length;
    
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${task.title}</span> 
                        <button onclick="deleteTask(${task.id})">Delete</button>`;
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById('taskInput');
    if (!input.value) return;
    await fetch(API_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ title: input.value })
    });
    input.value = '';
    refreshDashboard();
}

async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    refreshDashboard();
}

document.getElementById('addBtn').addEventListener('click', addTask);
refreshDashboard();