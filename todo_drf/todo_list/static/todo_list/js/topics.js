document.getElementById('toggle-menu').addEventListener('click', function() {
    const sidebar = document.getElementById('sidebar');

    // Переключаем класс для сворачивания/разворачивания меню
    sidebar.classList.toggle('collapsed');

    // Изменяем текст кнопки в зависимости от состояния
    this.textContent = sidebar.classList.contains('collapsed') ? '▶️' : '◀️';
});