# Stripe BIN Lookup Service

A production-ready Flask API for credit card validation, BIN (Bank Identification Number) lookup, and Stripe payment simulation. This service provides comprehensive card information including validation using the Luhn algorithm, detailed BIN lookup data, and simulated Stripe charge responses.

## Features

- **Credit Card Validation**: Validates credit card numbers using the Luhn algorithm
- **BIN Lookup Integration**: Retrieves detailed card information from the Binlist API
- **Card Type Detection**: Automatically identifies card brands (Visa, Mastercard, American Express, etc.)
- **Stripe Charge Simulation**: Generates realistic simulated Stripe payment responses
- **CORS Support**: Enables cross-origin requests for web applications
- **Error Handling**: Comprehensive error handling with informative error messages
- **Production-Ready**: Includes logging, configuration management, and best practices
- **RESTful API Design**: Clean and intuitive API endpoints

## Requirements

- Python 3.7+
- Flask 3.0.0
- Flask-CORS 4.0.0
- requests 2.31.0
- python-dotenv 1.0.0

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GunYamazakii/Stripe-Charge-2-.git
cd Stripe-Charge-2-
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `.env.example` to `.env` and update the values as needed:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
FLASK_ENV=development
FLASK_APP=app.py
FLASK_DEBUG=True
PORT=5000
BINLIST_API_URL=https://lookup.binlist.net
STRIPE_CHARGE_AMOUNT=2.00
STRIPE_CURRENCY=USD
```

### 5. Run the Application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Health Check

**Endpoint**: `GET /health`

**Description**: Check if the API service is running and healthy.

**Response**:
```json
{
  "status": "healthy",
  "service": "Stripe BIN Lookup Service",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### API Information

**Endpoint**: `GET /api/info`

**Description**: Get information about available endpoints and API configuration.

**Response**:
```json
{
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
    "stripe_charge_amount": "2.00",
    "stripe_currency": "USD",
    "binlist_api_url": "https://lookup.binlist.net"
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### Full Card Validation with BIN Lookup and Stripe Simulation

**Endpoint**: `GET /api/stripe?cc=<card_number>&name=<cardholder_name>`

**Description**: Validates a credit card number, performs BIN lookup, and simulates a Stripe charge.

**Query Parameters**:
- `cc` (required): Credit card number (can include spaces or dashes)
- `name` (optional): Cardholder name (default: "Cardholder")

**Example Request**:
```bash
curl "http://localhost:5000/api/stripe?cc=4532015112830366&name=John%20Doe"
```

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "card_validation": {
    "is_valid": true,
    "card_number": "****-****-****-0366",
    "card_type": "Visa",
    "card_length": 16,
    "luhn_check": "passed"
  },
  "bin_lookup": {
    "bin": "453201",
    "brand": "visa",
    "type": "credit",
    "sub_type": "unknown",
    "issuer": {
      "name": "BANK OF AMERICA, N.A.",
      "country": "US"
    },
    "country": {
      "name": "United States",
      "alpha2": "US",
      "alpha3": "USA",
      "numeric": "840"
    },
    "bank": {
      "name": "BANK OF AMERICA, N.A.",
      "url": "www.bankofamerica.com",
      "phone": "+1 800-432-1000"
    }
  },
  "stripe_charge": {
    "id": "ch_20240115103045",
    "object": "charge",
    "amount": 200,
    "amount_captured": 200,
    "amount_refunded": 0,
    "currency": "usd",
    "status": "succeeded",
    "description": "Test charge for Visa",
    "created": "2024-01-15T10:30:45.123456",
    "payment_method": {
      "id": "pm_20240115103045",
      "object": "payment_method",
      "type": "card",
      "card": {
        "brand": "visa",
        "last4": "0366",
        "exp_month": 12,
        "exp_year": 2029,
        "fingerprint": "fp_0366"
      }
    },
    "receipt_url": "https://receipts.stripe.com/r/test_20240115103045",
    "outcome": {
      "network_status": "approved_by_network",
      "reason": null,
      "risk_level": "normal",
      "risk_score": 32,
      "seller_message": "Payment complete.",
      "type": "authorized"
    }
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Error Response** (HTTP 400):
```json
{
  "success": false,
  "error": "Invalid credit card number (Luhn check failed)",
  "card_number": "****-****-****-1234",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### Card Validation Only

**Endpoint**: `GET /api/validate?cc=<card_number>` or `POST /api/validate`

**Description**: Validates a credit card number without performing BIN lookup or Stripe simulation.

**Query Parameters** (GET):
- `cc` (required): Credit card number

**Body Parameters** (POST):
```json
{
  "cc": "4532015112830366"
}
```

**Example Request**:
```bash
# GET method
curl "http://localhost:5000/api/validate?cc=4532015112830366"

# POST method
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"cc":"4532015112830366"}'
```

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "card_number": "****-****-****-0366",
  "is_valid": true,
  "card_type": "Visa",
  "card_length": 16,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

### BIN Lookup Only

**Endpoint**: `GET /api/bin/<bin_code>`

**Description**: Performs a BIN lookup for a given BIN code (first 6 digits of a card).

**Path Parameters**:
- `bin_code` (required): The BIN code (minimum 6 digits)

**Example Request**:
```bash
curl "http://localhost:5000/api/bin/453201"
```

**Success Response** (HTTP 200):
```json
{
  "success": true,
  "bin": "453201",
  "data": {
    "scheme": "visa",
    "type": "credit",
    "subtype": "unknown",
    "issuer": {
      "name": "BANK OF AMERICA, N.A.",
      "country": "US"
    },
    "country": {
      "name": "United States",
      "alpha2": "US",
      "alpha3": "USA",
      "numeric": "840"
    },
    "bank": {
      "name": "BANK OF AMERICA, N.A.",
      "url": "www.bankofamerica.com",
      "phone": "+1 800-432-1000"
    }
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Error Response** (HTTP 404):
```json
{
  "success": false,
  "error": "BIN lookup failed for 999999",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

## Usage Examples

### Python

```python
import requests

# Full card validation with BIN lookup and Stripe simulation
response = requests.get(
    'http://localhost:5000/api/stripe',
    params={
        'cc': '4532015112830366',
        'name': 'John Doe'
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Card Valid: {data['card_validation']['is_valid']}")
    print(f"Card Type: {data['card_validation']['card_type']}")
    print(f"Issuer: {data['bin_lookup']['issuer']['name']}")
    print(f"Stripe Status: {data['stripe_charge']['status']}")
else:
    print(f"Error: {response.json()['error']}")
```

### JavaScript/Node.js

```javascript
// Full card validation with BIN lookup and Stripe simulation
fetch('http://localhost:5000/api/stripe?cc=4532015112830366&name=John%20Doe')
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      console.log(`Card Valid: ${data.card_validation.is_valid}`);
      console.log(`Card Type: ${data.card_validation.card_type}`);
      console.log(`Issuer: ${data.bin_lookup.issuer.name}`);
      console.log(`Stripe Status: ${data.stripe_charge.status}`);
    } else {
      console.error(`Error: ${data.error}`);
    }
  });
```

### cURL

```bash
# Full card validation
curl "http://localhost:5000/api/stripe?cc=4532015112830366&name=John%20Doe"

# Card validation only
curl "http://localhost:5000/api/validate?cc=4532015112830366"

# BIN lookup only
curl "http://localhost:5000/api/bin/453201"

# API information
curl "http://localhost:5000/api/info"

# Health check
curl "http://localhost:5000/health"
```

---

## Test Credit Card Numbers

The following test credit card numbers can be used for development and testing:

| Card Type | Card Number | CVC | Expiry |
|-----------|-------------|-----|--------|
| Visa | 4532015112830366 | 123 | 12/2029 |
| Visa | 4556737586899855 | 456 | 12/2029 |
| Mastercard | 5425233010103442 | 123 | 12/2029 |
| Mastercard | 5105105105105100 | 456 | 12/2029 |
| American Express | 378282246310005 | 1234 | 12/2029 |
| Discover | 6011111111111117 | 123 | 12/2029 |

---

## Error Handling

The API provides clear error messages for various scenarios:

### Missing Required Parameter
```json
{
  "success": false,
  "error": "Missing required parameter: 'cc' (credit card number)",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Invalid Card Number
```json
{
  "success": false,
  "error": "Invalid credit card number (Luhn check failed)",
  "card_number": "****-****-****-1234",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### BIN Lookup Failure
```json
{
  "success": false,
  "error": "BIN lookup failed for 999999",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Endpoint Not Found
```json
{
  "success": false,
  "error": "Endpoint not found",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

---

## Security Considerations

1. **HTTPS in Production**: Always use HTTPS in production environments to protect sensitive card data in transit.

2. **Input Validation**: The API validates all input and sanitizes card numbers for display.

3. **Card Masking**: Card numbers are masked in responses, showing only the last 4 digits.

4. **No Card Storage**: The API does not store card numbers or any sensitive data.

5. **CORS Configuration**: CORS is enabled for development. Configure it appropriately for production.

6. **Rate Limiting**: Consider implementing rate limiting in production to prevent abuse.

7. **Logging**: All errors are logged for monitoring and debugging.

---

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:

```bash
docker build -t stripe-bin-service .
docker run -p 5000:5000 stripe-bin-service
```

### Using Render

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set the build command: `pip install -r requirements.txt`
5. Set the start command: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`
6. Deploy

---

## API Response Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success - Request processed successfully |
| 400 | Bad Request - Missing or invalid parameters |
| 404 | Not Found - Endpoint or resource not found |
| 405 | Method Not Allowed - HTTP method not supported |
| 500 | Internal Server Error - Server-side error |

---

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, change it in `.env`:

```env
PORT=5001
```

### BIN Lookup Not Working

Ensure you have internet connectivity and the Binlist API is accessible:

```bash
curl https://lookup.binlist.net/453201
```

### CORS Issues

If you encounter CORS errors, ensure Flask-CORS is installed and the API is running with CORS enabled.

---

## License

This project is licensed under the MIT License.

---

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release
- Credit card validation using Luhn algorithm
- BIN lookup integration with Binlist API
- Stripe charge simulation
- CORS support
- Comprehensive error handling
- Production-ready Flask application

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Disclaimer

This API is for educational and testing purposes. The Stripe charge simulation is not a real transaction and does not actually charge any payment method. Always use official Stripe APIs for production payment processing.
