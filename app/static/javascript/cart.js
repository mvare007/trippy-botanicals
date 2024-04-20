(function () {
  const cartBtn = document.getElementById("cart");
  if (!cartBtn) return;

  bindClickListenerToCartBtn();
  bindEventListenerToCartChangedEvent()

  function bindEventListenerToCartChangedEvent() {
    document.addEventListener("cartChanged", () => {
      updateCartItemsCount();
    });
    document.dispatchEvent(new Event("cartChanged"));
  }

  function bindClickListenerToCartBtn() {
    cartBtn.addEventListener("click", (event) => {
      event.preventDefault();
      displayCart();
    });
  }

  async function displayCart() {
    const response = await fetch("/current_order", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();

    if (response.ok) {
      appendOrderItems(data);
    } else {
      alert("Oops! Something went wrong. Please try again.");
    }
  }

  function appendOrderItems(orderData) {
    const { order, total } = orderData;

    const cartTableBody = document.getElementById("cart-table-body");
    cartTableBody.innerHTML = "";

    order.items.forEach((item) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
									<td>${item.product.name}</td>
									<td>${item.product.price} €</td>
									<td>${item.quantity}</td>
									<td><button class="rounded-circle bg-danger delete-order-item" data-order-item-id="${item.id}">X</button></td>
								`;

      cartTableBody.appendChild(tr);
    });

    const cartTotal = document.getElementById("cart-total");
    cartTotal.innerText = total + " €";

    bindClickListenerToDeleteOrderItemBtn();
  }

  function bindClickListenerToDeleteOrderItemBtn() {
    const deleteButtons = document.querySelectorAll(".delete-order-item");
    deleteButtons.forEach((button) => {
      const orderItemId = button.getAttribute("data-order-item-id");

      button.addEventListener("click", (event) => {
        deleteOrderIem(orderItemId);
      });
    });
  }

  async function deleteOrderIem(orderItemId) {
    const response = await fetch(`/order_items/${orderItemId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.ok) {
      displayCart();
      document.dispatchEvent(new Event("cartChanged"));
    } else {
      alert("Oops! Something went wrong. Please try again.");
    }
  }

  async function updateCartItemsCount() {
    const response = await fetch("/current_order/items_count", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();

    if (response.ok) {
      appendOrderItemsCount(data);
    } else {
      alert("Oops! Something went wrong. Please try again.");
    }
  }

  function appendOrderItemsCount(data) {
    const cartItemsCount = document.getElementById("cart-items-count");
    cartItemsCount.innerText = data.items_count;
  }
})();
