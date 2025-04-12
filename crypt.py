# Import necessary modules
import requests  # For making API requests
import json  # For saving data as JSON
import csv  # For saving data as CSV
from datetime import datetime  # For timestamps (if needed later)
import matplotlib.pyplot as plt  # For plotting charts


# ================================
# CLASS 1: Handles API interaction
# ================================
class CoinGeckoAPI:
    """Handles API requests to CoinGecko."""

    BASE_URL = "https://api.coingecko.com/api/v3"  # Base URL of the API

    def __init__(self):
        # Start a session to reuse the HTTP connection
        self.session = requests.Session()

    def get_market_data(self, vs_currency="usd", per_page=10):
        """
        Fetch market data for top cryptocurrencies.
        Parameters:
            vs_currency: Currency to compare (default is USD)
            per_page: Number of coins to retrieve
        """
        # Endpoint for getting market data
        endpoint = f"{self.BASE_URL}/coins/markets"

        # Query parameters
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",  # Order by market cap
            "per_page": per_page,  # Number of results
            "page": 1,  # First page
            "sparkline": False  # No sparkline chart data
        }

        # Send GET request
        response = self.session.get(endpoint, params=params)

        # Check for successful response
        if response.status_code == 200:
            return response.json()
        else:
            # Raise error with details if failed
            raise Exception(f"API Error: {response.status_code} - {response.text}")


# ======================================================
# CLASS 2: Handles saving, displaying, and plotting data
# ======================================================
class CryptoDataManager:
    """Handles saving, displaying and plotting cryptocurrency data."""

    def __init__(self, data):
        # Store fetched data in the class
        self.data = data

    def save_to_json(self, filename="crypto_data.json"):
        """Save the data to a JSON file."""
        with open(filename, 'w') as file:
            json.dump(self.data, file, indent=4)  # Pretty format
        print(f"[✔] Data saved to {filename}")

    def save_to_csv(self, filename="crypto_data.csv"):
        """Save the data to a CSV file."""
        # Select the fields to store in CSV
        keys = ['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()  # Write header row
            # Write each row of data
            for item in self.data:
                writer.writerow({key: item.get(key, "") for key in keys})
        print(f"[✔] Data saved to {filename}")

    def display_data(self):
        """Print data in a readable format."""
        print("\n📊 Top Cryptocurrencies:")
        for coin in self.data:
            print(
                f"- {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']} | Market Cap: ${coin['market_cap']}")

    def plot_market_caps(self):
        """Plot a bar chart of cryptocurrencies vs market cap."""
        # Extract names and market caps
        names = [coin['name'] for coin in self.data]
        market_caps = [coin['market_cap'] for coin in self.data]

        # Create a bar chart
        plt.figure(figsize=(12, 6))  # Chart size
        bars = plt.bar(names, market_caps, color='skyblue')  # Create bars

        # Format labels and layout
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels
        plt.ylabel('Market Cap (USD)')  # y-axis label
        plt.title('Top Cryptocurrencies by Market Cap')  # Title
        plt.tight_layout()  # Fit layout to screen

        # Annotate bars with values
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, yval, f"${yval:,.0f}",
                     va='bottom', ha='center', fontsize=8, rotation=90)

        # Display the chart
        plt.show()


# =============================================
# CLASS 3: Main Application - brings everything together
# =============================================
class CryptoApp:
    """Main application class tying together API and data management."""

    def __init__(self):
        # Create an instance of the API handler
        self.api = CoinGeckoAPI()

    def run(self):
        """Run the entire crypto data pipeline."""
        try:
            print("[🔄] Fetching data from CoinGecko API...")

            # Step 1: Get market data
            market_data = self.api.get_market_data(per_page=10)

            # Step 2: Manage and process the data
            manager = CryptoDataManager(market_data)

            # Step 3: Display in terminal
            manager.display_data()

            # Step 4: Save data to files
            manager.save_to_json()
            manager.save_to_csv()

            # Step 5: Visualize the market caps
            manager.plot_market_caps()

            print("[✅] Done!")

        except Exception as e:
            # Handle any errors gracefully
            print(f"[❌] An error occurred: {e}")


# =================================
# Entry point of the script
# =================================
if __name__ == "__main__":
    app = CryptoApp()  # Create app instance
    app.run()  # Run the app
