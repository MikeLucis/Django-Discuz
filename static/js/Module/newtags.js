$(function () {
//  Tag最新话题
    function fn_load_tags() {
        $.ajax({
            url: '/boards/tags/',
            type: 'GET',
            dataType: 'json',
            async: false
        }).done((res) => {
            if (res.data.count) {
                let content = "";
                res.data.tags.forEach((item) => {
                    content = `<li><a href="/search/?tag=${item.name}" data-id="${item.id}">${item.name}</a></li>`;
                    $(".tag-point").after(content)
                })
            }
        })
    }

    fn_load_tags();

})