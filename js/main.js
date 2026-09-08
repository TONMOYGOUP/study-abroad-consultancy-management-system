/* PVC GLOBAL 2.0 - Shared interactions */

document.addEventListener('DOMContentLoaded', () => {
  const navbar = document.querySelector('.navbar');
  const menuToggle = document.querySelector('.menu-toggle');
  const navContainer = document.querySelector('.nav-container');

  // Dynamic navbar on scroll
  const updateNavbar = () => {
    if (navbar) navbar.classList.toggle('scrolled', window.scrollY > 30);
  };
  updateNavbar();
  window.addEventListener('scroll', updateNavbar, { passive: true });

  // Mobile navigation
  if (menuToggle && navContainer) {
    menuToggle.addEventListener('click', () => {
      navContainer.classList.toggle('menu-open');
      const icon = menuToggle.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-xmark');
      }
    });

    document.querySelectorAll('.nav-menu a').forEach(link => {
      link.addEventListener('click', () => {
        navContainer.classList.remove('menu-open');
        const icon = menuToggle.querySelector('i');
        if (icon) {
          icon.classList.add('fa-bars');
          icon.classList.remove('fa-xmark');
        }
      });
    });
  }

  // FAQ accordion
  document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
      const current = question.closest('.faq-box');
      document.querySelectorAll('.faq-box').forEach(box => {
        if (box !== current) box.classList.remove('active');
      });
      if (current) current.classList.toggle('active');
    });
  });

  // Smooth internal links
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', event => {
      const id = link.getAttribute('href');
      if (!id || id === '#') return;
      const target = document.querySelector(id);
      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Scroll reveal
  const revealItems = document.querySelectorAll('.section, .service-card, .destination-card, .university-card, .process-card, .why-card, .testimonial-card, .faq-box, .contact-info-card');
  revealItems.forEach(item => item.classList.add('reveal'));
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    revealItems.forEach(item => observer.observe(item));
  } else {
    revealItems.forEach(item => item.classList.add('visible'));
  }

  // Demo forms
// Contact form - send data to Flask backend
// Contact form - send data to Flask backend
const contactForm = document.getElementById('contactForm');

if (contactForm) {
  contactForm.addEventListener('submit', async event => {
    event.preventDefault();

    const submitButton = contactForm.querySelector(
      "button[type='submit']"
    );

    submitButton.disabled = true;
    submitButton.textContent = 'Sending...';

const formData = {
  full_name: document.getElementById('contactName').value.trim(),
  email: document.getElementById('contactEmail').value.trim(),
  phone: document.getElementById('contactPhone').value.trim(),
  destination: document.getElementById('destination').value.trim(),
  subject: document.getElementById('subject').value.trim(),
  message: document.getElementById('message').value.trim()
};
    console.log("DATA BEING SENT:", formData);
    try {
      const response = await fetch(
        'http://127.0.0.1:5001/api/contact',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        }
      );

      const result = await response.json();

      if (result.success) {
        alert('✅ ' + result.message);
        contactForm.reset();
      } else {
        alert('❌ ' + result.message);
      }

    } catch (error) {
      console.error('Contact form error:', error);

      alert(
        '❌ Could not connect to the server. Make sure Flask backend is running.'
      );

    } finally {
      submitButton.disabled = false;
      submitButton.textContent = 'Send Message';
    }
  });
}

});

