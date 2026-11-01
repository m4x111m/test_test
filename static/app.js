const form = document.querySelector("#task-form");
const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const tasksContainer = document.querySelector("#tasks");
const message = document.querySelector("#message");

async function api(url, options = {}) {
    const response = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Ошибка сервера");
    }

    return data;
}

function showMessage(text = "") {
    message.textContent = text;
}

function renderTasks(tasks) {
    tasksContainer.replaceChildren();

    if (tasks.length === 0) {
        const empty = document.createElement("p");
        empty.textContent = "Пока нет задач. Добавь первую!";
        tasksContainer.append(empty);
        return;
    }

    for (const task of tasks) {
        const card = document.createElement("article");
        card.className = "task";

        if (task.completed) {
            card.classList.add("completed");
        }

        const content = document.createElement("div");
        content.className = "task-content";

        const heading = document.createElement("h3");
        heading.textContent = task.title;

        const description = document.createElement("p");
        description.textContent = task.description || "Без описания";

        content.append(heading, description);

        const actions = document.createElement("div");
        actions.className = "task-actions";

        const toggleButton = document.createElement("button");
        toggleButton.textContent = task.completed ? "Вернуть" : "Выполнить";

        toggleButton.addEventListener("click", async () => {
            try {
                await api(`/api/tasks/${task.id}`, {
                    method: "PATCH",
                    body: JSON.stringify({
                        completed: !Boolean(task.completed)
                    })
                });
                await loadTasks();
            } catch (error) {
                showMessage(error.message);
            }
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Удалить";
        deleteButton.className = "delete";

        deleteButton.addEventListener("click", async () => {
            try {
                await api(`/api/tasks/${task.id}`, { method: "DELETE" });
                await loadTasks();
            } catch (error) {
                showMessage(error.message);
            }
        });

        actions.append(toggleButton, deleteButton);
        card.append(content, actions);
        tasksContainer.append(card);
    }
}

async function loadTasks() {
    try {
        const tasks = await api("/api/tasks");
        renderTasks(tasks);
        showMessage();
    } catch (error) {
        showMessage(error.message);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    try {
        await api("/api/tasks", {
            method: "POST",
            body: JSON.stringify({
                title: titleInput.value,
                description: descriptionInput.value
            })
        });

        form.reset();
        await loadTasks();
    } catch (error) {
        showMessage(error.message);
    }
});

loadTasks();
