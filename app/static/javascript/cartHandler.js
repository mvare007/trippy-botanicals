(function () {
  const cartBtn = document.getElementById("cart");
  if (!cartBtn) return;

  const productOrderBtns = document.querySelectorAll(".add-product-to-cart");

  productOrderBtns.forEach((btn) => {
    btn.addEventListener("click", (_event) => {
      let productId = btn.previousElementSibling.value;

      addProductToCart(productId);
    });
  });

  async function addProductToCart(productId) {
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
      console.log("Product added to cart!");
      document.dispatchEvent(new Event("cartChanged"));
    } else {
      console.error("Oops! Something went wrong. Please try again.");
      console.table(response);
    }
  }

  async function createOrder() {
    const response = await fetch("/orders", {
      method: "POST",
    });

    const data = await response.json();
    if (response.ok) {
      document.getElementById("current-order-id").value = data.id;
    } else {
      alert("Oops! Something went wrong. Please try again.");
    }
  }

  function getCurrentOrderId() {
    let currentOrderId = document.getElementById("current-order-id").value;
    if (!currentOrderId) {
      currentOrderId = createOrder()["id"];
    }

    return currentOrderId;
  }
})();
