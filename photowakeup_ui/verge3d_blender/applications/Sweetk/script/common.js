$(document).ready(function () {
    /*메뉴창 버튼 제어*/
    $('.wrap nav .logo a').click(function () {
        $('.navi').toggleClass('active');
    });


    $('.select_wrap_fir ul li').click(function (e) {
        
        if ($(this).hasClass('active')) {
            $('.select_wrap_fir ul li').removeClass('active');
        } else {
            $('.select_wrap_fir ul li').removeClass('active');
            $(this).addClass('active');
        };
        e.preventDefault();
    });

    $('.select_wrap_sec ul li').click(function (e) {
        if ($(this).hasClass('active')) {
            $('.select_wrap_sec ul li').removeClass('active');
        } else {
            $('.select_wrap_sec ul li').removeClass('active');
            $(this).addClass('active');
        };
        e.preventDefault();
    });

});