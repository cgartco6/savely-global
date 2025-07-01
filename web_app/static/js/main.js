document.addEventListener('DOMContentLoaded', () => {
    // Initialize user
    const userId = localStorage.getItem('userId') || generateUserId();
    localStorage.setItem('userId', userId);
    
    // Serve ad
    fetchAd(userId);
    
    // Event listeners
    document.querySelectorAll('.recipe-card').forEach(card => {
        card.addEventListener('click', () => {
            trackRecipeView(card.dataset.id);
        });
    });
});

function generateUserId() {
    return 'user_' + Math.random().toString(36).substr(2, 9);
}

function fetchAd(userId) {
    fetch(`/ad?user_id=${userId}`)
        .then(response => response.json())
        .then(ad => {
            const adContainer = document.querySelector('.ad-container');
            if (ad.type === 'banner') {
                adContainer.innerHTML = `
                    <a href="${ad.tracking_url}" target="_blank">
                        <img src="/static/ads/${ad.content}" alt="${ad.brand} Ad">
                    </a>
                `;
            } else if (ad.type === 'video') {
                adContainer.innerHTML = `
                    <video controls>
                        <source src="/static/ads/${ad.content}" type="video/mp4">
                    </video>
                    <a href="${ad.tracking_url}" target="_blank">Learn More</a>
                `;
            }
        });
}

function trackRecipeView(recipeId) {
    // Send analytics about recipe view
    fetch(`/analytics/recipe-view/${recipeId}`, {
        method: 'POST'
    });
}
