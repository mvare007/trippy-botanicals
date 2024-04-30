(function () {
  const cartBtn = document.getElementById("cart");
  const currentOrderHiddenInput = document.getElementById("current-order-id")
  const productOrderBtns = document.querySelectorAll(".add-product-to-cart");
  disableProductOrderBtns(true) // Disable product order buttons if the user isn't logged in
  if (!cartBtn) return;

  productOrderBtns.forEach((btn) => {
    btn.addEventListener("click", (_event) => {
      let productId = btn.previousElementSibling.value;

      addProductToCart(productId);
    });
  });

  function disableProductOrderBtns(removeInnerText = false) {
    if (!currentOrderHiddenInput) {
      productOrderBtns.forEach((btn) => {
        btn.disabled = true;
        if (removeInnerText) {
          btn.innerHTML = null;

        }
      });
    }
  }

  function enableProductOrderBtns() {
    productOrderBtns.forEach((btn) => {
      btn.disabled = false;
    });
  }

  async function addProductToCart(productId) {
    disableProductOrderBtns();
    const currentOrderId = getCurrentOrderId();
    const response = await fetch(
      `/orders/${currentOrderId}/update?product_id=${productId}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          product_id: productId,
        }),
      }
    );

    if (response.ok) {
      document.dispatchEvent(new Event("cartChanged"));
    } else {
      console.error("Oops! Something went wrong. Please try again.");
      console.table(response);
    }
    sleep(5000).then(() => enableProductOrderBtns());
  }

  async function createOrder() {
    const response = await fetch("/orders", {
      method: "POST",
    });

    const data = await response.json();
    if (response.ok) {
      currentOrderHiddenInput.value = data.id;
    } else {
      alert("Oops! Something went wrong. Please try again.");
    }
  }

  function getCurrentOrderId() {
    let currentOrderId = currentOrderHiddenInput.value;
    if (!currentOrderId) {
      currentOrderId = createOrder()["id"];
    }

    return currentOrderId;
  }
})();