document.addEventListener("DOMContentLoaded", function () {

    const authButtons = document.getElementById("authButtons");

    if (!authButtons) return;

    const storedUser = sessionStorage.getItem("pvc_user");

    if (!storedUser) {
        return;
    }

    try {

        const user = JSON.parse(storedUser);

       authButtons.innerHTML = `
    <a href="account.html" class="user-account">
        <i class="fas fa-user-circle"></i>
        <span>${user.full_name}</span>
    </a>
    ${
    user.role === "admin"
        ? `
            <a href="admin.html">
                <i class="fas fa-user-shield"></i>
                <span>Admin Panel</span>
            </a>
          `
        : ""
}

    ${
        user.role === "admin"
            ? `
                <a href="admin.html" class="btn btn-outline">
                    <i class="fas fa-user-shield"></i>
                    Admin Panel
                </a>
              `
            : ""
    }

    <button
        type="button"
        class="btn btn-outline"
        id="logoutButton"
    >
        Logout
    </button>
`;

        document
            .getElementById("logoutButton")
            .addEventListener("click", function () {

                sessionStorage.removeItem("pvc_user");
                sessionStorage.removeItem("pvc_access_token");

                window.location.href = "index.html";

            });

    } catch (error) {

        console.error(
            "USER DATA ERROR:",
            error
        );

        sessionStorage.removeItem("pvc_user");
    }

});

// =========================================================
// GLOBAL AUTH NAVBAR
// =========================================================

// =========================================================
// GLOBAL AUTH NAVBAR
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    const authButtons =
        document.getElementById("authButtons");

    if (!authButtons) {
        return;
    }


    const storedUser =
        sessionStorage.getItem("pvc_user");


    // =====================================================
    // USER NOT LOGGED IN
    // =====================================================

    if (!storedUser) {

        authButtons.innerHTML = `
            <a
                href="login.html"
                class="btn btn-outline"
            >
                Login
            </a>

            <a
                href="signup.html"
                class="btn btn-primary"
            >
                Get Started
            </a>
        `;

        return;
    }


    // =====================================================
    // USER LOGGED IN
    // =====================================================

    try {

        const user =
            JSON.parse(storedUser);


        authButtons.innerHTML = `
            
            <div class="user-menu">

                <button
                    type="button"
                    class="user-account"
                    id="userMenuButton"
                >

                    <i class="fas fa-user-circle"></i>

                    <span>
                        ${user.full_name}
                    </span>

                    <i class="fas fa-chevron-down"></i>

                </button>


                <div
                    class="user-dropdown"
                    id="userDropdown"
                >

                    <a href="account.html">

                        <i class="fas fa-user"></i>

                        <span>
                            My Account
                        </span>

                    </a>


                    <a href="account.html">

                        <i class="fas fa-id-card"></i>

                        <span>
                            My Profile
                        </span>

                    </a>

                    ${
    user.role === "admin"
        ? `
            <a href="admin.html">

                <i class="fas fa-user-shield"></i>

                <span>
                    Admin Panel
                </span>

            </a>
          `
        : ""
}


                    <button
                        type="button"
                        id="logoutButton"
                    >

                        <i class="fas fa-sign-out-alt"></i>

                        <span>
                            Logout
                        </span>

                    </button>

                </div>

            </div>
        `;


        // =================================================
        // USER MENU
        // =================================================

        const userMenuButton =
            document.getElementById(
                "userMenuButton"
            );

        const userDropdown =
            document.getElementById(
                "userDropdown"
            );


        if (userMenuButton && userDropdown) {

            userMenuButton.addEventListener(
                "click",
                function (event) {

                    event.stopPropagation();

                    userDropdown.classList.toggle(
                        "show"
                    );

                }
            );


            // Close dropdown outside click

            document.addEventListener(
                "click",
                function () {

                    userDropdown.classList.remove(
                        "show"
                    );

                }
            );

        }


        // =================================================
        // LOGOUT
        // =================================================

        const logoutButton =
            document.getElementById(
                "logoutButton"
            );


        if (logoutButton) {

            logoutButton.addEventListener(
                "click",
                function () {

                    sessionStorage.removeItem(
                        "pvc_user"
                    );

                    sessionStorage.removeItem(
                        "pvc_access_token"
                    );

                    window.location.href =
                        "index.html";

                }
            );

        }


    } catch (error) {

        console.error(
            "USER DATA ERROR:",
            error
        );

        sessionStorage.removeItem(
            "pvc_user"
        );

        window.location.href =
            "login.html";
    }

});