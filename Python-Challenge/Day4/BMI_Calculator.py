from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

class BMICalculator:
    def __init__(self):
        self.categories = {
            "Underweight": {"range": (0, 18.4), "color": "#3498db", "description": "Below normal weight", "class": ""},
            "Normal": {"range": (18.5, 24.9), "color": "#2ecc71", "description": "Healthy weight", "class": ""},
            "Overweight": {"range": (25, 29.9), "color": "#f39c12", "description": "Above normal weight", "class": "Pre-obese"},
            "Obesity Class I": {"range": (30, 34.9), "color": "#e74c3c", "description": "Moderate risk", "class": "Obese Class I"},
            "Obesity Class II": {"range": (35, 39.9), "color": "#c0392b", "description": "Severe risk", "class": "Obese Class II"},
            "Obesity Class III": {"range": (40, 100), "color": "#8e44ad", "description": "Very severe risk", "class": "Obese Class III"}
        }
        
        self.quotes = {
            "Underweight": [
                "Your journey to optimal health starts with balanced nutrition!",
                "Strength comes from nourishing both body and mind.",
                "Every healthy choice brings you closer to your best self."
            ],
            "Normal": [
                "Excellent! You're maintaining a healthy balance - keep up the great work!",
                "Your commitment to health is paying off beautifully!",
                "A healthy weight is the foundation for a vibrant life!"
            ],
            "Overweight": [
                "Your determination today will shape your healthier tomorrow!",
                "Every step forward is progress toward your wellness goals!",
                "Your body is capable of amazing transformations - believe in it!"
            ],
            "Obesity Class I": [
                "Your health journey matters - take it one step at a time!",
                "Professional guidance can unlock your path to wellness!",
                "Your commitment to change is the first step toward vitality!"
            ],
            "Obesity Class II": [
                "Significant changes can lead to significant improvements in health!",
                "Your determination will overcome challenges on this wellness journey!",
                "Every positive choice contributes to your long-term wellbeing!"
            ],
            "Obesity Class III": [
                "Your health deserves immediate attention and professional care!",
                "With proper guidance, you can reclaim your health and vitality!",
                "Your journey to better health starts with a single decision today!"
            ]
        }
    
    def convert_to_kg(self, weight, unit):
        if unit == "pounds":
            return weight * 0.453592
        return weight
    
    def convert_to_meters(self, height, unit):
        if unit == "feet":
            return height * 0.3048
        elif unit == "cm":
            return height / 100
        return height
    
    def calculate_bmi(self, height, weight, height_unit, weight_unit):
        height_m = self.convert_to_meters(height, height_unit)
        weight_kg = self.convert_to_kg(weight, weight_unit)
        
        if height_m <= 0 or weight_kg <= 0:
            return None
        
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 1)
    
    def get_category(self, bmi):
        for category, data in self.categories.items():
            min_range, max_range = data["range"]
            if min_range <= bmi <= max_range:
                return category, data
        return "Unknown", {"color": "#95a5a6", "description": "Unable to determine", "class": ""}
    
    def get_healthy_weight_range(self, height_m):
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 25 * (height_m ** 2)
        return round(min_weight, 1), round(max_weight, 1)
    
    def get_weight_to_lose(self, current_weight_kg, height_m):
        target_bmi = 25
        ideal_max_weight = target_bmi * (height_m ** 2)
        weight_to_lose = current_weight_kg - ideal_max_weight
        return round(weight_to_lose, 1) if weight_to_lose > 0 else 0
    
    def calculate_bmi_prime(self, bmi):
        return round(bmi / 25, 2)
    
    def calculate_ponderal_index(self, height_m, weight_kg):
        return round(weight_kg / (height_m ** 3), 1)
    
    def get_quote(self, category):
        import random
        return random.choice(self.quotes.get(category, ["Stay committed to your health journey!"]))
    
    def get_speedometer_angle(self, bmi):
        min_bmi, max_bmi = 15, 40
        bmi_clamped = max(min_bmi, min(bmi, max_bmi))
        angle = ((bmi_clamped - min_bmi) / (max_bmi - min_bmi)) * 180
        return angle

bmi_calculator = BMICalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        name = data.get('name', '').strip()
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        height_unit = data.get('height_unit', 'meters')
        weight_unit = data.get('weight_unit', 'kg')
        
        if height <= 0 or weight <= 0:
            return jsonify({'error': 'Height and weight must be positive values'}), 400
        
        bmi = bmi_calculator.calculate_bmi(height, weight, height_unit, weight_unit)
        
        if bmi is None:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Convert to meters and kg for additional calculations
        height_m = bmi_calculator.convert_to_meters(height, height_unit)
        weight_kg = bmi_calculator.convert_to_kg(weight, weight_unit)
        
        category, category_data = bmi_calculator.get_category(bmi)
        healthy_weight_range = bmi_calculator.get_healthy_weight_range(height_m)
        weight_to_lose = bmi_calculator.get_weight_to_lose(weight_kg, height_m)
        bmi_prime = bmi_calculator.calculate_bmi_prime(bmi)
        ponderal_index = bmi_calculator.calculate_ponderal_index(height_m, weight_kg)
        quote = bmi_calculator.get_quote(category)
        speedometer_angle = bmi_calculator.get_speedometer_angle(bmi)
        
        result = {
            'bmi': bmi,
            'category': category,
            'category_class': category_data['class'],
            'color': category_data['color'],
            'description': category_data['description'],
            'healthy_weight_range': healthy_weight_range,
            'weight_to_lose': weight_to_lose,
            'bmi_prime': bmi_prime,
            'ponderal_index': ponderal_index,
            'quote': quote,
            'speedometer_angle': speedometer_angle,
            'name': name,
            'current_weight_kg': round(weight_kg, 1)
        }
        
        return jsonify(result)
    
    except ValueError:
        return jsonify({'error': 'Please enter valid numbers for height and weight'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)