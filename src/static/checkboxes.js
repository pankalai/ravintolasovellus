const dropdownMenu =  document.querySelector('.dropdown-menu'); 
const dropdownButton = document.getElementById('dropdownMenu1'); 
const checkBoxes = document.querySelectorAll('.dropdown-menu input[type="checkbox"]'); 
var lkm = 0

function countSelected() {
    checkBoxes.forEach((checkbox) => { 
        if (checkbox.checked) {
            lkm += 1
        }
    });
    setButtonText();
    
}

function updateCount(event) {
    const checkbox = event.target;
    if (checkbox.checked) { 
        lkm += 1; 
    } else {
        lkm -= 1;
    }
    setButtonText();
}

function setButtonText() {
    text = "Kategoria"
    if (lkm > 0) {
        text +=  " (" + lkm + ")";
    }
    dropdownButton.innerHTML = text + "&ensp;<span class='caret'></span>"
    
}
window.addEventListener('load', countSelected); 
dropdownMenu.addEventListener('change', updateCount);  