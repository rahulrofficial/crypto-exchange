document.addEventListener("DOMContentLoaded", function (event) {
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  if (document.querySelector("#all_orders_div")) {
    const all_order_buttons = document.querySelectorAll("#all_order_button");

    all_order_buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
        fetch(`/order_deal/${event.target.dataset.action}`, {
          method: "POST",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          body: JSON.stringify({
            id: event.target.dataset.order_id,
            owner: event.target.dataset.owner,
          }),
        })
          .then((response) => response.json())
          .then((reply) => {
            if (reply.status == "true") {
              window.open("wallet", "_self");
              document.querySelector("#message_display").style.display =
                "block";
              document.querySelector("#message_content").innerHTML =
                reply.message;
            } else {
              document.querySelector("#message_display").style.display =
                "block";
              document.querySelector("#message_content").innerHTML =
                reply.message;
            }
          });
      });
    });
  }

  if (document.querySelector("#my_orders_div")) {
    const my_order_buttons = document.querySelectorAll("#my_order_button");
    my_order_buttons.forEach((button) => {
      button.addEventListener("click", (event) => {
        fetch(`/order_deal/close`, {
          method: "POST",
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          body: JSON.stringify({
            id: event.target.dataset.order_id,
            owner: event.target.dataset.owner,
          }),
        })
          .then((response) => response.json())
          .then((reply) => {
            if (reply.status == "true") {
              window.open("my_orders", "_self");
            } else {
              document.querySelector("#message_display").style.display =
                "block";
              document.querySelector("#message_content").innerHTML =
                reply.message;
            }
          });
      });
    });
  }

  if (document.querySelector("#create_orders_div")) {
    var submit_btn = document.querySelector("#create_order_btn");
    document
      .querySelector("#order_radio_btn_0")
      .addEventListener("click", () => {
        document.querySelector("#create_orders_div").className = "bg-success";
        submit_btn.value = "Create Buy Order";
      });

    document
      .querySelector("#order_radio_btn_1")
      .addEventListener("click", () => {
        document.querySelector("#create_orders_div").className = "bg-danger";
        submit_btn.value = "Create Sell Order";
      });
  }

  if (document.querySelector("#buy_sell_div")) {
    var submit_btn = document.querySelector("#buy_sell_submit");
    document
      .querySelector("#buy_sell_radio_btn_0")
      .addEventListener("click", () => {
        document.querySelector("#buy_sell_div").className = "bg-success";
        submit_btn.value = "Buy";
      });

    document
      .querySelector("#buy_sell_radio_btn_1")
      .addEventListener("click", () => {
        document.querySelector("#buy_sell_div").className = "bg-danger";
        submit_btn.value = "Sell";
      });
  }

  if (document.querySelector("#markets_div")) {
    document.querySelector(`#market_current_price_usd`).innerHTML = `1.000000`;
    function update_market_price() {
      fetch(`https://api.coincap.io/v2/assets`)
        .then((response) => response.json())
        .then((data) => {
          data.data.forEach((coin) => {
            let price = parseFloat(coin.priceUsd);

            if (document.querySelector(`#market_current_price_${coin.id}`)) {
              let prev_value = parseFloat(
                document.querySelector(`#market_current_price_${coin.id}`)
                  .innerHTML
              );
              if (prev_value < price) {
                document.querySelector(
                  `#market_current_price_${coin.id}`
                ).style.color = "green";
              } else {
                document.querySelector(
                  `#market_current_price_${coin.id}`
                ).style.color = "red";
              }
              document.querySelector(
                `#market_current_price_${coin.id}`
              ).innerHTML = `${price.toFixed(9)}`;
            }
          });
        });
    }

    setInterval(update_market_price, 2000);
  }

  if (document.querySelector("#index_div")) {
    function update_market_price() {
      fetch(`https://api.coincap.io/v2/assets?limit=10`)
        .then((response) => response.json())
        .then((data) => {
          data.data.forEach((coin) => {
            let price = parseFloat(coin.priceUsd);

            if (document.querySelector(`#index_price_${coin.id}`)) {
              let prev_value = parseFloat(
                document.querySelector(`#index_price_${coin.id}`).innerHTML
              );

              if (prev_value < price) {
                document.querySelector(`#index_price_${coin.id}`).style.color =
                  "green";
              } else {
                document.querySelector(`#index_price_${coin.id}`).style.color =
                  "red";
              }
              document.querySelector(
                `#index_price_${coin.id}`
              ).innerHTML = `${price.toFixed(8)}`;
            }
          });
        });
    }

    setInterval(update_market_price, 1000);
  }

  if (document.querySelector("#wallet_div")) {
    function update_market_price() {
      fetch(`https://api.coincap.io/v2/assets`)
        .then((response) => response.json())
        .then((data) => {
          data.data.forEach((coin) => {
            let usd_price = parseFloat(coin.priceUsd);

            if (
              document.querySelector(`#wallet_current_total_amount_${coin.id}`)
            ) {
              let coin_amount = parseFloat(
                document.querySelector(
                  `#wallet_current_total_amount_${coin.id}`
                ).dataset.amount
              );
              let prev_value = parseFloat(
                document.querySelector(
                  `#wallet_current_total_amount_${coin.id}`
                ).innerHTML
              );
              price = usd_price * coin_amount;
              if (prev_value < price) {
                document.querySelector(
                  `#wallet_current_total_amount_${coin.id}`
                ).style.color = "green";
              } else {
                document.querySelector(
                  `#wallet_current_total_amount_${coin.id}`
                ).style.color = "red";
              }
              document.querySelector(
                `#wallet_current_total_amount_${coin.id}`
              ).innerHTML = `${price.toFixed(6)}`;
            }
          });
        });
    }

    setInterval(update_market_price, 2000);
  }
});
