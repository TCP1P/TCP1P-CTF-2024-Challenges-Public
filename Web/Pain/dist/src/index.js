var random = Math.random();
(async () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const html = form.querySelector('input').value;
        const url = new URL(window.location.href);
        url.searchParams.set('html', btoa(html));

        window.location.href = url.toString();
    });

    const output = document.querySelector('.output');

    const url = new URL(window.location.href);
    const html = url.searchParams.get('html');
    const frameOutput = document.createElement('iframe');
    const flagFrame = document.createElement('iframe');
    const secretDiv = document.querySelector('.secret');


    if (html) {
        frameOutput.src = '/sandbox.html';
        frameOutput.style.width = '100%';
        frameOutput.style.height = '100%';

        console.log(document.cookie)

        const flagBlob = new Blob([document.cookie], { type: 'text/html' });
        const flagUrl = URL.createObjectURL(flagBlob);

        flagFrame.src = flagUrl

        // delete all cookies
        var cookies = document.cookie.split("; ");
        for (var c = 0; c < cookies.length; c++) {
            var d = window.location.hostname.split(".");
            while (d.length > 0) {
                var cookieBase = encodeURIComponent(cookies[c].split(";")[0].split("=")[0]) + '=; expires=Thu, 01-Jan-1970 00:00:01 GMT; domain=' + d.join('.') + ' ;path=';
                var p = location.pathname.split('/');
                document.cookie = cookieBase + '/';
                while (p.length > 0) {
                    document.cookie = cookieBase + p.join('/');
                    p.pop();
                };
                d.shift();
            }
        }

        const shadow = secretDiv.attachShadow({ mode: 'closed' });

        shadow.appendChild(flagFrame);
        output.appendChild(frameOutput);

        frameOutput.addEventListener('load', () => {
            frameOutput.contentWindow.postMessage(html, '*');
        });

        window.addEventListener('message', (event) => {
            if (random !== event.data.random) {
                random = Math.random();
                return;
            }
            console.log(event)
            flagFrame.contentWindow.document.write(event.data.html);
        })
    }

})()
