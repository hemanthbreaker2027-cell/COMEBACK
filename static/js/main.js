document.addEventListener('DOMContentLoaded', () => {
    console.log('ANIZONEFLIX initialized');

    // Mobile Menu Toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mobileNav = document.getElementById('mobile-nav');
    const closeMenu = document.getElementById('close-menu');

    if (menuToggle && mobileNav && closeMenu) {
        menuToggle.addEventListener('click', () => {
            mobileNav.classList.add('active');
        });

        closeMenu.addEventListener('click', () => {
            mobileNav.classList.remove('active');
        });
    }

    // Smooth scroll for anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Glassmorphism hover effect enhancement
    const cards = document.querySelectorAll('.anime-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.borderColor = 'rgba(255, 60, 0, 0.5)';
        });
        card.addEventListener('mouseleave', () => {
            card.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });
    });
});
