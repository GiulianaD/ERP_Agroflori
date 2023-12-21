let quantityInputs = document.getElementsByClassName("quantity-class");
let souvenirTypeInputs = document.getElementsByClassName("souvenir-type-class");
let amountInputs = document.getElementsByClassName("amount-input-class");
let totalAmountInput = document.getElementById('amount-input-id');

Array.from(quantityInputs).forEach(element => {
    element.addEventListener('input', (event) => {
        updateAmount(event, "-quantity");
    });
});

Array.from(souvenirTypeInputs).forEach(element => {
    element.addEventListener('change', (event) => {
        updateAmount(event, "-souvenir-type");
    });
});


function updateAmount(event, sufix) {
    let id = event.target.id;
    let prefix = id.slice(0, -sufix.length); 
    let quantity = document.getElementById(prefix + "-quantity").value;   
    let amount_element_id = prefix + "-amount";
    let amount_element = document.getElementById(amount_element_id);
    let category = document.getElementById( prefix + "-souvenir-type");
    var selectedOption = category.options[category.selectedIndex];
    let unitary_price = selectedOption.text.split(':')[1];
    amount = unitary_price * quantity;
    amount_element.value = amount;

    var total = 0;
    Array.from(amountInputs).forEach(element => {
        total = total + parseFloat(element.value);
    });
    totalAmountInput.value = total;

}