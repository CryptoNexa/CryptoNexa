// const openModalButtons = document.querySelectorAll('[data-modal-target]')
// const closeModalButtons = document.querySelectorAll('[data-close-button]')
// const overlay = document.getElementById('overlay')
//
// openModalButtons.forEach(button => {
//     button.addEventListener('click',() => {
//         console.log("hellllllll")
//         const modal = document.querySelector(button.dataset.modalTarget)
//         openModal(modal)
//     })
// })
//
// closeModalButtons.forEach(button => {
//     button.addEventListener('click', () => {
//         const modal = button.closest('.modal')
//         closeModal(modal)
//     })
// })
//
// function openModal(modal){
//     console.log("hello")
//     if(modal == null) return
//     modal.classList.add('active')
//     // overlay.classList.add('active')
// }
//
// function closeModal(modal) {
//     if(modal == null) return
//     modal.classList.remove('active')
//     // overlay.classList.remove('active')
// }


document.querySelector(".close").addEventListener("click", function () {
    document.querySelector('.popup').classList.remove('active');
});

document.getElementById("loginButton").addEventListener("click", function () {
    document.querySelector('.popup').classList.add('active');
});

// // Close the popup if the user clicks outside the popup
// document.querySelector('.popup').addEventListener("click", function (event) {
//     if (event.target === document.querySelector('.popup')) {
//         document.querySelector('.popup').classList.remove('active');
//     }
// });

// Prevent clicks inside the popup from closing it
document.querySelector('.popup > div').addEventListener("click", function (event) {
    event.stopPropagation();
});
