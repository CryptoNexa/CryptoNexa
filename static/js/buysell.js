window.addEventListener("DOMContentLoaded", function () {
    var myModal = new bootstrap.Modal(document.getElementById("buysellModal"));
    myModal.show();
});
// config = {
//         enableTime: true,
//         dateFormat: "M. j, Y, h:i K",
//         time_24hr: false
//     }
// flatpickr("#datetime",config)

// function openDatetimePicker() {
//     // Trigger the click event on the datetime input
//     document.getElementById('datetime').click();
// }

function printing() {
    var selectedGender = document.querySelector('input[id="coin"]');
    if (selectedGender) {
        console.log("Selected gender: " + selectedGender.value);
    } else {
        console.log("Please select a gender.");
    }
}

function hideAlert(idh) {
    var alert = document.getElementById(idh);
    alert.style.display = "none";
}

function total_spent_calc() {
    var tot_spt = document.getElementById("id_total_spent");
    var qty = parseFloat(document.getElementById("id_quantity").value);
    var price = parseFloat(document.getElementById("id_price").value);
    var tran_fee = parseFloat(document.getElementById("id_transaction_fee").value);
    // Calculate total spent
    var totalSpent = (qty * price) + tran_fee;

    // Round off to 2 decimal points
    tot_spt.value = totalSpent.toFixed(4);
}