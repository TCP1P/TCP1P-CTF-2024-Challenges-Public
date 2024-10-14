/**
 *
 * @param {string} htmlContent
 * @returns {string}
 */
function sanitizeHTML(htmlContent) {
    return htmlContent.replaceAll(/<script/gi, '');
}
window.addEventListener('message', (event) => {
    if (event.origin !== window.location.origin) {
        return;
    }
    const frameOutput = document.createElement('iframe');

    if (sanitizeHTML(atob(event.data)) != atob(event.data)){
        return;
    }

    if (DOMPurify.sanitize(atob(event.data)) != atob(event.data)){
        alert("Don't hack hacker!")
    }

    frameOutput.src = 'data:text/html;base64,' + btoa(atob(event.data));
    frameOutput.addEventListener('load', () => {
        const random = Math.random();
        window.addEventListener('message', (event) => {
            if (random !== event.data.random) {
                return;
            }
            frameOutput.srcdoc = event.data.html;
        });

        frameOutput.contentWindow.postMessage({ random }, '*');
    })

    document.body.appendChild(frameOutput);
});
