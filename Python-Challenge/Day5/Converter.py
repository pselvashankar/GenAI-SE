import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- Conversion Constants and Helper Functions ---

# Simple API for currency exchange rates (no API key needed)
CURRENCY_API_BASE = "https://api.frankfurter.app"

def get_currency_rate(base_currency, target_currency):
    """Fetches the real-time exchange rate for a given pair."""
    try:
        response = requests.get(
            f"{CURRENCY_API_BASE}/latest",
            params={'from': base_currency, 'to': target_currency}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data['rates'].get(target_currency, 0.0)
    except requests.exceptions.RequestException:
        return None # Return None on API error

# Simple, non-API unit conversion logic
def convert_temperature(value, unit_from, unit_to):
    """Converts between Celsius and Fahrenheit."""
    if unit_from == 'C' and unit_to == 'F':
        return (value * 9/5) + 32
    elif unit_from == 'F' and unit_to == 'C':
        return (value - 32) * 5/9
    return value

def convert_length(value, unit_from, unit_to):
    """Converts between cm, inches, m, and feet."""
    # Convert to meters first (the base unit)
    to_meters = {
        'cm': 0.01,
        'inches': 0.0254,
        'm': 1.0,
        'ft': 0.3048,
    }
    # Convert from meters to target unit
    from_meters = {
        'cm': 100.0,
        'inches': 1 / 0.0254,
        'm': 1.0,
        'ft': 1 / 0.3048,
    }
    
    if unit_from in to_meters and unit_to in from_meters:
        # value -> meters -> target_unit
        meters = value * to_meters[unit_from]
        return meters * from_meters[unit_to]
    return value

def convert_weight(value, unit_from, unit_to):
    """Converts between kg, lbs, and grams."""
    # Convert to kilograms first (the base unit)
    to_kg = {
        'kg': 1.0,
        'lbs': 0.453592, # 1 lb = 0.453592 kg
        'g': 0.001,
    }
    # Convert from kilograms to target unit
    from_kg = {
        'kg': 1.0,
        'lbs': 1 / 0.453592,
        'g': 1000.0,
    }

    if unit_from in to_kg and unit_to in from_kg:
        # value -> kg -> target_unit
        kilograms = value * to_kg[unit_from]
        return kilograms * from_kg[unit_to]
    return value


# --- Flask Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    # Default values for the converters
    results = {
        'currency_result': 'N/A',
        'temp_result': 'N/A',
        'length_result': 'N/A',
        'weight_result': 'N/A',
        'error_message': None,
        'currency_from': 'INR',
        'currency_to': 'USD',
        'temp_from': 'C',
        'temp_to': 'F',
        'length_from': 'cm',
        'length_to': 'inches',
        'weight_from': 'kg',
        'weight_to': 'lbs',
    }

    if request.method == 'POST':
        try:
            # Get the form name which was submitted to determine the conversion type
            converter_type = request.form.get('converter_type')
            
            # --- CURRENCY CONVERTER ---
            if converter_type == 'currency':
                amount = float(request.form['currency_amount'])
                from_c = request.form['currency_from']
                to_c = request.form['currency_to']

                rate = get_currency_rate(from_c, to_c)

                if rate is not None:
                    results['currency_result'] = f"{amount * rate:.2f} {to_c}"
                else:
                    results['error_message'] = "Could not fetch real-time currency rates."
                
                results['currency_from'] = from_c
                results['currency_to'] = to_c

            # --- TEMPERATURE CONVERTER ---
            elif converter_type == 'temperature':
                amount = float(request.form['temp_amount'])
                from_t = request.form['temp_from']
                to_t = request.form['temp_to']

                converted_value = convert_temperature(amount, from_t, to_t)
                results['temp_result'] = f"{converted_value:.2f} {to_t}"

                results['temp_from'] = from_t
                results['temp_to'] = to_t

            # --- LENGTH CONVERTER ---
            elif converter_type == 'length':
                amount = float(request.form['length_amount'])
                from_l = request.form['length_from']
                to_l = request.form['length_to']

                converted_value = convert_length(amount, from_l, to_l)
                results['length_result'] = f"{converted_value:.2f} {to_l}"
                
                results['length_from'] = from_l
                results['length_to'] = to_l

            # --- WEIGHT CONVERTER ---
            elif converter_type == 'weight':
                amount = float(request.form['weight_amount'])
                from_w = request.form['weight_from']
                to_w = request.form['weight_to']

                converted_value = convert_weight(amount, from_w, to_w)
                results['weight_result'] = f"{converted_value:.2f} {to_w}"

                results['weight_from'] = from_w
                results['weight_to'] = to_w


        except ValueError:
            results['error_message'] = "Please enter a valid numerical amount."
        except Exception as e:
            results['error_message'] = f"An unexpected error occurred: {e}"

    # Currency options for the dropdowns
    results['currency_codes'] = [
        'INR', 'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD'
    ]
    
    return render_template('index.html', **results)

if __name__ == '__main__':
    # You'll run this in VS Code's terminal
    # Set the FLASK_DEBUG=True in your environment for auto-reloading
    app.run(debug=True)