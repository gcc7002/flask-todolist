function toggleEditForm(taskId) {
    const form = document.getElementById(`edit-form-${taskId}`);
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
    }
    else {
        form.style.display = "none";
    }
    return false; // Prevent form submission
}