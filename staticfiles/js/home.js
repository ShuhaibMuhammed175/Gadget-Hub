document.addEventListener('DOMContentLoaded', (e) => {
    const wishlistButtons = document.querySelectorAll('.wishlist-button');
    const productIds = document.querySelectorAll('.product-id');
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    wishlistButtons.forEach((wishlistbutton, index) => {
        wishlistbutton.addEventListener ( 'click', () => {
        const product_id = productIds[index].value
        let postObj = {
            pdt_id : product_id,
            tkn : token
        }

        console.log(postObj)
        fetch('/wishlist/', {
            method: 'POST',
            credentials: 'same-origin',
            headers : {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': token,
            },
            body: JSON.stringify(postObj)
        }).then(response => {
            return response.json();
        }).then(data => {
            alert(data['status'])
        })
        }
    )
    })
})

