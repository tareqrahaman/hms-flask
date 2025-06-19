let formToDelete = null;

document.querySelectorAll('.delete-btn').forEach(button => {
  button.addEventListener('click', function () {
    formToDelete = this.closest('form');
    const modal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
    modal.show();
  });
});

document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
  if (formToDelete) {
    formToDelete.submit();
  }
});
