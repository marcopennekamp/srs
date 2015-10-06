function mark_single_kanji(id) {
    mark_kanji(JSON.stringify([id]))
}

function unmark_single_kanji(id) {
    unmark_kanji(JSON.stringify([id]))
}

function unmark_kanji(data) {
    $.ajax({
        url: "/api/unmark/kanji",
        method: "PUT",
        data: data,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            window.location.reload(true);
        }
    });
}

function mark_kanji(data) {
    $.ajax({
        url: "/api/mark/kanji",
        method: "PUT",
        data: data,
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(data) {
            window.location.reload(true);
        }
    });
}