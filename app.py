"""
Stripe BIN Lookup Service - Flask API
A production-ready Flask API for credit card validation, BIN lookup, and Stripe payment simulation.
"""

import os
import json
import requests
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_SORT_KEYS'] = False
BINLIST_API_URL = os.getenv('BINLIST_API_URL', 'https://lookup.binlist.net')
STRIPE_CHARGE_AMOUNT = os.getenv('STRIPE_CHARGE_AMOUNT', '2.00')
STRIPE_CURRENCY = os.getenv('STRIPE_CURRENCY', 'USD')


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_luhn(card_number):
    """
    Validate a credit card number using the Luhn algorithm.
    
    Args:
        card_number (str): The credit card number to validate.
        
    Returns:
        bool: True if the card number is valid, False otherwise.
    """
    # Remove spaces and dashes
    card_number = str(card_number).replace(' ', '').replace('-', '')
    
    # Check if it contains only digits
    if not card_number.isdigit():
        return False
    
    # Check if length is between 13 and 19 (valid card length range)
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    
    # Apply Luhn algorithm
    def digits_of(n):
        return [int(d) for d in str(n)]
    
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    
    return checksum % 10 == 0


def format_card_number(card_number):
    """
    Format a credit card number for display (last 4 digits visible).
    
    Args:
        card_number (str): The credit card number.
        
    Returns:
        str: Formatted card number (e.g., "****-****-****-1234").
    """
    card_number = str(card_number).replace(' ', '').replace('-', '')
    if len(card_number) >= 4:
        return f"****-****-****-{card_number[-4:]}"
    return "****"


def get_card_type(card_number):
    """
    Determine the card type based on the first few digits (IIN).
    
    Args:
        card_number (str): The credit card number.
        
    Returns:
        str: The card type (e.g., "Visa", "Mastercard", "American Express").
    """
    card_number = str(card_number).replace(' ', '').replace('-', '')
    
    if not card_number:
        return "Unknown"
    
    first_digit = card_number[0]
    first_two = card_number[:2]
    first_four = card_number[:4]
    
    # Visa
    if first_digit == '4':
        return "Visa"
    
    # Mastercard
    if first_two in ['51', '52', '53', '54', '55'] or (51 <= int(first_four) <= 55):
        return "Mastercard"
    
    # American Express
    if first_two in ['34', '37']:
        return "American Express"
    
    # Discover
    if first_four in ['6011', '622126', '622925'] or first_two == '65':
        return "Discover"
    
    # Diners Club
    if first_two in ['36', '38', '39'] or first_four == '3010':
        return "Diners Club"
    
    # JCB
    if first_four in ['3528', '3589'] or (3528 <= int(first_four) <= 3589):
        return "JCB"
    
    return "Unknown"


def lookup_bin(bin_code):
    """
    Lookup BIN information using the Binlist API.
    
    Args:
        bin_code (str): The first 6 digits of the card (BIN).
        
    Returns:
        dict: BIN information or None if lookup fails.
    """
    try:
        url = f"{BINLIST_API_URL}/{bin_code}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        app.logger.error(f"BIN lookup failed for {bin_code}: {str(e)}")
        return None


def simulate_stripe_charge(card_number, card_holder_name=None):
    """
    Simulate a Stripe charge response.
    
    Args:
        card_number (str): The credit card number.
        card_holder_name (str): Optional cardholder name.
        
    Returns:
        dict: Simulated Stripe charge response.
    """
    card_number_clean = str(card_number).replace(' ', '').replace('-', '')
    
    return {
        "id": f"ch_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "object": "charge",
        "amount": int(float(STRIPE_CHARGE_AMOUNT) * 100),  # Amount in cents
        "amount_captured": int(float(STRIPE_CHARGE_AMOUNT) * 100),
        "amount_refunded": 0,
        "currency": STRIPE_CURRENCY.lower(),
        "status": "succeeded",
        "description": f"Test charge for {get_card_type(card_number_clean)}",
        "created": datetime.now().isoformat(),
        "payment_method": {
            "id": f"pm_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "object": "payment_method",
            "type": "card",
            "card": {
                "brand": get_card_type(card_number_clean).lower(),
                "last4": card_number_clean[-4:],
                "exp_month": 12,
                "exp_year": 2029,
                "fingerprint": f"fp_{card_number_clean[-4:]}",
            }
        },
        "receipt_url": f"https://receipts.stripe.com/r/test_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "outcome": {
            "network_status": "approved_by_network",
            "reason": None,
            "risk_level": "normal",
            "risk_score": 32,
            "seller_message": "Payment complete.",
            "type": "authorized"
        }
    }


# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Stripe BIN Lookup Service",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/stripe', methods=['GET'])
def stripe_api():
    """
    Main API endpoint for credit card validation and BIN lookup.
    
    Query Parameters:
        cc (str): Credit card number (required)
        name (str): Cardholder name (optional)
        
    Returns:
        JSON response with card validation, BIN lookup, and Stripe charge simulation.
    """
    try:
        # Get credit card number from query parameter
        card_number = request.args.get('cc', '').strip()
        card_holder_name = request.args.get('name', 'Cardholder').strip()
        
        # Validate input
        if not card_number:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: 'cc' (credit card number)",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Validate card number with Luhn algorithm
        is_valid = validate_luhn(card_number)
        
        if not is_valid:
            return jsonify({
                "success": False,
                "error": "Invalid credit card number (Luhn check failed)",
                "card_number": format_card_number(card_number),
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # Extract BIN (first 6 digits)
        card_number_clean = card_number.replace(' ', '').replace('-', '')
        bin_code = card_number_clean[:6]
        
        # Lookup BIN information
        bin_info = lookup_bin(bin_code)
        
        # Simulate Stripe charge
        stripe_response = simulate_stripe_charge(card_number_clean, card_holder_name)
        
        # Build response
        response = {
            "success": True,
            "card_validation": {
                "is_valid": True,
                "card_number": format_card_number(card_number_clean),
                "card_type": get_card_type(card_number_clean),
                "card_length": len(card_number_clean),
                "luhn_check": "passed"
            },
            "bin_lookup": {
                "bin": bin_code,
                "brand": bin_info.get("scheme", "Unknown") if bin_info else "Unknown",
                "type": bin_info.get("type", "Unknown") if bin_info else "Unknown",
                "sub_type": bin_info.get("subtype", "Unknown") if bin_info else "Unknown",
                "issuer": {
                    "name": bin_info.get("issuer", {}).get("name", "Unknown") if bin_info else "Unknown",
                    "country": bin_info.get("issuer", {}).get("country", "Unknown") if bin_info else "Unknown"
                } if bin_info else {"name": "Unknown", "country": "Unknown"},
                "country": {
                    "name": bin_info.get("country", {}).get("name", "Unknown") if bin_info else "Unknown",
                    "alpha2": bin_info.get("country", {}).get("alpha2", "Unknown") if bin_info else "Unknown",
                    "alpha3": bin_info.get("country", {}).get("alpha3", "Unknown") if bin_info else "Unknown",
                    "numeric": bin_info.get("country", {}).get("numeric", "Unknown") if bin_info else "Unknown"
                } if bin_info else {"name": "Unknown", "alpha2": "Unknown", "alpha3": "Unknown", "numeric": "Unknown"},
                "bank": {
                    "name": bin_info.get("bank", {}).get("name", "Unknown") if bin_info else "Unknown",
                    "url": bin_info.get("bank", {}).get("url", "Unknown") if bin_info else "Unknown",
                    "phone": bin_info.get("bank", {}).get("phone", "Unknown") if bin_info else "Unknown"
                } if bin_info else {"name": "Unknown", "url": "Unknown", "phone": "Unknown"}
            },
            "stripe_charge": stripe_response,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/validate', methods=['GET', 'POST'])
def validate_card():
    """
    Endpoint for card validation only (without BIN lookup or Stripe simulation).
    
    Query/Body Parameters:
        cc (str): Credit card number (required)
        
    Returns:
        JSON response with card validation result.
    """
    try:
        # Get card number from query or POST body
        if request.method == 'POST':
            data = request.get_json() or {}
            card_number = data.get('cc', '').strip()
        else:
            card_number = request.args.get('cc', '').strip()
        
        if not card_number:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: 'cc' (credit card number)",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        is_valid = validate_luhn(card_number)
        
        return jsonify({
            "success": True,
            "card_number": format_card_number(card_number),
            "is_valid": is_valid,
            "card_type": get_card_type(card_number),
            "card_length": len(card_number.replace(' ', '').replace('-', '')),
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error in validate_card: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/bin/<bin_code>', methods=['GET'])
def bin_lookup(bin_code):
    """
    Endpoint for BIN lookup only.
    
    Path Parameters:
        bin_code (str): The BIN code (first 6 digits of card).
        
    Returns:
        JSON response with BIN information.
    """
    try:
        if not bin_code or len(bin_code) < 6:
            return jsonify({
                "success": False,
                "error": "Invalid BIN code. Must be at least 6 digits.",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        bin_info = lookup_bin(bin_code[:6])
        
        if not bin_info:
            return jsonify({
                "success": False,
                "error": f"BIN lookup failed for {bin_code}",
                "timestamp": datetime.now().isoformat()
            }), 404
        
        return jsonify({
            "success": True,
            "bin": bin_code[:6],
            "data": bin_info,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error in bin_lookup: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/info', methods=['GET'])
def api_info():
    """
    Endpoint providing API information and available endpoints.
    
    Returns:
        JSON response with API documentation.
    """
    return jsonify({
        "service": "Stripe BIN Lookup Service",
        "version": "1.0.0",
        "description": "A production-ready Flask API for credit card validation, BIN lookup, and Stripe payment simulation.",
        "endpoints": {
            "GET /health": "Health check endpoint",
            "GET /api/info": "API information and documentation",
            "GET /api/stripe?cc=<card_number>&name=<name>": "Full card validation, BIN lookup, and Stripe charge simulation",
            "GET /api/validate?cc=<card_number>": "Card validation only",
            "POST /api/validate": "Card validation (POST method)",
            "GET /api/bin/<bin_code>": "BIN lookup only"
        },
        "configuration": {
            "stripe_charge_amount": STRIPE_CHARGE_AMOUNT,
            "stripe_currency": STRIPE_CURRENCY,
            "binlist_api_url": BINLIST_API_URL
        },
        "timestamp": datetime.now().isoformat()
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "success": False,
        "error": "Method not allowed",
        "timestamp": datetime.now().isoformat()
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
