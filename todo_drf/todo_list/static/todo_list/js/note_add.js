    const plusIcon = document.getElementById('add-form');
    const formContainer = document.querySelector('.form-container');
     const adder = document.getElementById('adder');
    plusIcon.addEventListener('click', () => {
      formContainer.style.display = 'block';
      adder.style.display = 'none'; // Скрываем плюсик
    });


$(document).ready(function() {
  $('#note-form').submit(function(event) {
    event.preventDefault();
    const catId = document.getElementById('cat-id').value;

    const formData = new FormData(this);


    $.ajax({
      url: `/categories/${catId}/add_notes/`,
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        console.log('Заметка успешно создана:', response);
        window.location.href = `/categories/${catId}/`;
      },
      error: function(error) {
        console.error('Ошибка при создании заметки:', error);
      }
    });
  });
});