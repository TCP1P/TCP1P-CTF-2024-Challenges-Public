<?php

/**
 * Plugin Name: GADGET
 * Description: gadget
 * Version: 1.0
 * Author: Dimas Maulana
 */

class GADGET
{
    private string $value = '';
    public function __unserialize(array $data): void
    {
        if (is_admin()){
            echo __CLASS__ . " has been unserialized with value\n";
            foreach ($data as $key => $value) {
                echo "$key => $value";
            }
        }
    }
}
