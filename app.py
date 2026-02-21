from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML template for the calculator UI
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Calculator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .calculator {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .input-group {
            margin: 15px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #e7f3e7;
            border-radius: 5px;
            display: none;
        }
        .error {
            background-color: #fce4e4;
            color: #c00;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>🧮 Simple Calculator</h1>
        <div class="input-group">
            <label>First Number:</label>
            <input type="number" id="num1" step="any" placeholder="Enter first number">
        </div>
        <div class="input-group">
            <label>Operation:</label>
            <select id="operation">
                <option value="add">Add (+)</option>
                <option value="subtract">Subtract (-)</option>
                <option value="multiply">Multiply (×)</option>
                <option value="divide">Divide (÷)</option>
            </select>
        </div>
        <div class="input-group">
            <label>Second Number:</label>
            <input type="number" id="num2" step="any" placeholder="Enter second number">
        </div>
        <button onclick="calculate()">Calculate</button>
        <div id="result" class="result"></div>
    </div>

    <script>
        function calculate() {
            const num1 = parseFloat(document.getElementById('num1').value);
            const num2 = parseFloat(document.getElementById('num2').value);
            const operation = document.getElementById('operation').value;
            const resultDiv = document.getElementById('result');

            if (isNaN(num1) || isNaN(num2)) {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '❌ Please enter valid numbers';
                resultDiv.style.display = 'block';
                return;
            }

            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    num1: num1,
                    num2: num2,
                    operation: operation
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '❌ ' + data.error;
                } else {
                    resultDiv.className = 'result';
                    resultDiv.innerHTML = '✅ Result: <strong>' + data.result + '</strong>';
                }
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                resultDiv.className = 'result error';
                resultDiv.innerHTML = '❌ Error: ' + error;
                resultDiv.style.display = 'block';
            });
        }
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/calculate", methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']

        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 == 0:
                return jsonify({'error': 'Cannot divide by zero'}), 400
            result = num1 / num2
        else:
            return jsonify({'error': 'Invalid operation'}), 400

        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/health")
def health():
    return jsonify({'status': 'healthy', 'message': 'Calculator API is running'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
