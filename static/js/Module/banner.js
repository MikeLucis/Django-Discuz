$(function () {
    // 轮播图
    // 1.加载轮播图数据
    function fn_load_banner() {
        // 发送ajax 获取数据
        $.ajax({
            url: '/boards/banners/',
            type: 'GET',
            dataType: 'json',
            async: false                // 设置为同步
        }).done((res) => {
            if (res.data.count) {
                let content = '';
                let tab_content = '';
                res.data.banners.forEach((one_banner, index) => {
                    if (index === 0) {        // 第一页 加active属性
                        content = `<li style="display:block;">
                                        <a href="/boards/${one_banner.board_id}/topics/${one_banner.topic_id}/">
                                            <img src="/static/media/${one_banner.image_url}" alt="${one_banner.topic_title}">
                                        </a>
                                   </li>`;
                        tab_content = '<li class="active"></li>';
                    } else {
                        content = `<li>
                                        <a href="/boards/${one_banner.board_id}/topics/${one_banner.topic_id}/">
                                            <img src="/static/media/${one_banner.image_url}" alt="${one_banner.topic_title}">
                                        </a>
                                   </li>`;
                        tab_content = '<li></li>';
                    }
                    $('.pic').append(content);
                    $('.tab').append(tab_content)
                })
            } else {
                message.showError(res.errmsg)
            }
        })
            .fail(() => {
                message.showError('服务器超时，请重试！')
            })

        // 定义变量
        let $banner = $('.banner');         // banner容器div
        let $picLi = $('.banner .pic li');  // 图片li标签
        let $pre = $('.banner .prev');      // 上一张
        let $next = $('.banner .next');     // 下一张
        let $tabLi = $('.banner .tab li');  // 按钮
        let index = 0;                      // 当前索引

        // 2.点击导航按钮切换
        $tabLi.click(function () {
            index = $(this).index();
            // 点击当前li加上active, 并将所有兄弟li的active去掉
            $(this).addClass('active').siblings('li').removeClass('active');
            // 当前图片淡入, 其它兄弟li的图片淡出
            $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
        });

        // 3.上一张，下一张
        // 点击切换上一张
        $pre.click(() => {
            index--;
            if (index < 0) {
                // 如果当前索引是0,那么点击后index小于0,我们让他退回到最后一张
                index = $tabLi.length - 1       // 最后一张
            }
            // 当前索引的li加active, 其他li去掉active
            $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
            // 当前图片淡入, 其它li的图片淡出
            $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500);
        });
        // 点击切换下一张
        $next.click(() => {
            // 这里单独定义方法, 是为了可以同时使用 定时 和 手动切换
            auto();
        });

        // 图片向前滑动
        function auto() {
            index++;
            // 模等于, 当index为6时, 其模为0, 就重新从0开始, 也就起到一个循环的作用
            index %= $tabLi.length;
            $tabLi.eq(index).addClass('active').siblings('li').removeClass('active');
            $picLi.eq(index).fadeIn(1500).siblings('li').fadeOut(1500)
        }

        // 4.自动切换
        let timer = setInterval(auto, 8000);

        // 5.鼠标滑入 暂停自动播放
        $banner.hover(
            () => {
                // 鼠标移入时, 清除定时器
                clearInterval(timer)
            },
            () => {
                // 鼠标移出时, 重新添加定时器
                timer = setInterval(auto, 8000);
            }
        );
    }

    fn_load_banner();

})