import stripe
from config.api_keys import STRIPE_API_KEY
from database.user_manager import upgrade_user

stripe.api_key = STRIPE_API_KEY

def create_payment_link(country, currency, amount, user_email):
    try:
        # Create product
        product = stripe.Product.create(name="Savely Global Premium")

        # Create price
        price = stripe.Price.create(
            unit_amount=amount*100,
            currency=currency.lower(),
            product=product.id
        )

        # Create checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='https://yourdomain.com/success',
            cancel_url='https://yourdomain.com/cancel',
            customer_email=user_email,
            metadata={
                "country": country,
                "user_id": "user_id_here"  # Should be passed in
            }
        )
        return session.url
    except Exception as e:
        print(f"Payment error: {e}")
        return None

def process_webhook(request):
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return None, 400
    except stripe.error.SignatureVerificationError as e:
        return None, 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment_success(session)

    return "Success", 200

def handle_payment_success(session):
    user_id = session.metadata.get('user_id')
    upgrade_user(user_id)
