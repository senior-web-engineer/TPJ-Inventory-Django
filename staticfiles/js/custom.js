$(function () {
    var current = location.pathname;
    $('.sidebar .nav-item.active').removeClass('active');
    $(`.sidebar .nav-link[href='${current}']`).parent('.nav-item').addClass('active');
});