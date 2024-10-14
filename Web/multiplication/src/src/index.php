<?php
    error_reporting(0);
    header("Content-Security-Policy: script-src 'self' 'unsafe-inline';");
    $digit = $_GET['digit'];
    if ((int) $digit) {
        $forbiddenChars = array('<', '>', '`', '~', '(' , ')', ',', '+', '-', '/', '*', '%', '^', '|', '&', '!', '?', ':', ';', '.');

        foreach ($forbiddenChars as $char) {
            if (strpos($digit, $char) !== false) {
                http_response_code(403);
                die('403 Forbidden');
            }
        }
    } else {
        $digit = "0";
    }

?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Beautiful 7</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            text-align: center;
        }

        h1 {
            color: #333;
        }

        form {
            margin-top: 20px;
        }

        input {
            padding: 10px;
            margin: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }

        input[type="text"] {
            width: 150px;
        }

        input[type="submit"] {
            background-color: #4CAF50;
            color: #fff;
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
            color: #4CAF50;
        }

        img {
            max-width: 30%;
            height: auto;
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>

<body>
    <h1>Magical 7</h1>
    <h3 class="result"></h3>
    <form action="/">
        <input type="text" name="digit" placeholder="Enter a digit">
        <input type="submit" value="Calculate">
    </form>
    <script>
        var multiply = function(a, b) {
            return a * b;
        }

        var result = multiply(7, <?php echo $digit; ?>);

        document.querySelector('.result').textContent = 'The result is: ' + result;
    </script>
</body>
</html>