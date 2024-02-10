document.addEventListener('DOMContentLoaded', (e) => {
    const submit = document.getElementById('form-button')
    const productIds = document.querySelectorAll('.product_id');
    const quantity = document.querySelectorAll('.quantity');
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value

    submit.addEventListener('click', (event) => {
    event.preventDefault();
    let productIdArray = [];
    let quantitiesArray = [];

    productIds.forEach((input) => {
        productIdArray.push(input.value);
    });

    quantity.forEach((input) => {
        quantitiesArray.push(input.value);
    });



    let postObj = {
        product_ids: productIdArray,
        quantities: quantitiesArray,
        token: token,
    };

    console.log(postObj)

    fetch('/order_update/', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': token,
        },
        body: JSON.stringify(postObj),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
        window.location.href = '/';
    })
});
})
