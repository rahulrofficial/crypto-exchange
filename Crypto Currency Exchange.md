# Crypto Currency Exchange

This project is a Crypto Currency Exchange platform that provides live coin prices, historical price graphs, user profiles, trading functionalities, and more.

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

## Files Created

- `index.html`: Contains the main interface for the platform.
- `styles.css`: Stylesheet for the HTML pages.
- `app.js`: Handles client-side interactions, including API calls and UI updates.
- `server.js`: Backend server logic handling user requests and database operations.
- `plotly_helpers.js`: Functions to format data for Plotly.js and render historical price graphs.

## How to Run

To run the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/crypto-exchange.git
