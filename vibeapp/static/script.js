$(document).ready(function() {
    $('.chat-btn').click(function() {
        var userId = $(this).data('user-id');
        $.ajax({
            url: '/chat/' + userId + '/',
            success: function(response) {
                $('#chat-container').html(response);
            }
        });
    });

    $('#message-form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                content: $('#id_content').val()
            },
            success: function() {
                $('#id_content').val('');
            }
        });
    });
});
