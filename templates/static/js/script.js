var menu_triger = '<a class="primary-nav-trigger" href="#0"><span class="menu-icon"></span></a>'
var menu_id = ['<a href="/"><h3>История появления в России</h3></a>',
            '<a href="/danger"><h3>Чем опасен?</h3></a>',
            '<a href="/map"><h3>Карта Борщевика</h3></a>',
            '<a href="/methods"><h3>Способы борьбы</h3></a>',
            '<a href="/application"><h3>Применение</h3></a>',
            '<a href="/pmp"><h3>ПМП при ожогах</h3></a>',
            '<a href="/fight"><h3>Борьба с борщевиком на Смоленщине</h3></a>'];
function check_resize(){
    let windowInnerWidth = window.innerWidth;
    if(windowInnerWidth<=768){
        var menu = document.getElementById("menu_triger");
        if(!$('.primary-nav').hasClass('is-visible')){
            menu.innerHTML = '';
            menu.innerHTML = menu_triger;
            $('.primary-nav-trigger').on('click', function(){
                $('.menu-icon').toggleClass('is-clicked');
                $('.primary-nav').toggleClass('is-visible');
                $('.body').toggleClass('overflow-hidden');
            });
            var menu = document.getElementById("menu");
            menu.innerHTML  = '';
        }

    }
    else{
        var menu = document.getElementById("menu_triger");
        menu.innerHTML  = '';
        var menu = document.getElementById("menu");
        menu.innerHTML = '';
        for(var key in menu_id){
            menu.innerHTML += menu_id[key];
        }
    }
}
window.onresize = function(){
    check_resize();
}
$(document).ready(function($){
    check_resize();
});

