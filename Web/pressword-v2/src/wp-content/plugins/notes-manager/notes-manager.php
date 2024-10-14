<?php

/**
 * Notes Manager: A cookie based note plugin app
 *
 * Plugin Name: Notes Manager
 * Description: A handsome plugin used to crete a note
 * Version:     1.0.0
 * Author:      Dimas Maulana
 */

if (!defined('ABSPATH')) {
    exit;
}

require "ajax.php";


class NotesManager
{
    public string $cookie_name = "notes";

    public function __construct()
    {
        add_action('rest_api_init', array($this, 'register_rest_endpoints'));
        add_action('init', array($this, 'display_init_message'));
    }

    public function register_rest_endpoints()
    {
        register_rest_route('notes/v1', '/health', array(
            'methods' => 'GET',
            'callback' => array($this, 'health_check'),
        ));

        register_rest_route('notes/v1', '/note', array(
            'methods' => 'POST',
            'callback' => array($this, 'post_note'),
        ));

        register_rest_route('notes/v1', '/note', array(
            'methods' => 'GET',
            'callback' => array($this, 'get_note'),
            'args' => array(
                'title' => array(
                    'required' => true,
                    'validate_callback' => function ($param, $request, $key) {
                        return is_string($param);
                    },
                ),
            ),
        ));

        register_rest_route('notes/v1', '/note', array(
            'methods' => 'DELETE',
            'callback' => array($this, 'delete_note'),
            'args' => array(
                'title' => array(
                    'required' => true,
                    'validate_callback' => function ($param, $request, $key) {
                        return is_string($param);
                    },
                ),
            ),
        ));
    }

    public function post_note()
    {
        $json = $this->get_json();

        $title = isset($json->title) ? $json->title : false;
        $value = isset($json->value) ? $json->value : false;
        $time = isset($json->time) ? $json->time : time(); // Use provided time or current time

        if ($title && $value) {
            $existing_notes = isset($_COOKIE[$this->cookie_name]) ? maybe_unserialize(wp_unslash($_COOKIE[$this->cookie_name])) : array();

            $existing_notes[$title] = array(
                'value' => $value,
                'time' => $time,
            );

            setcookie($this->cookie_name, maybe_serialize($existing_notes), time() + 36000, '/', "", false, true);

            return rest_ensure_response([
                'message' => 'Data successfully stored!',
            ]);
        }

        return $this->error_response('Key or data parameter is missing');
    }

    public function get_note(WP_REST_Request $request)
    {
        $title = $request->get_param('title');

        if ($title) {
            $existing_notes = isset($_COOKIE[$this->cookie_name]) ? maybe_unserialize(wp_unslash($_COOKIE[$this->cookie_name])) : array();
            if (isset($existing_notes[$title])) {
                return rest_ensure_response([
                    'title' => $title,
                    'value' => $existing_notes[$title],
                ]);
            } else {
                return $this->error_response('Note not found');
            }
        }

        return $this->error_response('Title parameter is missing');
    }

    public function delete_note(WP_REST_Request $request)
    {
        $title = $request->get_param('title');

        if ($title) {
            $existing_notes = isset($_COOKIE[$this->cookie_name]) ? maybe_unserialize(wp_unslash($_COOKIE[$this->cookie_name])) : array();

            if (isset($existing_notes[$title])) {
                unset($existing_notes[$title]);

                setcookie($this->cookie_name, maybe_serialize($existing_notes), time() + 3600, '/');

                return rest_ensure_response([
                    'message' => 'Note successfully deleted!',
                ]);
            } else {
                return $this->error_response('Note not found');
            }
        }

        return $this->error_response('Title parameter is missing');
    }

    public function health_check()
    {
        return wp_send_json(['status' => 'ok']);
    }

    public function display_init_message()
    {
        error_log('Notes Manager plugin initialized.');
    }

    private function error_response($message)
    {
        $response = new WP_REST_Response(['message' => $message], 400);
        $response->set_status(400);
        return $response;
    }

    private function get_json()
    {
        return json_decode(file_get_contents('php://input'));
    }
}

new NotesManager();
