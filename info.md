In a README.md in your project’s main directory, include a writeup describing your project, and specifically your file MUST include all of the following:
Under its own header within the README called Distinctiveness and Complexity: Why you believe your project satisfies the distinctiveness and complexity requirements, mentioned above.
What’s contained in each file you created.
How to run your application.
Any other additional information the staff should know about your project.

Write a detailed README.md file about my project "Crypto Currency Exchange" which includes live coin prices (powered by coincap.io api) of over 100 coins and also shows each coins price history using line graph.The prices of the coins in this project updates live when there is a price change in coin value.Project also includes the following functions : index :which shows live prices of top 10 crypto currency.



Profile: Show users profile details such as email,firstname,lastname,profile pic url and also provides edit option
view_coin-Shows selected coin history(in periods-1day,12hour,6hour,2hour,1hour,30minutes,15minutes,5minutes,1minute) using plotly line graph,curent live price,supply,max supply,market capital,volume change/24hr also we can add/remove the coin from watchlist
markets-which show live prices of 100s of coins with the ability to add/remove watchlist
deposit-function enables to deposit USD so that the users can purchase crypto using USD
wallet-This is a multi-currency wallet.which stores the user's coins and shows their current amount and value in usd
buy/sell-user can purchase or sell crypto from the exchange at the current market price (using coincap api)
history-shows users purchase,sell,transfer and received history in reverse chronological order
transfer-Enables user to transfer their crypto to any other user
watchlist-shows watchlisted coins and their current prices
create_order-The User can create buy_order/sell_order using the window so that any other user can fulfill that order.It temporarly freexes the order amount so that when another user buy/sell from this order it fulfills instantly
myorder-show users orders which includes both current and fulfilled orders.User can close an active order from the window.When a user closes their oder the freezed amount returns back to their wallet.
allorders-shows all cureent active orders except the current user.The user can do the appropriate action(buy/sell) on these orders.

also project uses apis for the smooth functioning of website
coincap api-Its the backbone of crypto information in this project which gives current coin price,coin details and price history
order_deal-which helps the user to buy,sell or close an order using javascript
info-which gives information about listed coins,wallets and amounts and contents of watchlist
coin_data-which retruns current coins data
price_history-formats the data from coin cap api price history and feeds to plotly.js from live price graph 