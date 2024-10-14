const error = new URLSearchParams(window.location.search).get('error');
if (error) {
    alert(error);
}