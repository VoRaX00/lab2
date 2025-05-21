// устанавливаем соответствие между полями формы и столбцами таблицы
let correspond = {
    "Название": "structure",
    "Тип": "category",
    "Страна": "country",
    "Город": "city",
    "Год": ["yearFrom", "yearTo"],
    "Высота": ["heightFrom", "heightTo"]
}

let dataFilter = (dataForm) => {
    let dictFilter = {};

    // Перебираем все элементы формы с фильтрами
    for (let j = 0; j < dataForm.elements.length; j++) {
        // Выделяем очередной элемент формы
        let item = dataForm.elements[j];

        // Пропускаем кнопки (они не нужны в фильтре)
        if (item.type === "button") continue;

        // Получаем значение элемента
        let valInput = item.value;

        // Обработка текстовых полей
        if (item.type === "text") {
            valInput = valInput.toLowerCase(); // Приводим к нижнему регистру
        }

        // Обработка числовых полей
        if (item.type === "number") {
            if (valInput === "") {
                // Если поле пустое
                if (item.id.includes("From")) {
                    valInput = -Infinity; // Для полей "From" используем -бесконечность
                } else if (item.id.includes("To")) {
                    valInput = Infinity; // Для полей "To" используем +бесконечность
                }
            } else {
                valInput = Number(valInput); // Преобразуем значение в число
            }
        }

        // Формируем очередной элемент ассоциативного массива
        dictFilter[item.id] = valInput;
    }

    return dictFilter;
};

let filterTable = (data, idTable, dataForm) => {
    // Получаем данные из полей формы
    let datafilter = dataFilter(dataForm);

    // Фильтруем данные
    let tableFilter = data.filter(item => {
        let result = true;

        for (let key in item) {
            let val = item[key];

            if (typeof val === "string") {
                val = val.toLowerCase();
                let filterValue = datafilter[correspond[key]];
                // Проверяем только если фильтр не пустой
                if (filterValue) {
                    result &&= val.includes(filterValue);
                }
            }

            if (typeof val === "number") {
                let filterFrom = datafilter[correspond[key][0]];
                let filterTo = datafilter[correspond[key][1]];
                result &&= val >= filterFrom && val <= filterTo;
            }
        }

        return result;
    });

    // Очищаем таблицу перед обновлением
    clearTable(idTable);

    // Создаем таблицу с отфильтрованными данными
    createTable(tableFilter, idTable);

    // Применяем текущую сортировку, если она есть
    let sortForm = document.getElementById("sort");
    if (sortForm) {
        let sortArr = createSortArr(sortForm);
        if (sortArr.length > 0) {
            sortTable(idTable, sortForm);
        }
    }
};

let clearFilter = (idTable, data, dataForm) => {
    // Очищаем все поля формы
    for (let i = 0; i < dataForm.elements.length; i++) {
        let element = dataForm.elements[i];

        // Пропускаем кнопки (они не нужны для очистки)
        if (element.type === "button") continue;

        // Очищаем значение поля
        element.value = "";
    }

    // Очищаем таблицу
    clearTable(idTable);

    // Выводим таблицу с исходными данными
    createTable(data, idTable);

    // Проверяем, есть ли активная сортировка
    let sortForm = document.getElementById("sort");
    if (sortForm) {
        let sortArr = createSortArr(sortForm);
        if (sortArr.length > 0) {
            // Если есть активная сортировка, применяем её
            sortTable(idTable, sortForm);
        }
    }
};