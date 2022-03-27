$(function () {
//  HotTopic最热话题
    function fn_load_hotopics() {
        $.ajax({
            url: '/boards/hotopics/',
            type: 'GET',
            dataType: 'json',
            async: false
        }).done((res) => {
            if (res.data.count) {
                let content = "";
                res.data.topics.forEach((item) => {
                    content = `<li><a href="/boards/${item.board}/topics/${item.id}/" target="_blank"><div class="recommend-thumbnail"><img src="${item.image_url}" alt="${item.subject}"></div><p class="info">${item.subject}</p></a></li>`;
                    $(".Hotopic-point").append(content);
                })
            }
        })
    }

    fn_load_hotopics();

})