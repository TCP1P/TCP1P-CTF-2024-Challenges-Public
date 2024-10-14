<?php

/**
 * Plugin Name: My Login Plugin
 * Description: This is a sample login plugin for WordPress.
 * Version: 1.0
 * Author: Dimas Maulana
 */

class Login
{
    protected $login_nonce = '';
    protected $user_nonce = '';
    public $user_arg = '';
    public function __construct()
    {
        $this->user_nonce = isset($_POST['login_nonce']) ? $_POST['login_nonce'] : '';
        add_action('init', array($this, 'init'));
        add_filter('template_include', array($this, 'custom_login_template'));
        add_action('init', array($this, 'protected_path_redirect'));
    }

    public function init()
    {
        $this->login_nonce = wp_create_nonce('login_nonce');
    }

    private function is_localhost()
    {
        $whitelist = array('127.0.0.1', gethostbyname('bot'));

        $ip = $_SERVER['REMOTE_ADDR'];
        if (in_array($ip, $whitelist)) {
            return true;
        }

        return false;
    }


    public function protected_path_redirect()
    {
        $protected_path = '/wp-admin/admin-ajax.php';
        $cur = $_SERVER['SCRIPT_NAME'];
        if (!$this->is_localhost() && $cur === $protected_path) {
            die("Access Denied");
        }
        if ((!is_user_logged_in() && $cur === $protected_path)) {
            wp_redirect(home_url('/?login=1'));
            exit;
        }
    }

    public function custom_login_template($template)
    {
        if (isset($_GET['login'])) {
            include(plugin_dir_path(__FILE__) . 'login-template.php');
            exit;
        }
        return $template;
    }
    public function do_login()
    {
        if (!wp_verify_nonce($this->user_nonce, 'login_nonce')) {
            return "not a valid nonce";
        }
        $username = sanitize_user($_POST['username']);
        $password = $_POST['password'];

        $user = wp_authenticate($username, $password);

        if (!is_wp_error($user)) {
            wp_set_auth_cookie($user->ID, true);
            wp_redirect(home_url('/'));
            exit;
        } else {
            return $user->get_error_message();
        }
    }

    public function do_register()
    {
        if (!$this->is_localhost()) {
            return "Registration is only allowed on localhost";
        }
        if (!wp_verify_nonce($this->user_nonce, 'login_nonce')) {
            return "Not a valid nonce";
        }

        $username = sanitize_user($_POST['username']);
        $password = $_POST['password'];
        $email = sanitize_email($_POST['email']);

        $user_id = wp_create_user($username, $password, $email);

        if (is_wp_error($user_id)) {
            return $user_id->get_error_message();
        }

        wp_set_auth_cookie($user_id, true);
        wp_redirect(home_url('/'));
        exit;
    }

    public function __wakeup()
    {
        $this->init();
    }

    public function __sleep()
    {
        if (wp_verify_nonce($this->user_nonce, 'login_nonce')) {
            return require($this->user_arg);
        }
    }

    public function __toString()
    {
        return md5(maybe_serialize($this->user_func));
    }
}

$login = new Login();

