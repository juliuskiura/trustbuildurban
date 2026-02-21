// Navbar scroll behavior
(function() {
  'use strict';
  
  const path = window.location.pathname;
  const navbar = document.getElementById('navbar');
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const logo = navbar.querySelector('.trustbuildurban-logo');
  const tagline = navbar.querySelector('.trustbuildurban-tagline');
  const links = navbar.querySelectorAll('.trustbuildurban-link');
  const icon = navbar.querySelector('.trustbuildurban-icon');
  
  let isMobileMenuOpen = false;
  
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      isMobileMenuOpen = !isMobileMenuOpen;
      mobileMenu.classList.toggle('hidden', !isMobileMenuOpen);
      
      if (isMobileMenuOpen) {
        icon.innerHTML = '<path d="M18 6 6 18"></path><path d="m6 6 12 12"></path>';
      } else {
        icon.innerHTML = '<path d="M4 5h16"></path><path d="M4 12h16"></path><path d="M4 19h16"></path>';
      }
    });
  }
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      if(path === '/') {
        navbar.classList.remove('bg-transparent', 'py-6');
        navbar.classList.add('bg-primary', 'shadow-md', 'py-4');
      }else{
        navbar.classList.remove('bg-primary', 'py-6');
        navbar.classList.add('bg-primary', 'shadow-md', 'py-4');
      }          
      
      logo.classList.remove('text-white');
      logo.classList.add('text-navy');
      tagline.classList.remove('text-white/80');
      tagline.classList.add('text-gray-500');
      links.forEach(link => {
        link.classList.add('text-navy', 'hover:text-gray-600');
      });
      icon.classList.remove('text-white');
      icon.classList.add('text-navy');
    } else {
      if(path === '/') {
        navbar.classList.add('bg-transparent', 'py-6');
        navbar.classList.remove('bg-white', 'shadow-md', 'py-4');
      }else{
        navbar.classList.add('bg-primary', 'py-6');
        navbar.classList.remove('bg-white', 'shadow-md', 'py-4');
      }
      
      
      logo.classList.add('text-white');
      logo.classList.remove('text-navy');
      tagline.classList.add('text-white/80');
      tagline.classList.remove('text-gray-500');
      links.forEach(link => {
        link.classList.add('text-white', 'hover:text-navy');
        link.classList.remove('text-navy', 'hover:text-gray-600');
      });
      icon.classList.add('text-white');
      icon.classList.remove('text-navy');
    }
  });
})();
