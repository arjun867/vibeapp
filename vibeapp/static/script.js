$(document).ready(function() {
    // Function to scroll to the bottom of the messages container
    function scrollToBottom() {
        var messagesContainer = document.querySelector('.messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    $('.chat-btn').click(function() {
        var userId = $(this).data('user-id');
        $.ajax({
            url: '/chat/' + userId + '/',
            success: function(response) {
                $('#chat-container').html(response);
                scrollToBottom(); // Scroll to the bottom when loading new chat
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
                scrollToBottom(); // Scroll to the bottom after fetching new messages
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
                scrollToBottom(); // Scroll to the bottom after sending a message
            }
        });
    });

    // Scroll to the bottom when the page loads
    scrollToBottom();

    // Toggle profile view
    document.getElementById('toggle-profile-btn').addEventListener('click', function() {
        var profileDiv = document.getElementById('receiver-profile');
        if (profileDiv.style.display === 'none' || profileDiv.style.display === '') {
            profileDiv.style.display = 'block';
            this.textContent = 'Hide Profile';
        } else {
            profileDiv.style.display = 'none';
            this.textContent = 'View Profile';
        }
    });
});
