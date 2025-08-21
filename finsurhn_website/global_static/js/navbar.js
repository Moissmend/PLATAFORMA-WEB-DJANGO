document.addEventListener("DOMContentLoaded", () => {
  const hamburger = document.getElementById("hamburger");
  const navLinks = document.getElementById("navLinks");
  const infobar = document.getElementById("infobar");

  let isMenuOpen = false;

  hamburger.addEventListener("click", () => {
    isMenuOpen = !isMenuOpen;
    if (isMenuOpen) {
      navLinks.classList.add("active");
      hamburger.innerHTML = `<svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M18 6L6 18M6 6L18 18"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>`;
    } else {
      navLinks.classList.remove("active");
      hamburger.innerHTML = `<svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M4 6H20M4 12H20M4 18H20"
                stroke="currentColor"
                strokeWidth="2"
              />
            </svg>`;
    }
  });

  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      infobar.classList.add("infobarHidden");
      if (isMenuOpen) {
        isMenuOpen = false;
        navLinks.classList.remove("active");
        hamburger.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 6H20M4 12H20M4 18H20" stroke="currentColor" stroke-width="2"/>
            </svg>
            `;
      }
    }else{
        infobar.classList.remove('infobarHidden');
    }
  });
  
});
