<?php

add_action('wp_ajax_nopriv_note_form', 'note_form');
add_action('wp_ajax_note_form', 'note_form');

function note_form()
{
    // Generate a random nonce
    $nonce = bin2hex(random_bytes(5));
    header("Content-Security-Policy: default-src 'self';script-src 'self' 'nonce-$nonce'");

    // Include bootstrap CSS
    echo '<link href="' . plugins_url('notes-manager/bootstrap.min.css') . '" rel="stylesheet">';

    if (isset($_COOKIE['notes'])) {
        $notes = maybe_unserialize(wp_unslash($_COOKIE['notes']));

        echo '<div class="container mt-5">';
        echo '<h1 class="mb-3">Notes</h1>';
        echo '<ul class="list-group mb-3">';

        foreach ($notes as $title => $note) {
            $value = esc_html($note['value']);
            $time = esc_html(date('Y-m-d H:i:s', $note['time'])); // Format time as desired

            echo '<li class="list-group-item" id="note-' . esc_attr($title) . '"><strong>' . esc_html($title) . ':</strong> ' . $value . ' (Time: ' . $time . ')' .
                ' <button class="btn btn-info btn-sm mx-2" name="edit" data-title="' . esc_attr($title) . '">Edit</button>
                <button class="btn btn-danger btn-sm" data-title="' . esc_attr($title) . '">Delete</button></li>';
        }
        echo '</ul>';
        echo '</div>';
    }

    // Nonce verification
    if (isset($_POST['nonce']) && !wp_verify_nonce($_POST['nonce'], 'nonce')) {
        die("wrong nonce");
    }

?>
    <div class="container mt-5">
        <h1>Add Note</h1>
        <form id="noteForm">
            <label for="noteTitle">Title:</label>
            <input type="text" id="noteTitle" name="noteTitle" class="form-control mb-2" required>

            <label for="noteValue">Value:</label>
            <textarea id="noteValue" name="noteValue" class="form-control mb-2" required></textarea>
            <input id="noteTime" data-location='<?=sanitize_text_field($_SERVER['REQUEST_URI'])?>' type="hidden" value="<?php if (isset($_POST['now'])) {
                                                echo sanitize_text_field($_POST['now']);
                                            } else {
                                                echo time();
                                            } ?>">

            <input type="submit" value="Add Note" class="btn btn-primary">
        </form>
    </div>

    <script nonce="<?=$nonce?>">
        document.addEventListener('DOMContentLoaded', function() {
            var noteForm = document.getElementById('noteForm');

            // Handle form submission
            noteForm.addEventListener('submit', function(e) {
                e.preventDefault();

                var title = document.getElementById('noteTitle').value;
                var value = document.getElementById('noteValue').value;
                var time = document.getElementById('noteTime').value;

                fetch('/?rest_route=/notes/v1/note', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            title: title,
                            value: value,
                            time: time,
                        }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        location.reload();
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            });

            // Handle delete button click
            document.querySelectorAll('.btn-danger').forEach(function(button) {
                button.addEventListener('click', function() {
                    var title = button.getAttribute('data-title');
                    deleteNote(title);
                });
            });

            // Handle edit button click
            document.querySelectorAll('.btn-info').forEach(function(button) {
                button.addEventListener('click', function() {
                    var title = button.getAttribute('data-title');
                    editNote(title);
                });
            });
        });

        function deleteNote(title) {
            fetch('/?rest_route=/notes/v1/note&title=' + encodeURIComponent(title), {
                    method: 'DELETE',
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('note-' + title).remove(); // Remove the deleted note from the list
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        function editNote(title) {
            fetch('/?rest_route=/notes/v1/note&title=' + encodeURIComponent(title))
                .then(response => response.json())
                .then(data => {
                    document.getElementById('noteTitle').value = data.title;
                    document.getElementById('noteValue').value = data.value.value;
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    </script>
<?php
}
