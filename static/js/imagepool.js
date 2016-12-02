//Ебаный пиздец
//Что здесь блять происходит


function getCaretPos(jQobject) {
    var obj = jQobject.get(0);
    obj.focus();
    if (document.selection) {
        var sel = document.selection.createRange();
        var clone = sel.duplicate();
        sel.collapse(true);
        clone.moveToElementText(obj);
        clone.setEndPoint('EndToEnd', sel);
        return clone.text.length;
    }   else if (obj.selectionStart !== false) return obj.selectionStart;
    else return 0;
}

// Получает словарь от функции get_list
function getImageList(url) {
    $.getJSON(url, function(data) {
        var images = $("#imagepool_image_list td.image");
        //Очищает словарь от присутствующих файлов
        images.empty();

        //Создает в каждой ячейке словаря с привязанным стилем image две гиперссылки:
        //Ссылку на само изображение и ссылку на удаление изображения
        for (var i = 0; i < data.images.length; i++) {
            $(images.get(i)).append("<a class='insert' href='" +
            data.images[i].src + "'><img src='" + data.images[i].src +
            "'></a><br><a class='delete' href='" + data.images[i].delete_src +
            "'>Удалить</a>");
    }

    //Если это первая страница списка, привязывает стиль отключающий ее
    //В другом случае - пишет в атрибут href ee тега а ссылку на преведущую страницу
    var link = $("#imagepool_prev");
    if (data.prev_url == "") {
        link.addClass("disabled");
        link.attr("href", "#");
    }   else {
        link.removeClass("disabled");
        link.attr("href", data.prev_url);
    }

    //Аналогичные действия для последней страницы
    var link = $("#imagepool_next");
    if (data.next_url == "") {
        link.addClass("disabled");
        link.attr("href", "#");
    }   else {
        link.removeClass("disabled");
        link.attr("href", data.next_url);
    }
    });
}

//Основной код, выполняющийся при загрузке страницы
$(function() {
    // Получение объекта jQuery представляющий область редактирования content
    // где выводится содержимое новости
    var contentField = $("form textarea[name=content]");
    $("#imagepool_prev, #imagepool_next").click(function(evt) {
        evt.preventDefault();
        getImageList($(this).attr("href"));
    });

    // Привязывает к событию load ифрейма image_output обработчик
    // Выполняется сразу после загрузки файла и грузит первую страницу списка
    // Взяв ее адрес из атрибута href тега <table> таблицы imagepool_image_list
    $("#imagepool_output").on("load", function() {
        getImageList($("#imagepool_image_list").attr("href"));
    });
    $("#imagepool_image_list").on("click", "td.image a.insert",
    function(evt) {
        evt.preventDefault();
        var content = contentField.val();
        var position = getCaretPos(contentField);
        content = content.substring(0, position) + "[img]" +
            location.protocol + "//" + location.host +
            $(this).attr("href") + "[/img]" + content.substring(position);
        contentField.val(content);
   });
   $("#imagepool_image_list").on("click", "td.image a.delete",
   function(evt) {
        evt.preventDefault();
        if (window.confirm("Удалить изображение?")) {
            $.getJSON($(this).attr("href"), function(data) {
                getImageList($("#imagepool_image_list").attr("href"));
            });
        }
    });
    getImageList($("#imagepool_image_list").attr("href"));
});
