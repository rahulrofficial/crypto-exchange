# Crypto Currency Exchange: A Comprehensive Overview

## Introduction

The Crypto Currency Exchange stands as a dynamic and robust platform, dedicated to providing users with a sophisticated interface for navigating the world of cryptocurrencies. Powered by the CoinCap.io API, this platform brings forth a comprehensive array of functionalities and tools aimed at offering real-time insights, historical data, and user-friendly interactions.This project is a Crypto Currency Exchange platform that provides live coin prices, historical price graphs, user profiles, trading functionalities, and more.

### Overview of the Project

This platform is meticulously designed to cater to both novice and experienced cryptocurrency enthusiasts. The core focus revolves around delivering live updates for over 100 cryptocurrencies, enabling users to monitor and analyze market movements on a granular level. The fusion of live coin prices and historical data visualization empowers users to make informed decisions in their crypto ventures.

## Distinctiveness and Complexity

### Distinctiveness

Our project stands out due to its comprehensive set of features covering live coin prices for over 100 currencies, real-time updates on price changes, user profiles with edit options, a multi-currency wallet, buy/sell functionalities using the CoinCap API, and the ability to create, view, and fulfill orders within the platform.

### Complexity

The complexity of our project lies in its varied functionalities:
- **Live Coin Prices**: Utilizes the CoinCap.io API to fetch live prices and updates in real-time.
- **Historical Price Graphs**: Utilizes Plotly.js to display price history in different periods.
- **User Profiles and Wallets**: Manages user details, profile pictures, wallet contents, and their respective values in USD.
- **Trading and Orders**: Implements buying, selling, order creation, fulfilling, and tracking user history.
- **API Integration**: Relies on CoinCap API for live coin data, order dealing API for trade execution, and additional APIs for user-related information.

## Features in Detail

### Live Coin Prices

The platform's centerpiece functionality harnesses the CoinCap.io API to provide users with real-time updates on cryptocurrency prices. The continuous updates ensure users stay abreast of market changes, offering an invaluable edge in the volatile world of digital assets.

### Historical Price Visualization

One of the platform's standout features is its ability to showcase detailed price history for each cryptocurrency. Using Plotly.js, this functionality presents historical data in various timeframes—ranging from a day to a minute—enabling users to analyze trends and patterns with precision.

### Top 10 Crypto Currency Index

The index section acts as a quick reference guide, offering a concise view of the top 10 cryptocurrencies. This feature provides immediate insights into the performance of leading digital currencies, aiding users in monitoring market trends efficiently.

### Profile Management

Users have complete control over their profiles within the platform. They can effortlessly view and update personal information, including email, first name, last name, and profile picture URL. This personalized approach ensures user information remains accurate and up-to-date.

### Coin Details with view_coin Functionality

The view_coin feature enhances user experience by offering detailed insights into individual cryptocurrencies. It combines live price updates, supply, maximum supply, market capitalization, volume change in 24 hours, and historical data visualization. Additionally, it allows users to conveniently add or remove coins from their watchlist.

### Market Overview: Markets Functionality

The platform offers a comprehensive market overview, displaying live prices of hundreds of coins. This functionality enables users to easily add or remove coins from their watchlist, fostering a tailored experience based on their preferences.

### USD Deposit Functionality

Users can deposit USD into their accounts, providing them with the means to purchase cryptocurrencies using deposited funds. This feature ensures seamless integration of fiat currency transactions within the platform.

### Multi-Currency Wallet: Wallet Functionality

The multi-currency wallet serves as a secure repository for users' cryptocurrencies. It showcases the current amount and value of the stored coins in USD, allowing users to effectively manage their digital assets.

### Buy/Sell Functionality

The buy/sell feature enables users to engage in cryptocurrency transactions at the current market price. Leveraging the CoinCap API, users can seamlessly execute buy or sell orders based on real-time market valuations.

### Transaction History: History Functionality

The platform meticulously records users' transaction history, providing a chronological account of their purchases, sales, transfers, and receipts. This detailed record ensures transparency and aids users in monitoring their activities within the platform.

### Peer-to-Peer Transfers: Transfer Functionality

Users can initiate direct cryptocurrency transfers to other platform users. This functionality fosters a peer-to-peer exchange ecosystem within the platform, enhancing user interaction and engagement.

### Watchlist Management

The watchlist feature enables users to monitor their preferred coins by listing them in a watchlist. Users can effortlessly track the current prices of these coins, providing a convenient overview of their investment interests.

### Order Management: Create Order and My Order Functionalities

The platform empowers users to create buy or sell orders visible to other users. Additionally, users can manage their active and fulfilled orders, including the ability to close active orders and receive the frozen amount back into their wallets.

### Market Orders: All Orders Functionality

The all orders feature displays all current active orders, except the user's own orders. This functionality allows users to take appropriate actions, such as buying or selling, on these orders.

## APIs Utilized

### CoinCap API

The CoinCap API serves as the backbone of the platform, providing real-time coin prices, coin details, and historical price data. The integration of this API ensures the platform remains up-to-date with accurate cryptocurrency information.

### Order_Deal API

The order_deal API facilitates buying, selling, or closing orders using JavaScript within the platform. This API plays a pivotal role in executing trade orders and ensuring seamless user interactions.

### Info API

The info API serves as an information hub, offering details about listed coins, user wallets, watchlist contents, and relevant amounts. This API supports various functionalities, enhancing user interactions within the platform.

### Coin_Data API

The coin_data API furnishes the platform with current data for listed coins. Its integration ensures users have access to real-time information about cryptocurrencies.

### Price_History API

The price_history API plays a crucial role in formatting data from the CoinCap API's price history and feeding it to Plotly.js for live price graph visualization. This API enhances the platform's ability to present historical price data effectively.

---

## Getting Started

To run the Crypto Currency Exchange locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-exchange.git
