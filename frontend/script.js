let tasks = [];

// Add a task
function addTask() {
    const task = {
        id: tasks.length + 1,
        title: document.getElementById("title").value,
        due_date: document.getElementById("due_date").value,
        estimated_hours: Number(document.getElementById("hours").value),
        importance: Number(document.getElementById("importance").value),
        dependencies: document.getElementById("dependencies").value.split(",").map(s => s.trim()).filter(Boolean)
    };

    tasks.push(task);
    alert("Task added!");
}

// Import JSON
function importJSON() {
    try {
        tasks = JSON.parse(document.getElementById("jsonInput").value);
        alert("JSON Imported Successfully!");
    } catch (err) {
        alert("Invalid JSON!");
    }
}

// Analyze Tasks
function analyzeTasks() {
    document.getElementById("results").innerHTML =
        "<p class='text-gray-600'>Analyzing...</p>";

    setTimeout(() => {
        document.getElementById("results").innerHTML =
            `<pre>${JSON.stringify(tasks, null, 2)}</pre>`;
    }, 400);
}

// Suggest Top 3
function suggestTop3() {
    const sorted = [...tasks].sort((a, b) => b.importance - a.importance).slice(0, 3);

    document.getElementById("results").innerHTML =
        `<pre>${JSON.stringify(sorted, null, 2)}</pre>`;
}
