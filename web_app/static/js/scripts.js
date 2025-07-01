document.addEventListener('DOMContentLoaded', () => {
    // Load ad for user
    const userId = localStorage.getItem('userId') || generateUserId();
    localStorage.setItem('userId', userId);
    
    fetch(`/ad?user=${userId}`)
        .then(res => res.json())
        .then(ad => {
            const adContainer = document.querySelector('.ad-container');
            adContainer.innerHTML = `
                <a href="${ad.tracking_url}" target="_blank">
                    <img src="/static/ads/${ad.image}" alt="${ad.brand}">
                </a>
            `;
        });
    
    // Generate user ID if not exists
    function generateUserId() {
        return 'user_' + Math.random().toString(36).substr(2, 9);
    }
});
