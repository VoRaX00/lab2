table.js// Формируем массив для сортировки по уровням
let createSortArr = (data) => {
    let sortArr = [];

    // Находим все SELECT в форме
    let sortSelects = data.getElementsByTagName('select');

    // Перебираем все SELECT
    for (let i = 0; i < sortSelects.length; i++) {
        // Получаем номер выбранной опции
        let keySort = sortSelects[i].value;

        // Если выбрана опция "Нет", завершаем формирование массива
        if (keySort == 0) {
            break;
        }

        // Получаем значение флажка для порядка сортировки
        // Имя флажка формируется как имя поля SELECT + "Desc"
        let desc = document.getElementById(sortSelects[i].id + 'Desc').checked;

        // Добавляем объект с параметрами сортировки в массив
        sortArr.push({
            column: keySort - 1, // Номер столбца (начинается с 0)
            order: desc // Порядок сортировки (true — по убыванию, false — по возрастанию)
        });
    }

    return sortArr;
};

let sortTable = (idTable, data) => {
    // Формируем управляющий массив для сортировки
    let sortArr = createSortArr(data);

    // Если сортировка не требуется (все поля выбраны как "Нет"), завершаем выполнение
    if (sortArr.length === 0) {
        return false;
    }

    // Находим нужную таблицу
    let table = document.getElementById(idTable);

    // Сохраняем строку заголовка
    let headerRow = table.rows[0];

    // Получаем названия столбцов из заголовков
    let columnNames = [];
    for (let i = 0; i < headerRow.cells.length; i++) {
        columnNames.push(headerRow.cells[i].textContent);
    }

    // Преобразуем строки таблицы в массив (исключая заголовки)
    let rowData = Array.from(table.rows).slice(1);

    // Сортируем данные по всем уровням сортировки
    rowData.sort((first, second) => {
        for (let i in sortArr) {
            let key = sortArr[i].column; // Номер столбца для сортировки
            let valueFirst = first.cells[key].innerHTML; // Значение из первой строки
            let valueSecond = second.cells[key].innerHTML; // Значение из второй строки

            // Для столбцов "Год" и "Высота" преобразуем значения в числа
            if (columnNames[key] === "Год" || columnNames[key] === "Высота") {
                valueFirst = parseFloat(valueFirst) || 0;
                valueSecond = parseFloat(valueSecond) || 0;
            }

            // Учитываем порядок сортировки (по возрастанию или убыванию)
            if (sortArr[i].order) { // Если order = true (по убыванию)
                if (valueFirst < valueSecond) {
                    return 1; // Первая строка должна быть после второй
                } else if (valueFirst > valueSecond) {
                    return -1; // Первая строка должна быть перед второй
                }
            } else { // Если order = false (по возрастанию)
                if (valueFirst > valueSecond) {
                    return 1; // Первая строка должна быть после второй
                } else if (valueFirst < valueSecond) {
                    return -1; // Первая строка должна быть перед второй
                }
            }
            // Если значения равны, переходим к следующему уровню сортировки
        }
        return 0; // Строки равны по всем уровням сортировки
    });

    // Обновляем таблицу на странице
    let tbody = table.querySelector('tbody');
    if (!tbody) {
        tbody = document.createElement('tbody');
        table.appendChild(tbody);
    }

    // Очищаем текущее содержимое таблицы
    tbody.innerHTML = '';

    // Добавляем заголовок обратно в таблицу
    if (headerRow) {
        tbody.appendChild(headerRow);
    }

    // Добавляем отсортированные строки в таблицу
    rowData.forEach(row => {
        tbody.appendChild(row);
    });
};

let resetSort = (idTable, dataForm) => {
    // Сбрасываем поля формы сортировки
    let sortSelects = dataForm.getElementsByTagName('select');
    for (let i = 0; i < sortSelects.length; i++) {
        sortSelects[i].selectedIndex = 0;
        sortSelects[i].disabled = i > 0;
    }

    // Сбрасываем флажки для порядка сортировки
    let checkboxes = dataForm.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });

    // Очищаем таблицу
    clearTable(idTable);

    // Восстанавливаем данные с учетом текущих фильтров
    let filterForm = document.getElementById("filter");
    if (filterForm) {
        // Если есть активные фильтры, применяем их
        filterTable(buildings, idTable, filterForm);
    } else {
        // Иначе просто создаем таблицу с исходными данными
        createTable(buildings, idTable);
    }
};