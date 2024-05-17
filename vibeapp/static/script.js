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

    function fetchNewMessages() {
        $.ajax({
            url: window.location.pathname,  // Your current chat URL
            data: {
                'fetch_new': true  // Custom parameter to differentiate this request
            },
            success: function(response) {
                // Append new messages to the chat container
                $('.messages ul').html(response.messages_html);
            }
        });
    }

    // Poll for new messages every 5 seconds
    setInterval(fetchNewMessages, 5000);

    // Handling form submission
    $('#message-form').on('submit', function(event) {
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: window.location.pathname,
            data: {
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val(),
                content: $('#id_content').val()
            },
            success: function(response) {
                $('#id_content').val(''); // Clear the input field
                $('.messages ul').html(response.messages_html); // Update messages
            }
        });
    });
    
});
