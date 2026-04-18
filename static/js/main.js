document.addEventListener("DOMContentLoaded", function() {
    // 1. Navbar Scroll Effect
    const navbar = document.querySelector(".navbar");
    
    if (navbar) {
        window.addEventListener("scroll", function() {
            if (window.scrollY > 50) {
                navbar.classList.add("scrolled");
            } else {
                navbar.classList.remove("scrolled");
            }
        });
    }

    // 2. Fade-in Animation on Scroll (Intersection Observer)
    const observerOptions = {
        root: null,
        rootMargin: "0px",
        threshold: 0.1
    };

    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target); // Optional: Stop observing once visible
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll(".fade-in");
    fadeElements.forEach(el => {
        fadeObserver.observe(el);
    });

    // 3. Button Ripple Effect
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            let x = e.clientX - e.target.getBoundingClientRect().left;
            let y = e.clientY - e.target.getBoundingClientRect().top;

            let ripples = document.createElement('span');
            ripples.className = 'ripple-effect';
            ripples.style.left = x + 'px';
            ripples.style.top = y + 'px';
            this.appendChild(ripples);

            setTimeout(() => {
                ripples.remove();
            }, 1000);
        });
    });

    // 4. Form Submit Loading State
    const forms = document.querySelectorAll("form");
    forms.forEach(form => {
        form.addEventListener("submit", function() {
            const submitBtn = form.querySelector("button[type='submit'], input[type='submit']");
            if (submitBtn) {
                // Prevent multiple submissions by slightly dimming and disabling pointer events
                submitBtn.classList.add("loading");
                if (submitBtn.tagName.toLowerCase() === "button") {
                    submitBtn.dataset.originalText = submitBtn.innerHTML;
                    submitBtn.innerHTML = "Processing... <span class='spinner'></span>";
                } else if (submitBtn.tagName.toLowerCase() === "input") {
                    submitBtn.dataset.originalValue = submitBtn.value;
                    submitBtn.value = "Processing...";
                }
            }
        });
    });
});
