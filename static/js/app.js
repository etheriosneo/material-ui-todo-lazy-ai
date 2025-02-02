document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();

  document.getElementById("taskForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const taskInput = document.getElementById("taskInput");
    const task = taskInput.value.trim();
    if (task) {
      addTask(task);
      taskInput.value = "";
    }
  });
});

function fetchTasks() {
  fetch("/tasks")
    .then((response) => response.json())
    .then((tasks) => {
      const taskList = document.getElementById("taskList");
      taskList.innerHTML = "";
      tasks.forEach((task) => {
        const taskItem = createTaskItem(task);
        taskList.appendChild(taskItem);
      });
    });
}

function addTask(task) {
  fetch("/tasks", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task }),
  }).then(() => {
    fetchTasks();
  });
}

function updateTask(taskId, task) {
  fetch(`/tasks/${taskId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ task }),
  }).then(() => {
    fetchTasks();
  });
}

function deleteTask(taskId) {
  fetch(`/tasks/${taskId}`, {
    method: "DELETE",
  }).then(() => {
    fetchTasks();
  });
}

function completeTask(taskId) {
  fetch(`/tasks/${taskId}/complete`, {
    method: "PUT",
  }).then(() => {
    fetchTasks();
  });
}

function markAsIncomplete(taskId) {
  fetch(`/tasks/${taskId}/incomplete`, {
    method: "PUT",
  }).then(() => {
    fetchTasks();
  });
}

function createTaskItem(task) {
  const taskItem = document.createElement("li");
  taskItem.className = "task-item";
  taskItem.innerHTML = `
    <span>${task.description}</span>
    <button onclick="deleteTask(${task.id})" class="delete-btn">
      <i class="material-icons">delete_outline</i>
    </button>
    <button onclick="completeTask(${task.id})" class="complete-btn">
      <i class="material-icons">check_circle_outline</i>
    </button>
  `;
  return taskItem;
}