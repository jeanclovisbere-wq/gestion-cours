// Recherche en temps réel
document.addEventListener('DOMContentLoaded', function() {

    // Recherche
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const query = this.value.toLowerCase();
            const rows = document.querySelectorAll('#coursBody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query) ? '' : 'none';
            });
        });
    }

    // Confirmation suppression
    const deleteBtns = document.querySelectorAll('.btn-delete');
    deleteBtns.forEach(btn => {
        if (btn.tagName === 'A' && btn.href.includes('supprimer')) {
            btn.addEventListener('click', function(e) {
                if (!confirm('⚠️ Voulez-vous vraiment supprimer ce cours ?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Animation des lignes du tableau
    const rows = document.querySelectorAll('tbody tr');
    rows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.1}s`;
        row.style.animation = 'fadeIn 0.5s ease forwards';
    });

    // Disparition automatique des alertes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});