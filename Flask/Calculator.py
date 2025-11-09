from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>Simple Arithmetic Operations</h2>
    <form action="/calculate" method="get">
        <label>Number 1:</label>
        <input type="text" name="num1"><br><br>
        
        <label>Number 2:</label>
        <input type="text" name="num2"><br><br>
        
        <label>Operation:</label>
        <select name="operation">
            <option value="add">Add</option>
            <option value="subtract">Subtract</option>
            <option value="multiply">Multiply</option>
            <option value="divide">Divide</option>
        </select><br><br>

        <input type="submit" value="Calculate">
    </form>
    '''

@app.route('/calculate')
def calculate():
    try:
        num1 = float(request.args.get('num1'))
        num2 = float(request.args.get('num2'))
        op = request.args.get('operation')

        if op == 'add':
            result = num1 + num2
        elif op == 'subtract':
            result = num1 - num2
        elif op == 'multiply':
            result = num1 * num2
        elif op == 'divide':
            if num2 == 0:
                return "<h3>Error: Division by zero!</h3>"
            result = num1 / num2
        else:
            return "<h3>Invalid operation!</h3>"

        return f"<h3>Result: {result}</h3><a href='/'>Go Back</a>"

    except Exception as e:
        return f"<h3>Error: {e}</h3><a href='/'>Go Back</a>"

if __name__ == '__main__':
    app.run(debug=True)
