document.addEventListener('DOMContentLoaded', () => {
    const dependencies = {
        "test1": ["employee3", "employee4"],  // Опции для "test1"
        "test2": ["employee1", "employee2"]   // Опции для "test2"
    };

    // Функция для обновления field_3 на основе выбора в field_2
    function updateField3(selectElement, initialValue = null) {
        const row = selectElement.closest('.form-row');
        const field3 = row.querySelector('.field_3');
        const selectedValue = selectElement.value.trim();

        // Очищаем предыдущие опции
        field3.innerHTML = '<option value="">Select employee</option>';

        // Добавляем новые опции на основе выбора в field_2
        if (dependencies[selectedValue]) {
            dependencies[selectedValue].forEach(option => {
                const opt = document.createElement('option');
                opt.value = option;
                opt.textContent = option;
                // Если значение совпадает с initialValue, выбираем его
                if (initialValue && option === initialValue) {
                    opt.selected = true;
                }
                field3.appendChild(opt);
            });
        }
    }

    // Инициализация обработчиков для существующих строк
    document.querySelectorAll('.field_2').forEach(select => {
        const row = select.closest('.form-row');
        const field3 = row.querySelector('.field_3');
        const initialValue = field3.value.trim(); // Получаем текущее значение field_3

        // Обновляем field_3 при загрузке страницы
        updateField3(select, initialValue);

        // Привязываем обработчик изменения
        select.addEventListener('change', function () {
            updateField3(this);
        });
    });

    // Добавление новой строки
    document.getElementById('addRow').addEventListener('click', function () {
        const newRow = document.createElement('div');
        newRow.classList.add('form-row');
        newRow.setAttribute('data-id', 'new'); // Указываем, что это новая строка
        newRow.innerHTML = `
            <input type="text" name="field_1" placeholder="Field 1" required />
            <select name="field_2" class="field_2" required>
                <option value="">Select an option</option>
                <option value="test1">test1</option>
                <option value="test2">test2</option>
            </select>
            <select name="field_3" class="field_3" required>
                <option value="">Select employee</option>
            </select>
            <button type="button" class="deleteRow">Delete</button>
        `;

        // Добавляем новую строку в конец контейнера формы
        document.getElementById('dynamicForm').appendChild(newRow);

        // Привязываем обработчик к новому field_2
        newRow.querySelector('.field_2').addEventListener('change', function () {
            updateField3(this);
        });

        // Привязываем обработчик к кнопке удаления
        newRow.querySelector('.deleteRow').addEventListener('click', function () {
            deleteRow(this);
        });
    });

    // Удаление строки
    function deleteRow(button) {
        const row = button.closest('.form-row');
        const rowId = row.getAttribute('data-id');

        if (rowId && rowId !== "new") {
            // Если строка существует в базе данных, отправляем запрос на удаление
            fetch('/delete-row', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: rowId }),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(result => {
                    if (result.message) {
                        alert(result.message);
                        row.remove(); // Удаляем строку из DOM
                    } else {
                        alert(`Error: ${result.error}`);
                    }
                })
                .catch(err => {
                    console.error('Delete failed:', err);
                    alert('Failed to delete row. Check the console for more information.');
                });
        } else {
            // Если строка новая, просто удаляем её из DOM
            row.remove();
        }
    }

    // Сохранение данных формы
    document.getElementById('saveState').addEventListener('click', async function () {
        const rows = document.querySelectorAll('.form-row');
        const jsonData = {
            field_1: [],
            field_2: [],
            field_3: [],
            ids: []  // Добавим сюда id для отслеживания существующих строк
        };

        // Преобразуем данные из FormData в JSON
        rows.forEach(row => {
            const id = row.getAttribute('data-id');  // Получаем id строки
            const field_1 = row.querySelector('input[name="field_1"]').value.trim();
            const field_2 = row.querySelector('select[name="field_2"]').value.trim();
            const field_3 = row.querySelector('select[name="field_3"]').value.trim();

            // Добавляем данные в jsonData
            jsonData.field_1.push(field_1);
            jsonData.field_2.push(field_2);
            jsonData.field_3.push(field_3);
            jsonData.ids.push(id);  // Добавляем id строки
        });

        console.log("Form data to save:", jsonData);  // Логируем данные перед отправкой

        // Проверка, чтобы все поля были заполнены
        if (jsonData.field_1.includes("") || jsonData.field_2.includes("") || jsonData.field_3.includes("")) {
            alert('Please fill out all fields!');
            return;
        }

        try {
            const response = await fetch('/save-form-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(jsonData),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            console.log(result);  // Логируем ответ сервера
            if (response.ok) {
                alert('Data saved successfully!');
                location.reload(); // Перезагружаем страницу, чтобы отобразить обновленные данные
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (err) {
            console.error('Save failed:', err);
            alert('Failed to save data. Check the console for more information.');
        }
    });

    // Привязываем обработчики к кнопкам удаления для существующих строк
    document.querySelectorAll('.deleteRow').forEach(button => {
        button.addEventListener('click', function () {
            deleteRow(this);
        });
    });
});