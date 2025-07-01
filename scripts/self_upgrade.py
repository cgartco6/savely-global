import requests
import json
from config.api_keys import STRIPE_API_KEY

def check_revenue():
    # Get revenue from Stripe
    url = "https://api.stripe.com/v1/balance"
    response = requests.get(url, auth=(STRIPE_API_KEY, ""))
    balance = response.json()
    available = balance['available'][0]['amount'] / 100
    
    # 50% for upgrades, 50% for owner
    upgrade_fund = available * 0.50
    owner_payout = available * 0.50
    
    # Execute upgrades
    execute_upgrades(upgrade_fund)
    
    # Send owner payout
    send_payout(owner_payout)
    
def execute_upgrades(amount):
    upgrades = {
        500: "Upgrade to GPT-4 API",
        1000: "Upgrade to Midjourney Pro",
        2000: "Upgrade video generation",
        5000: "Implement AI anthropologist"
    }
    
    for threshold, description in upgrades.items():
        if amount >= threshold:
            print(f"Executing upgrade: {description}")
            # API calls to upgrade services would go here
            amount -= threshold
            
def send_payout(amount):
    # Send to owner's PayPal/crypto
    print(f"Sending ${amount:.2f} to owner")
    
if __name__ == '__main__':
    check_revenue()
