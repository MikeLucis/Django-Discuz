// class Swiper {
//     constructor(id) {
//         this.box = document.querySelector(id);
//         this.picBox = this.box.querySelector('ul');
//         this.indexBox = this.box.querySelector('.index-box');
//         this.imgWidth = this.box.clientWidth;
//         this.index = 1;
//         this.animated = false;
//         this.imgNums = this.picBox.children.length;
//         this.init();
//     }
//
//     init() {
//         this.loadBanner();
//         this.initPoint();
//         this.copyPic();
//         this.leftRight();
//     }
//
//     loadBanner() {
//         $.ajax({
//             url: '/boards/banners/',
//             type: 'GET',
//             dataType: 'json',
//             async: false
//         }).done((res) => {
//             if (res.count) {
//                 let li = '';
//                 res.data.banners.forEach((item, index) => {
//                     li = `<li><img width="1226" height="460" src="/static/media/${item.image_url}" alt=""></li>`;
//                     $('.img').append(li);
//                 })
//             } else {
//                 alert(res.errmsg)
//             }
//         }).fail(() => {
//             alert("服务器超时，请重试！")
//         })
//     }
//
//     initPoint() {
//         const num = this.picBox.children.length;
//         let frg = document.createDocumentFragment();
//         for (let i = 1; i <= num; i++) {
//             let li = document.createElement('li');
//             if (i === 1) {
//                 li.className = 'active';
//             }
//             li.setAttribute('data-index', i);
//             frg.appendChild(li);
//         }
//
//         this.indexBox.children[0].style.width = num * 10 * 2 + 'px';
//         this.indexBox.children[0].appendChild(frg);
//
//         this.indexBox.children[0].addEventListener('click', (e) => {
//             let pointIndex = e.target.getAttribute('data-index');
//             let offset = (pointIndex - this.index) * this.imgWidth;
//             this.index = pointIndex;
//             this.move(offset);
//         });
//     }
//
//     copyPic() {
//         const first = this.picBox.firstElementChild.cloneNode(true);
//         const last = this.picBox.lastElementChild.cloneNode(true);
//
//         this.picBox.appendChild(first);
//         this.picBox.insertBefore(last, this.picBox.firstElementChild);
//
//         this.picBox.style.width =
//             this.imgWidth * this.picBox.children.length + 'px';
//         this.picBox.style.left = -1 * this.imgWidth + 'px';
//     }
//
//     animate(offset) {
//         const time = 1000;
//         const rate = 100;
//         this.animated = true;
//         let speed = offset / (time / rate);
//         let goal = parseFloat(this.picBox.style.left) - offset;
//
//         let animate = setInterval(() => {
//             if (
//                 (this.picBox.style.left === goal) |
//                 (Math.abs(
//                     Math.abs(parseFloat(this.picBox.style.left)) - Math.abs(goal)
//                     ) <
//                     Math.abs(speed))
//             ) {
//                 this.picBox.style.left = goal + 'px';
//                 this.animated = false;
//                 clearInterval(animate);
//
//                 if (parseFloat(this.picBox.style.left) === 0) {
//                     this.picBox.style.left = -this.imgNums * this.imgWidth + 'px';
//                 } else if (
//                     parseFloat(this.picBox.style.left) ===
//                     -(this.imgNums + 1) * this.imgWidth
//                 ) {
//                     this.picBox.style.left = -this.imgWidth + 'px';
//                 }
//             } else {
//                 this.picBox.style.left =
//                     parseFloat(this.picBox.style.left) - speed + 'px';
//             }
//         }, rate);
//     }
//
//     move(offset) {
//         this.animate(offset);
//         const num = this.indexBox.children[0].children.length;
//         for (let i = 0; i < num; i++) {
//             this.indexBox.children[0].children[i].className = '';
//         }
//         this.indexBox.children[0].children[this.index - 1].className = 'active';
//     }
//
//     leftRight() {
//         this.box.querySelector('.left-box').addEventListener('click', () => {
//             if (this.animated) {
//                 return;
//             }
//
//             if (this.index - 1 < 1) {
//                 this.index = this.imgNums;
//             } else {
//                 this.index--;
//             }
//             this.move(-this.imgWidth);
//         });
//         this.box.querySelector('.right-box').addEventListener('click', () => {
//             if (this.animated) {
//                 return;
//             }
//
//             if (this.index + 1 > this.imgNums) {
//                 this.index = 1;
//             } else {
//                 this.index++;
//             }
//             this.move(this.imgWidth);
//         });
//     }
// }

/*=== bannerStart ===*/
$(function () {
    // 轮播图
    // 1.加载轮播图数据
    function fn_load_banner() {
        // 发送ajax 获取数据
        $
            .ajax({
                url: '/boards/banners/',
                type: 'GET',
                dataType: 'json',
                async: false                // 设置为同步
            })
            .done((res) => {
                if (res.count) {
                    let content = '';
                    let tab_content = '';
                    res.data.banners.forEach((one_banner, index) => {
                        if (index === 0) {        // 第一页 加active属性
                            content = `<li style="display:block;"><a href="/boards/${one_banner.board_id}/topics/${one_banner.topic_id}/">
                 <img src="/static/media/${one_banner.image_url}" alt="${one_banner.topic_title}"></a></li>`;
                            tab_content = '<li class="active"></li>';
                        } else {
                            content = `<li><a href="/boards/${one_banner.board_id}/topics/${one_banner.topic_id}/"><img src="/static/media/${one_banner.image_url}" alt="${one_banner.topic_title}"></a></li>`;
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
    }

    fn_load_banner();
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
})