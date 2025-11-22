const API_URL = "/todos"; // relative path با StaticFiles

const todoForm = document.getElementById("todo-form");
const todoList = document.getElementById("todo-list");
const searchInput = document.getElementById("search");

// -------------------- FETCH AND RENDER --------------------
async function fetchTodos()
{
    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error("Failed to fetch todos");
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error("Error fetching todos:", error);
    }
}

function renderTodos(todos) {
    todoList.innerHTML = "";
    todos.forEach(todo => {
        const li = document.createElement("li");
        li.className = todo.completed ? "completed" : "";

        li.innerHTML = `
            <span>${todo.title} - ${todo.description || ""} 
            <br><small>Created: ${new Date(todo.created_at).toLocaleString()}</small>
            ${todo.updated_at !== todo.created_at ? `<br><small>Updated: ${new Date(todo.updated_at).toLocaleString()}</small>` : ""}
            </span>
            <div>
                <button class="action-btn complete-btn">${todo.completed ? "Undo" : "Complete"}</button>
                <button class="action-btn delete-btn">Delete</button>
            </div>
        `;

        li.querySelector(".complete-btn").addEventListener("click", () => {
            toggleComplete(todo.id, !todo.completed);
        });

        li.querySelector(".delete-btn").addEventListener("click", () => {
            deleteTodo(todo.id);
        });

        todoList.appendChild(li);
    });
}

// -------------------- TODO OPERATIONS --------------------
todoForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!title) {
        alert("Title is required");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, description })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || response.statusText}`);
            return;
        }

        todoForm.reset();
        fetchTodos();
    } catch (error) {
        alert("Error adding todo");
        console.error(error);
    }
});

async function toggleComplete(id, completed) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ completed })
        });

        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || response.statusText}`);
            return;
        }

        fetchTodos();
    } catch (error) {
        console.error("Error updating todo:", error);
    }
}

async function deleteTodo(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
        if (!response.ok) {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || response.statusText}`);
            return;
        }
        fetchTodos();
    } catch (error) {
        console.error("Error deleting todo:", error);
    }
}

//  SEARCH BOX 
searchInput.addEventListener("input", async () => {
    const query = searchInput.value.trim();
    if (!query) {
        fetchTodos();
        return;
    }
    try {
        const response = await fetch(`/todos/search?q=${encodeURIComponent(query)}`);
        if (!response.ok) throw new Error("Search failed");
        const todos = await response.json();
        renderTodos(todos);
    } catch (error) {
        console.error("Error searching todos:", error);
    }
});

// init fetching
fetchTodos();
