const print = console.log;

const form = document.getElementById("create-concert-form");

function handleFormChange(event) {
  const priceField = document.getElementById("id_ticket_price");
  if (event.target !== priceField) {
    priceField.value = 100;
  }
}

form.addEventListener("change", handleFormChange);
