document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            let isValid = true;
            
            // Password validation
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            const passwordError = document.getElementById('passwordError');
            
            if (password !== confirmPassword) {
                passwordError.textContent = "Passwords do not match.";
                isValid = false;
            } else if (password.length < 6) {
                passwordError.textContent = "Password must be at least 6 characters.";
                isValid = false;
            } else {
                passwordError.textContent = "";
            }
            
            // Phone validation
            const contact = document.getElementById('contact').value;
            const contactError = document.getElementById('contactError');
            
            if (contact && !/^\+?[\d\s-]{7,15}$/.test(contact)) {
                contactError.textContent = "Please enter a valid phone number.";
                isValid = false;
            } else {
                contactError.textContent = "";
            }
            
            // Email validation
            const email = document.getElementById('email').value;
            const emailError = document.getElementById('emailError');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (!emailRegex.test(email)) {
                emailError.textContent = "Please enter a valid email address.";
                isValid = false;
            } else {
                emailError.textContent = "";
            }
            
            if (!isValid) {
                e.preventDefault(); // Prevent form submission
            }
        });
    }
});
