document.addEventListener('DOMContentLoaded', function () {
    var form = document.querySelector('form');
    var loader = document.getElementById('loader');
    var loginButton = document.getElementById('login-button');

    // Function to show the loader and hide the login button
    function showLoader() {
        if (loader && loginButton) {
            loader.style.display = 'block';
            loginButton.style.display = 'none';
        }
    }

    // Function to hide the loader and show the login button
    function hideLoader() {
        if (loader && loginButton) {
            loader.style.display = 'none';
            loginButton.style.display = 'block';
        }
    }

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the form from submitting for this example
            showLoader();

            // Simulate a successful or failed login
            setTimeout(function () {
                // Simulate a successful login (replace with your actual success logic)
                hideLoader();
                alert('Successful login'); // Replace with your actual success handling
            }, 3000);

            setTimeout(function () {
                // Simulate an error (replace with your actual error handling)
                hideLoader();
                alert('Error occurred during login'); // Replace with your actual error handling
            }, 5000);
        });
    }
});
