#!/usr/bin/env python3
"""A simple calculator web API."""
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>🦞 Calculator API</title>
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px; 
            margin: 50px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #eee;
        }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { text-align: center; color: #888; margin-bottom: 30px; }
        .calculator {
            background: #0f0f23;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        input, select, button {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: none;
            border-radius: 10px;
            font-size: 18px;
        }
        input { background: #1a1a3e; color: #fff; }
        select { background: #1a1a3e; color: #fff; }
        button { 
            background: linear-gradient(135deg, #e94560 0%, #ff6b6b 100%);
            color: white; 
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover { transform: scale(1.02); }
        .result { 
            text-align: center; 
            font-size: 2em; 
            margin-top: 20px;
            padding: 20px;
            background: #1a1a3e;
            border-radius: 10px;
        }
        .api-info {
            margin-top: 30px;
            padding: 20px;
            background: #1a1a3e;
            border-radius: 10px;
            font-size: 14px;
        }
        code { background: #0a0a1a; padding: 3px 8px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>🦞 Calculator</h1>
    <p class="subtitle">Built by Jean Claw Vandamn</p>
    
    <div class="calculator">
        <input type="number" id="a" placeholder="First number" step="any">
        <select id="op">
            <option value="add">➕ Add</option>
            <option value="subtract">➖ Subtract</option>
            <option value="multiply">✖️ Multiply</option>
            <option value="divide">➗ Divide</option>
        </select>
        <input type="number" id="b" placeholder="Second number" step="any">
        <button onclick="calculate()">Calculate</button>
        <div class="result" id="result">🔢</div>
    </div>
    
    <div class="api-info">
        <strong>API Endpoints:</strong><br><br>
        <code>GET /api/add?a=5&b=3</code><br>
        <code>GET /api/subtract?a=10&b=4</code><br>
        <code>GET /api/multiply?a=6&b=7</code><br>
        <code>GET /api/divide?a=20&b=4</code><br><br>
        <code>POST /api/calculate</code> with JSON body
    </div>
    
    <script>
        async function calculate() {
            const a = document.getElementById('a').value;
            const b = document.getElementById('b').value;
            const op = document.getElementById('op').value;
            
            if (!a || !b) {
                document.getElementById('result').textContent = '⚠️ Enter both numbers';
                return;
            }
            
            const res = await fetch(`/api/${op}?a=${a}&b=${b}`);
            const data = await res.json();
            
            if (data.error) {
                document.getElementById('result').textContent = '❌ ' + data.error;
            } else {
                document.getElementById('result').textContent = data.result;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/add')
def add():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'operation': 'add', 'a': a, 'b': b, 'result': a + b})

@app.route('/api/subtract')
def subtract():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'operation': 'subtract', 'a': a, 'b': b, 'result': a - b})

@app.route('/api/multiply')
def multiply():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    return jsonify({'operation': 'multiply', 'a': a, 'b': b, 'result': a * b})

@app.route('/api/divide')
def divide():
    a = float(request.args.get('a', 0))
    b = float(request.args.get('b', 0))
    if b == 0:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    return jsonify({'operation': 'divide', 'a': a, 'b': b, 'result': a / b})

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    a = float(data.get('a', 0))
    b = float(data.get('b', 0))
    op = data.get('operation', 'add')
    
    operations = {
        'add': lambda: a + b,
        'subtract': lambda: a - b,
        'multiply': lambda: a * b,
        'divide': lambda: a / b if b != 0 else None
    }
    
    if op not in operations:
        return jsonify({'error': 'Invalid operation'}), 400
    
    result = operations[op]()
    if result is None:
        return jsonify({'error': 'Cannot divide by zero'}), 400
    
    return jsonify({'operation': op, 'a': a, 'b': b, 'result': result})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
