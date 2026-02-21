// Navbar and Mobile Menu logic
(function() {
  'use strict';

  const navbar = document.getElementById('navbar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const body = document.body;
  
  // Select logo elements for color switching
  const logoMain = navbar.querySelector('.font-serif');
  const logoSub = navbar.querySelector('span[class*="tracking-[0.4em]"]');

  function setMenuIcon(isOpen) {
    if (isOpen) {
      mobileMenuBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x text-white">
          <path d="M18 6 6 18"></path>
          <path d="m6 6 12 12"></path>
        </svg>`;
      if (logoMain) logoMain.classList.replace('text-texts', 'text-white');
      if (logoSub) logoSub.classList.replace('text-texts/60', 'text-white/60');
    } else {
      mobileMenuBtn.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu text-texts">
          <path d="M4 5h16"></path>
          <path d="M4 12h16"></path>
          <path d="M4 19h16"></path>
        </svg>`;
      if (logoMain) logoMain.classList.replace('text-white', 'text-texts');
      if (logoSub) logoSub.classList.replace('text-white/60', 'text-texts/60');
    }
  }

  // Mobile Menu Toggle
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpening = mobileMenu.classList.contains('hidden');
      
      if (isOpening) {
        mobileMenu.classList.remove('hidden');
        body.classList.add('overflow-hidden');
        setMenuIcon(true);
      } else {
        mobileMenu.classList.add('hidden');
        body.classList.remove('overflow-hidden');
        setMenuIcon(false);
      }
    });

    // Close menu when clicking links
    const mobileLinks = mobileMenu.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        body.classList.remove('overflow-hidden');
        setMenuIcon(false);
      });
    });
  }
  
  // Navbar Scroll Behavior
  window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
      navbar.classList.add('py-2');
      navbar.classList.remove('py-4');
    } else {
      navbar.classList.add('py-4');
      navbar.classList.remove('py-2');
    }
  });
})();
