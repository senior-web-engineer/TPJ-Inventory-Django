$(function () {
    var current = location.pathname;
    $('.sidebar .nav-item.active').removeClass('active');
    $(`.sidebar .nav-link[href='${current}']`).parent('.nav-item').addClass('active');

    $('#btn-sync').click(function() {
        $.ajax({
            url: '/create_callback/',
            type: 'post',
            dataType: 'json',
            success: function(data) {
                alert('Success');
            }
        });
        return false;
    });
});