#!/usr/bin/env python3
"""A simple calculator web API with FastAPI."""
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(
    title="🦞 Calculator API",
    description="A simple calculator API built by Jean Claw Vandamn",
    version="2.0.0"
)

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
        a { color: #e94560; }
    </style>
</head>
<body>
    <h1>🦞 Calculator</h1>
    <p class="subtitle">Built by Jean Claw Vandamn • <a href="/docs">API Docs</a></p>
    
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
        <code>POST /api/calculate</code> with JSON body<br><br>
        📚 <a href="/docs">Interactive Swagger Docs</a> | <a href="/redoc">ReDoc</a>
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

class CalculateRequest(BaseModel):
    a: float
    b: float
    operation: str = "add"

class CalculateResponse(BaseModel):
    operation: str
    a: float
    b: float
    result: float

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the calculator web interface."""
    return HTML_TEMPLATE

@app.get("/api/add", response_model=CalculateResponse, tags=["Operations"])
async def add(a: float = Query(..., description="First number"), 
              b: float = Query(..., description="Second number")):
    """Add two numbers together."""
    return {"operation": "add", "a": a, "b": b, "result": a + b}

@app.get("/api/subtract", response_model=CalculateResponse, tags=["Operations"])
async def subtract(a: float = Query(..., description="First number"), 
                   b: float = Query(..., description="Second number")):
    """Subtract b from a."""
    return {"operation": "subtract", "a": a, "b": b, "result": a - b}

@app.get("/api/multiply", response_model=CalculateResponse, tags=["Operations"])
async def multiply(a: float = Query(..., description="First number"), 
                   b: float = Query(..., description="Second number")):
    """Multiply two numbers."""
    return {"operation": "multiply", "a": a, "b": b, "result": a * b}

@app.get("/api/divide", response_model=CalculateResponse, tags=["Operations"])
async def divide(a: float = Query(..., description="First number"), 
                 b: float = Query(..., description="Second number")):
    """Divide a by b."""
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"operation": "divide", "a": a, "b": b, "result": a / b}

@app.post("/api/calculate", response_model=CalculateResponse, tags=["Operations"])
async def calculate(req: CalculateRequest):
    """Perform a calculation with the specified operation."""
    operations = {
        "add": lambda: req.a + req.b,
        "subtract": lambda: req.a - req.b,
        "multiply": lambda: req.a * req.b,
        "divide": lambda: req.a / req.b if req.b != 0 else None
    }
    
    if req.operation not in operations:
        raise HTTPException(status_code=400, detail="Invalid operation")
    
    result = operations[req.operation]()
    if result is None:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    
    return {"operation": req.operation, "a": req.a, "b": req.b, "result": result}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
