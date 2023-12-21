const date1 = document.getElementById("datepicker1");
const date2 = document.getElementById("datepicker2");
const findButton = document.getElementById("find");

const today = new Date().toISOString().split('T')[0];

date1.min = '2023-01-01';
date2.min = '2023-01-01';
date1.max = today;
date2.max = today;

findButton.addEventListener('click', () => {
    if (date2.value < date1.value){
        alert("Debe especificar un intervalo válido de fechas");
    }
})