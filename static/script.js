document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('markdown');
    const preview = document.getElementById('preview');

    async function updatePreview() {
        const md = textarea.value;
        const response = await fetch('/convert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ markdown: md })
        });
        const data = await response.json();
        preview.innerHTML = data.html;
    }

    textarea.addEventListener('input', updatePreview);
    updatePreview(); // Pour afficher l'aperçu initial
}); 