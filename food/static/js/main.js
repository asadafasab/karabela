document.addEventListener('DOMContentLoaded', () => {
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0)
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target
                const $target = document.getElementById(target)

                el.classList.toggle('is-active')
                $target.classList.toggle('is-active')

            })
        })
    }
    const popUp = document.querySelectorAll("#add-new-dish")[0]
    const hide = document.querySelectorAll("#hide-popup-btn")[0]
    const addNewDish = document.querySelectorAll("#add-new-dish-btn")[0]
    if (addNewDish) {
        addNewDish.addEventListener('click', () => {
            popUp.classList.toggle("hide")
        })
        hide.addEventListener('click', () => {
            popUp.classList.toggle("hide")
        })
    }

    const rec = document.querySelectorAll("#recomend-btn")[0]
    const dontRec = document.querySelectorAll("#dont-recomend-btn")[0]
    const check = document.querySelectorAll("#id_recommendation")[0]
    if (rec) {
        rec.addEventListener('click', () => {
            rec.classList.toggle("is-primary")
            dontRec.classList.remove("is-primary")
            check.checked = !check.checked
        })
        dontRec.addEventListener('click', () => {
            dontRec.classList.toggle("is-primary")
            rec.classList.remove("is-primary")
            check.checked = false
        })
    }
    const score_form = document.querySelectorAll("#id_score")[0]
    const score_star_btns = document.querySelectorAll("#all-star-btn")
    score_star_btns.forEach((el, idx, arr) => {
        el.addEventListener('click', () => {
            score_form.value = idx + 1
            score_star_btns.forEach(el => {
                el.classList.remove("fas")
                el.classList.add("far")
            })
            for (let i = 0; i <= idx; i++) {
                score_star_btns[i].classList.toggle("fas")
            }
        })
    })
    if (window.location.pathname == "/cart") {
        const loadingBtn = document.querySelectorAll("#loading-btn")[0]
        let cart = window.sessionStorage.getItem("cart")
        const url = window.location.href.replace("cart", "get-cart")

        if (checkIfObjectEmpty(cart)) {
            sendData(url, { cart: JSON.parse(cart) }).then(res => {
                if (res) {
                    let total = 0.0
                    for (const property in res) {
                        addProductsCart(property, res)
                        total += (res[property].price * res[property].quantity)
                    }
                    setTotalPrice(total.toFixed(2))
                    if (total > 0.0) {
                        loadingBtn.classList.toggle("hide")
                        document.querySelectorAll("#cart-table")[0].classList.toggle("hide")
                    } else {
                        loadingBtn.classList.toggle("is-loading")
                    }
                } else {
                    loadingBtn.classList.toggle("is-loading")
                }
            })
        } else {
            loadingBtn.classList.toggle("is-loading")
        }
    }
    if (window.location.pathname == "/address") {
        const dishesInp = document.querySelectorAll("#id_dishes")[0]
        dishesInp.value = getProducts()
    }

})

let sendData = (url, data) => {
    const csrftoken = csrfToken()

    return fetch(url, {
        method: "POST",
        mode: 'same-origin',
        headers: {
            "Content-Type": "application/json",
            'X-Requested-With': 'XMLHttpRequest',
            "X-CSRFToken": csrftoken
        },
        body: JSON.stringify(data)
    }).then(res => res.json())
}

let setTotalPrice = (total) => {
    let node = document.getElementById("cart-total-price")
    node.innerHTML = total + " PLN"
}
let addProductsCart = (property, dishes) => {
    let tbody = document.getElementById("tbody")
    let tr = document.createElement("tr")
    tbody.appendChild(tr)

    let td = document.createElement("td")
    let image = document.createElement("img")
    td.appendChild(image)
    tr.appendChild(td)
    image.classList.add("round")
    image.classList.add("cart-preview")
    image.src = dishes[property].photo

    let name = document.createElement("td")
    let link = document.createElement("a")
    link.href = "/dish/" + dishes[property].id
    link.innerHTML = dishes[property].name
    name.appendChild(link)
    tr.appendChild(name)

    let price = document.createElement("td")
    price.innerHTML = dishes[property].price + " PLN"
    tr.appendChild(price)

    let quantity = document.createElement("td")
    quantity.innerHTML = dishes[property].quantity
    tr.appendChild(quantity)

    td = document.createElement("td")
    let deleteBtn = document.createElement("button")
    deleteBtn.classList.add("button")
    deleteBtn.addEventListener('click', () => {
        deteteFromStorage(property)
    })
    let i = document.createElement("i")
    i.classList.add("fas")
    i.classList.add("fa-trash")
    deleteBtn.appendChild(i)
    td.appendChild(deleteBtn)
    tr.appendChild(td)
}

let deteteFromStorage = (num) => {
    let cart = window.sessionStorage.getItem("cart")
    cart = JSON.parse(cart)
    delete cart["" + num]
    window.sessionStorage.setItem("cart", JSON.stringify(cart))
    window.location.reload();
}

let csrfToken = () => {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];
}

let changeQuantity = (change) => {
    let val = parseInt(inputQuantity.value)
    val += parseInt(change)
    if (val <= 63 & val >= 1) {
        inputQuantity.value = val
    }
}

let deleteDish = (id) => {
    if (confirm('Are you sure you want to delete this dish?')) {
        window.location.assign("/remove/d/" + id)
    }
}
let deleteRestaurant = (id) => {
    if (confirm('Are you sure you want to delete this restaurant?')) {
        window.location.assign("/remove/r/" + id)
    }
}

let addToCart = (product) => {
    let quantity = document.querySelectorAll("#inputQuantity")[0]
    quantity = parseInt(quantity.value)
    let cart = window.sessionStorage.getItem("cart")
    if (checkIfObjectEmpty(cart)) {
        cart = JSON.parse(cart)
        if (product in cart) {
            cart[product] += quantity
        } else {
            cart[product] = quantity
        }
    } else {

        cart = {}
        cart[product] = quantity
    }
    window.sessionStorage.setItem("cart", JSON.stringify(cart))
    alert("Added")
}

let getProducts = () => {
    return window.sessionStorage.getItem("cart")
}
let clearStorage = () => {
    window.sessionStorage.removeItem("cart")
}

let checkIfObjectEmpty = (value) => {
    return value && value !== undefined
}
let setOrderStatus = (order, status) => {
    const url = window.location.href.split("/restaurant")[0] + "/order-status"
    const data = {
        id: order,
        status: status
    }

    sendData(url, data).then(res => {
        if (res && res.ok) {
            alert("Status has been set")
        } else {
            alert("ERROR...")
        }
    })
}