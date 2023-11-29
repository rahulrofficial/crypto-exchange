# Crypto Hub - Crypto Currency Exchange

## Table of Contents

- [Introduction](#introduction)
- [Overview of the Project](#overview-of-the-project)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
   - [Distinctiveness](#distinctiveness)
   - [Complexity](#complexity)
- [Features in Detail](#features-in-detail)
   - [APIs Utilized](#apis-utilized)
- [Files Created](#files-created)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)

## Introduction

The Crypto Currency Exchange stands as a dynamic and robust platform, dedicated to providing users with a sophisticated interface for navigating the world of cryptocurrencies. Powered by the CoinCap.io API, this platform brings forth a comprehensive array of functionalities and tools aimed at offering real-time insights, historical data, and user-friendly interactions.This project is a Crypto Currency Exchange platform that provides live coin prices, historical price graphs, user profiles, trading functionalities, and more.

### Overview of the Project

This platform is meticulously designed to cater to both novice and experienced cryptocurrency enthusiasts. The core focus revolves around delivering live updates for over 100 cryptocurrencies, enabling users to monitor and analyze market movements on a granular level. The fusion of live coin prices and historical data visualization empowers users to make informed decisions in their crypto ventures.

## Distinctiveness and Complexity

### Distinctiveness

Our project stands out due to its comprehensive set of features covering live coin prices for over 100 currencies, real-time updates on price changes, user profiles with edit options, a multi-currency wallet, buy/sell functionalities using the CoinCap API, and the ability to create, view, and fulfill orders within the platform.It also helps Peer to Peer Crypto Transfer.

### Complexity

The complexity of the project lies in its varied functionalities:
- **Live Coin Prices** : Utilizes the CoinCap.io API to fetch live prices and updates in real-time.
- **Historical Price Graphs** : Utilizes Plotly.js to display price history in different periods.
- **User Profiles and Wallets** : Manages user details, profile pictures, wallet contents, and their respective values in USD.
- **Trading and Orders** : Implements buying, selling, order creation, fulfilling, and tracking user history.
- **Peer to Peer Crypto Transfer** :It also acts like a multi-crypto currency wallet and allow coin transfers between users.
- **API Integration** : Relies on CoinCap API for live coin data, Custom APIs for trade execution, and additional APIs for user-related information.
- **Extensive Error Checking and Real time result Display** :The Platform automatically checks for user errors and automatically responds to user input in realtime.
- **Single Click Executions** :The User can execute a buy/sell by a single click if they have sufficient funds.

## Features in Detail

- ### Live Coin Prices

   The platform's centerpiece functionality harnesses the CoinCap.io API to provide users with real-time updates on cryptocurrency prices. The continuous updates ensure users stay abreast of market changes, offering an invaluable edge in the volatile world of digital assets.

- ### Historical Price Visualization

   One of the platform's standout features is its ability to showcase detailed price history for each cryptocurrency. Using Plotly.js, this functionality presents historical data in various timeframes—ranging from a day to a minute—enabling users to analyze trends and patterns with precision.

- ### Top 10 Crypto Currency Index

   The index section acts as a quick reference guide, offering a concise view of the top 10 cryptocurrencies. This feature provides immediate insights into the performance of leading digital currencies, aiding users in monitoring market trends efficiently.

- ### Profile Management

   Users have complete control over their profiles within the platform. They can effortlessly view and update personal information, including email, first name, last name, and profile picture URL. This personalized approach ensures user information remains accurate and up-to-date.

- ### Coin Details with view_coin Functionality

   The view_coin feature enhances user experience by offering detailed insights into individual cryptocurrencies. It combines live price updates, supply, maximum supply, market capitalization, volume change in 24 hours, and historical data visualization. Additionally, it allows users to conveniently add or remove coins from their watchlist.

- ### Market Overview: Markets Functionality

   The platform offers a comprehensive market overview, displaying live prices of hundreds of coins. This functionality enables users to easily add or remove coins from their watchlist, fostering a tailored experience based on their preferences.

- ### USD Deposit Functionality

   Users can deposit USD into their accounts, providing them with the means to purchase cryptocurrencies using deposited funds. This feature ensures seamless integration of fiat currency transactions within the platform.

- ### Multi-Currency Wallet: Wallet Functionality

   The multi-currency wallet serves as a secure repository for users' cryptocurrencies. It showcases the current amount and value of the stored coins in USD, allowing users to effectively manage their digital assets.

- ### Buy/Sell Functionality

   The buy/sell feature enables users to engage in cryptocurrency transactions at the current market price. Leveraging the CoinCap API, users can seamlessly execute buy or sell orders based on real-time market valuations.

- ### Transaction History: History Functionality

   The platform meticulously records users' transaction history, providing a chronological account of their purchases, sales, transfers, and receipts. This detailed record ensures transparency and aids users in monitoring their activities within the platform.

- ### Peer-to-Peer Transfers: Transfer Functionality

   Users can initiate direct cryptocurrency transfers to other platform users. This functionality fosters a peer-to-peer exchange ecosystem within the platform, enhancing user interaction and engagement.

- ### Watchlist Management

   The watchlist feature enables users to monitor their preferred coins by listing them in a watchlist. Users can effortlessly track the current prices of these coins, providing a convenient overview of their investment interests.

- ### Order Management: Create Order and My Order Functionalities

   The platform empowers users to create buy or sell orders visible to other users. Additionally, users can manage their active and fulfilled orders, including the ability to close active orders and receive the frozen amount back into their wallets.

- ### Market Orders: All Orders Functionality

   The all orders feature displays all current active orders, except the user's own orders. This functionality allows users to take appropriate actions, such as buying or selling, on these orders.

## APIs Utilized

- ### CoinCap API

   The CoinCap API serves as the backbone of the platform, providing real-time coin prices, coin details, and historical price data. The integration of this API ensures the platform remains up-to-date with accurate cryptocurrency information.

- ### Order_Deal API

   The order_deal API facilitates buying, selling, or closing orders using JavaScript within the platform. This API plays a pivotal role in executing trade orders and ensuring seamless user interactions.

- ### Info API

   The info API serves as an information hub, offering details about listed coins, user wallets, watchlist contents, and relevant amounts. This API supports various functionalities, enhancing user interactions within the platform.

- ### Coin_Data API

   The coin_data API furnishes the platform with current data for listed coins. Its integration ensures users have access to real-time information about cryptocurrencies.

- ### Price_History API

   The price_history API plays a crucial role in formatting data from the CoinCap API's price history and feeding it to Plotly.js for live price graph visualization. This API enhances the platform's ability to present historical price data effectively.

## Files Created

- `views.py`: Contains the main interfaces for the platform-**The Back-end**
   - views.index - Shows top 10 Crypto Currencies and their live prices each second exchange.js does the live updating by utilizing coincap api.
   - views.login_view- Include Login Form.
   - views.logout_view - Used to logout the user.
   - views.register - New User Registration.
   - views.profile - Shows Profile Picture, Email, Joined date, First and Last name and Last Login. User can also edit these data as well as change their password.
   - views.view_coin - Live current prices, Supply, MarketCap, Price History Graph which has intervals of 1day, 12h, 6h, 2h, 1h, 30minutes, 15minutes, 5minutes and 1minute. The plotting of graph is done by Plotly.js and live fetching of data is done by exchange.js 
   - views.markets - Shows live prices of 100+ coins and gives an option to add them/remove them to the watchlist.
   - views.deposit - Helps the user to deposit Fiat Money (USD for now) to their wallet so that they can purchase crypto.
   - views.wallet -A Multi-Currency Wallet: Shows User's Current coins, their amount and their total value in USD
   - views.buy_sell - User can Purchase or Sell their crypto with the exchange at the current market rate.The exchange.js enables live price display of required amount in USD if the user want to purchase a specific crypto or expected money in USD if they wished to sell.
   - views.history - Shows the Users Purchase, Sale, Transfer and Reception of Funds/Coins
   - views.transfer - User can transfer the crypto in their wallet to other users.
   - views.watchlist - Displays user added coins and their current live prices.
   - views.add_watchlist - Add a specific coin to Watchlist.
   - views.remove_watchlist - Remove a specific coin from Watchlist.
   - views.create_orders - User can create buy order if they wish to purchase a particular coin at a specific price or sell a coin at a specific price. The mentioned amount is temporarily transferred to a order wallet
   - views.my_orders - Display User created orders and provision to close them. If they are either closed or fulfilled; it also shows the status.
   - views.all_orders - Displays all current active orders.The user can execute buy/sell action on other user's listed orders and close if the order is listed by the current user. 
   
      **APIs**
   - views.order_deal - Used to Buy,Sell or Close orders using exchange.js
   - views.info - Provides information about current coins listed in exchange,User wallet status and User watchlists
   - views.coin_data - Return details about a specific crypto coin
   - views.price_history - Return Price History details of specific crypto coin on different time intervals

   - database_listed_coins_updater - It does not do anything with the views.If there is no coins listed at the exchange,this function calls the CoinCap Api and list first hundred coins and Buys 1 Million dollar worth of coin for each listed coins.

- `model.py`: Contains the Django Models which deals with different tables in the Database.
   - User - User details such as username,password,email,profile picture url etc.
   - List_Coin - Deals with Details of Listed coins, their attributes such as Title, Symbol, Logo Url, Coin id (for API).
   - Coin - It stores coin and their amount for individual user. 
   - Wallet - Collection of Coins and their User
   - Watchlist - Stores a User's watchlist contains List_Coin objects.
   - History - Stores Users transaction history such as from, to, coin, amount, total amount and status (eg.purchased or sold)
   - Orders - Stores all orders which users created.
   - Order_wallet - A temporary wallet which stores the user's crypto/Money for the successful execution of the created order.It's Instance gets destroyed after transferring the amount to user ( when the order is completed or closed )
- `styles.css`: Stylesheet for the HTML pages.
- `exchange.js`: Handles client-side interactions, including API calls,UI live price updates and rendering Historical price graphs with the help of Plotly.js.It works in conjunction with `views.py`-**The Front-end**

---
## Dependencies

The Crypto Hub - The Crypto Currency Exchange uses the following libraries:

- `Django`: For backend.
- `Javascript`: For Handling client-side interactions and live price updating.
- `Bootstrap.js`: For User Interfaces.
- `Plotly.js`: For rendering Price Line Graph.
- `requests`: For interacting with CoinCap API.
- `CoinCap Api` : For live coin prices and Price History <https://docs.coincap.io/>

## Getting Started

To run the Crypto Currency Exchange locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/rahulrofficial/crypto-exchange.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Crypto
   ```
3. Run Django Server :
   ```bash
   python manage.py runserver
   ```
