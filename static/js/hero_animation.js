/**
 * SAMS Hero Entrance Animations via Web Animations API (WAAPI)
 * Runs once smoothly when the landing page loads.
 */

document.addEventListener('DOMContentLoaded', () => {
  // Check user preference for reduced motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion) {
    return; // Skip animation if reduced motion is preferred
  }

  const logo = document.querySelector('.hero-nav-logo');
  const navPill = document.querySelector('.hero-nav-pill');
  const loginNav = document.querySelector('.hero-nav-login');
  const kicker = document.querySelector('.hero-kicker');
  const headlineLine1 = document.querySelector('.hero-headline-1');
  const headlineLine2 = document.querySelector('.hero-headline-2');
  const subline = document.querySelector('.hero-subline');
  const btnLogin = document.querySelector('.hero-btn-login');
  const btnModules = document.querySelector('.hero-btn-modules');
  const modulesTitle = document.querySelector('.hero-modules-title');
  const modulesLink = document.querySelector('.hero-modules-link');
  const cardAdmin = document.querySelector('.hero-card-admin');
  const cardTeacher = document.querySelector('.hero-card-teacher');
  const cardStudent = document.querySelector('.hero-card-student');

  // Animation helper
  const animateElement = (el, keyframes, options) => {
    if (!el) return;
    return el.animate(keyframes, {
      fill: 'forwards',
      easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
      ...options
    });
  };

  // 1. Logo, Nav Pill, and Login Nav drop in
  const dropNav = [
    { transform: 'translateY(-30px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ];
  animateElement(logo, dropNav, { duration: 700, delay: 100 });
  animateElement(navPill, dropNav, { duration: 750, delay: 150 });
  animateElement(loginNav, dropNav, { duration: 700, delay: 200 });

  // 2. Kicker un-blurs
  animateElement(kicker, [
    { filter: 'blur(14px)', opacity: 0, transform: 'scale(0.96)' },
    { filter: 'blur(0)', opacity: 1, transform: 'scale(1)' }
  ], { duration: 800, delay: 350 });

  // 3. Headline lines spring up out of blur 0.16s apart
  const springUp = [
    { transform: 'translateY(40px)', filter: 'blur(12px)', opacity: 0 },
    { transform: 'translateY(0)', filter: 'blur(0)', opacity: 1 }
  ];
  animateElement(headlineLine1, springUp, { duration: 850, delay: 500 });
  animateElement(headlineLine2, springUp, { duration: 850, delay: 660 }); // +0.16s

  // 4. Subline rises
  animateElement(subline, [
    { transform: 'translateY(25px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ], { duration: 700, delay: 850 });

  // 5. CTA Buttons rise
  const btnRise = [
    { transform: 'translateY(30px) scale(0.95)', opacity: 0 },
    { transform: 'translateY(0) scale(1)', opacity: 1 }
  ];
  animateElement(btnLogin, btnRise, { duration: 650, delay: 950 });
  animateElement(btnModules, btnRise, { duration: 650, delay: 1050 });

  // 6. Modules Title and Link
  const fadeRise = [
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ];
  animateElement(modulesTitle, fadeRise, { duration: 600, delay: 1150 });
  animateElement(modulesLink, fadeRise, { duration: 600, delay: 1200 });

  // 7. Three Cards rise in succession
  const cardRise = [
    { transform: 'translateY(50px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ];
  animateElement(cardAdmin, cardRise, { duration: 750, delay: 1250 });
  animateElement(cardTeacher, cardRise, { duration: 750, delay: 1400 });
  animateElement(cardStudent, cardRise, { duration: 750, delay: 1550 });
});
