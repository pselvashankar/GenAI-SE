from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class Calculator:
    @staticmethod
    def calculate(num1, num2, operation):
        """Perform arithmetic calculation with error handling"""
        try:
            num1 = float(num1)
            num2 = float(num2)
            
            operations = {
                'add': ('+', lambda x, y: x + y),
                'subtract': ('-', lambda x, y: x - y),
                'multiply': ('×', lambda x, y: x * y),
                'divide': ('÷', lambda x, y: x / y if y != 0 else None)
            }
            
            if operation not in operations:
                return None, "Invalid operation"
            
            symbol, func = operations[operation]
            
            if operation == 'divide' and num2 == 0:
                return None, "Division by zero is not allowed"
            
            result = func(num1, num2)
            return result, None
            
        except ValueError:
            return None, "Please enter valid numbers"
        except Exception as e:
            return None, f"An error occurred: {str(e)}"

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    num1 = data.get('num1', '')
    num2 = data.get('num2', '')
    operation = data.get('operation', 'add')
    
    # Validate inputs
    if not num1 or not num2:
        return jsonify({
            'success': False,
            'error': 'Please enter both numbers'
        })
    
    result, error = Calculator.calculate(num1, num2, operation)
    
    if error:
        return jsonify({
            'success': False,
            'error': error
        })
    
    # Format the display
    operations_display = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    }
    
    symbol = operations_display.get(operation, '+')
    
    return jsonify({
        'success': True,
        'result': result,
        'expression': f"{num1} {symbol} {num2}",
        'full_calculation': f"{num1} {symbol} {num2} = {result}"
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)