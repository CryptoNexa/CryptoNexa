document.getElementById('profile-image-input').addEventListener('change', function () {
    const profileImage = document.getElementById('profile-image');
    const selectedImage = this.files[0];
    if (selectedImage) {
        const imageUrl = URL.createObjectURL(selectedImage);
        profileImage.src = imageUrl;
        profileImage.style.objectFit = 'cover';
    }
});