<?php

function get_xor($str){
    for ($i = 10; $i < 99; $i++) {
        for ($j = 10; $j < 99; $j++) {
            if ((hex2bin(strval($j)) ^ hex2bin(strval($i))) === $str) {
                return [$j, $i];
            }
        }
    }
    return false;
}

function get_xor_str($str){
    $result = [];

    foreach (str_split($str) as $char) {
        $result[] = get_xor($char);
    }

    return $result;
}

function get_xor_joined($str){
    $result = "join(hex2bin(00),[";
    $arrxor = get_xor_str($str);

    foreach ($arrxor as $ab){
        $a = $ab[0];
        $b = $ab[1];
        $result .= "hex2bin($a)^hex2bin($b),";
    }

    $result = rtrim($result, ',') . "])";

    return $result;
}

$inputString = $argv[1];
echo get_xor_joined($inputString);
