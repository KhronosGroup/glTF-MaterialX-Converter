// Include the Mermaid.js library
var script = document.createElement('script');
script.src = 'https://cdn.jsdelivr.net/npm/mermaid@9/dist/mermaid.min.js';
script.onload = function () {
    mermaid.initialize({
        startOnLoad: true,
        theme: document.body.classList.contains('vscode-dark') || document.body.classList.contains('vscode-high-contrast')
            ? 'dark'
            : 'default'
    });
};
document.head.appendChild(script);
