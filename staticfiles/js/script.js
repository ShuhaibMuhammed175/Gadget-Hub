document.addEventListener('DOMContentLoaded', (e) => {
    const btnPlus = document.getElementById('btnPlus')
    const btnMinus = document.getElementById('btnMinus')
    const txtQty = document.getElementById('txtQty')
    const product_id = document.getElementById('product_id').value
    const token = document.querySelector('[name="csrfmiddlewaretoken"]').value
    const addCart = document.getElementById('cartBtn')
    const wishlist = document.getElementById('wishlist')

    btnPlus.addEventListener('click', () => {
        let qty = parseInt(txtQty.value,10)
        qty= isNaN (qty) ? 0 : qty
        if (qty < 10) {
        qty++
        txtQty.value = qty
        }
    })

    btnMinus.addEventListener('click', () => {
        let qty = parseInt(txtQty.value,10)
        qty= isNaN (qty) ? 0 : qty
        if (qty > 1) {
        qty--
        txtQty.value = qty
        }
    })

    addCart.addEventListener('click', () => {
        let qty = parseInt(txtQty.value,10)
        qty= isNaN (qty) ? 0 : qty
        if (qty > 0) {
            let postObj = {
                product_qty : qty,
                pdt_id : product_id,
                tkn : token
            }
            txtQty.value = 1
            fetch('/add_to_cart/', {
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
        else {
            alert('Please Enter the quantity')
        }
    })

    wishlist.addEventListener ( 'click', () => {

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

