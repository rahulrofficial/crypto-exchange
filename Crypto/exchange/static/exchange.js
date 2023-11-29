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
		var current_price_span = document.querySelector("#buy_sell_current_price");
		var coin_list = document.querySelector("#id_coins");
		id_amount = document.querySelector("#id_amount");
		fetch("/info/list_coin")
			.then((response) => response.json())
			.then((list_coin) => {
				function value_fetcher(crypto_coin_name) {
					
					current_price_span.innerHTML = "";

					document.querySelector("#exp_amount").innerHTML = "";
					fetch("/info/wallet")
						.then((response) => response.json())
						.then((data) => {
							//eg.bitcoin for api searching
							if (crypto_coin_name)
								document
									.querySelector("#buy_sell_radio_btn_0")
									.addEventListener("click", () => {
										document.querySelector("#buy_sell_div").className =
											"bg-success";
										submit_btn.value = "Buy";

										if (data.wallet.all_coins.includes("usd")) {
											var rpt1 = setInterval(() => {
												crypto_coin_name = list_coin.all_coins[coin_list.value];

												fetch(
													`https://api.coincap.io/v2/assets/${crypto_coin_name}`
												)
													.then((response) => response.json())
													.then((coin_data) => {
														var amount_val = id_amount.value;
														if (!amount_val) {
															amount_val = 0;
														}
														req_amount =
															parseFloat(coin_data.data.priceUsd) *
															parseFloat(amount_val);
														current_price_span.innerHTML = `Current ${crypto_coin_name} price:$ ${parseFloat(
															coin_data.data.priceUsd
														).toFixed(4)}  Available ${"usd"}: ${parseFloat(
															data.wallet.wallet["usd"]
														).toFixed(4)}`;
														document.querySelector(
															"#exp_amount"
														).innerHTML = `Required amount: $${req_amount.toFixed(
															4
														)}`;
													});
											}, 2000);
											document
												.querySelector("#buy_sell_radio_btn_1")
												.addEventListener("click", () => {
													clearInterval(rpt1);
												});
										} else {
											current_price_span.innerHTML = `Deposit USD and Create a wallet`;
										}
									});

							document
								.querySelector("#buy_sell_radio_btn_1")
								.addEventListener("click", () => {
									document.querySelector("#buy_sell_div").className =
										"bg-danger";
									submit_btn.value = "Sell";

									if (
										data.wallet.all_coins.includes(
											list_coin.all_coins[coin_list.value]
										)
									) {
										function repeat2() {
											crypto_coin_name = list_coin.all_coins[coin_list.value];

											fetch(
												`https://api.coincap.io/v2/assets/${crypto_coin_name}`
											)
												.then((response) => response.json())
												.then((coin_data) => {
													var amount_val = id_amount.value;
													if (!amount_val) {
														amount_val = 0;
													}
													exp_amount =
														parseFloat(coin_data.data.priceUsd) *
														parseFloat(amount_val);
													exp_amount = exp_amount.toFixed(4);
													exp_amount = `Expected amount: $${exp_amount}`;
													if (
														amount_val >
														data.wallet.wallet[
														list_coin.all_coins[coin_list.value]
														]
													) {
														exp_amount = "Not enough Coins";
													}
													current_price_span.innerHTML = `Current ${crypto_coin_name} price:$ ${parseFloat(
														coin_data.data.priceUsd
													).toFixed(
														4
													)}  Available ${crypto_coin_name}: ${parseFloat(
														data.wallet.wallet[crypto_coin_name]
													).toFixed(4)}`;

													document.querySelector(
														"#exp_amount"
													).innerHTML = `${exp_amount}`;
												});
										}
										const rpt2 = setInterval(repeat2, 2000);
										document
											.querySelector("#buy_sell_radio_btn_0")
											.addEventListener("click", () => {
												clearInterval(rpt2);
											});
									} else {
										current_price_span.innerHTML = `Please Buy ${crypto_coin_name} and Create a wallet`;
									}
								});
						});
				}

				id_amount.addEventListener("change", () => {
					value_fetcher(list_coin.all_coins[coin_list.value]);
				});

				coin_list.addEventListener("change", () => {
					value_fetcher(list_coin.all_coins[coin_list.value]);
				});
				value_fetcher(list_coin.all_coins[coin_list.value]);
			});
	}

	if (document.querySelector("#markets_div")) {
		if (document.querySelector(`#market_current_price_usd`)) {
			document.querySelector(
				`#market_current_price_usd`
			).innerHTML = `1.000000`;
		}

		fetch("/info/list_coin")
			.then((response) => response.json())
			.then((data) => {
				var coins = data.coins.join(",");

				function update_market_price() {
					fetch(`https://api.coincap.io/v2/assets?ids=${coins}`)
						.then((response) => response.json())
						.then((data) => {
							data.data.forEach((coin) => {
								let price = parseFloat(coin.priceUsd);

								if (
									document.querySelector(`#market_current_price_${coin.id}`)
								) {
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
			});
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
		fetch("/info/wallet")
			.then((response) => response.json())
			.then((data) => {
				var coins = data.wallet.crypto.join(",");
				
				function update_market_price() {
					fetch(`https://api.coincap.io/v2/assets?ids=${coins}`)
						.then((response) => response.json())
						.then((data) => {
							data.data.forEach((coin) => {
								let usd_price = parseFloat(coin.priceUsd);

								if (
									document.querySelector(
										`#wallet_current_total_amount_${coin.id}`
									)
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
			});
	}
	if (document.querySelector("#view_coin_div")) {
		const coin_id = document.querySelector("#view_coin_id");
		const coin_price = document.querySelector("#view_coin_price");
		const view_market_cap = document.querySelector("#view_market_cap");
		view_volume_24h = document.querySelector("#view_volume_24h");
		view_change_24 = document.querySelector("#view_change_24");
		view_supply = document.querySelector("#view_supply");
		view_maxsupply = document.querySelector("#view_maxsupply");
		view_coin_symbol = document.querySelector("#view_coin_symbol");
		period=document.querySelector("#select_period");
		function graph(){
			fetch(`/price_history/${coin_id.innerHTML}/${period.value}`)
			.then((response) => response.json())
			.then((values) => {
				var xArray = values.time;
				var yArray = values.priceUsd;
				var coin_name=values.name
				// Define Data
				const data = [
					{
						x: xArray,
						y: yArray,
						mode: "lines",
					},
				];

				// Define Layout
				const layout = {autosize: false,
					width: 900,
					height: 600,
					xaxis: { title: "Time" },
					yaxis: { title: "Price" },
					title: `${coin_name} Prices`,
				};

				// Display using Plotly
				Plotly.newPlot("myPlot", data, layout);
			});

		}
		graph()
		period.addEventListener('change',()=>{
			if (timer){
				clearInterval(timer)
			}
			if (period.value=='d1'){
				var time=86400000
			}else if (period.value=='h12'){
				var time=43200000
			}else if (period.value=='h6'){
				var time=21600000
			}else if (period.value=='h2'){
				var time=7200000
			}else if (period.value=='h1'){
				var time=3600000
			}else if (period.value=='m30'){
				var time=1800000
			}else if (period.value=='m15'){
				var time=900000
			}else if (period.value=='m5'){
				var time=300000
			}else if (period.value=='m1'){
				var time=60000
			}
			graph()
			var timer=setInterval(graph,time)
		})
		
		function repeat_view_price() {
			
			fetch(`/coin_data/${coin_id.innerHTML}`)
				.then((response) => response.json())
				.then((coin) => {
					var prev_price = parseFloat(coin_price.innerHTML);
					document.querySelector(
						"#view_coin_name"
					).innerHTML = `${coin.coin.name} Price`;
					view_coin_symbol.innerHTML = coin.coin.symbol;
					view_supply.innerHTML = parseFloat(coin.coin.supply).toFixed(4);
					view_maxsupply.innerHTML = parseFloat(coin.coin.maxSupply).toFixed(4);
					view_market_cap.innerHTML = parseFloat(
						coin.coin.marketCapUsd).toFixed(4);
					view_volume_24h.innerHTML = parseFloat(coin.coin.volumeUsd24Hr).toFixed(4);
					view_change_24.innerHTML = parseFloat(coin.coin.changePercent24Hr).toFixed(4);
					var curent_price = parseFloat(coin.coin.priceUsd).toFixed(8);
					coin_price.innerHTML = curent_price;
					if (curent_price > prev_price) {
						coin_price.style.color = "green";
					} else if (curent_price == prev_price) {
						coin_price.style.color = "black";
					} else {
						coin_price.style.color = "red";
					}
				});
		}

		setInterval(repeat_view_price, 2000);
		
	}

	if (document.querySelector("#watchlist_div")) {
		if (document.querySelector(`#watch_current_price_usd`)) {
			document.querySelector(`#watch_current_price_usd`).innerHTML = `1.000000`;
		}

		fetch("/info/watchlist")
			.then((response) => response.json())
			.then((data) => {
				var coins = data.watchlist.join(",");
				
				function update_market_price() {
					fetch(`https://api.coincap.io/v2/assets?ids=${coins}`)
						.then((response) => response.json())
						.then((data) => {
							data.data.forEach((coin) => {
								let price = parseFloat(coin.priceUsd);

								if (document.querySelector(`#watch_current_price_${coin.id}`)) {
									let prev_value = parseFloat(
										document.querySelector(`#watch_current_price_${coin.id}`)
											.innerHTML
									);
									if (prev_value < price) {
										document.querySelector(
											`#watch_current_price_${coin.id}`
										).style.color = "green";
									} else {
										document.querySelector(
											`#watch_current_price_${coin.id}`
										).style.color = "red";
									}
									document.querySelector(
										`#watch_current_price_${coin.id}`
									).innerHTML = `${price.toFixed(9)}`;
								}
							});
						});
				}

				setInterval(update_market_price, 2000);
			});
	}

	if (document.querySelector("#profile_div")) {
		document
			.querySelector("#profile_edit_btn")
			.addEventListener("click", () => {
				document.querySelector("#profile_edit_form").style.display = "block";
				document.querySelector("#details_display").style.display = "none";
			});
		document
			.querySelector("#profile_submit_btn")
			.addEventListener("click", () => {
				document.querySelector("#profile_edit_form").style.display = "none";
				document.querySelector("#details_display").style.display = "block";
			});
	}

	
});
