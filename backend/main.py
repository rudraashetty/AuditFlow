from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ast

app = FastAPI(title="AuditFlow AI Engine")

# This allows your Mac's frontend (the website) to talk to your backend (the AI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_spaghetti_score(code_text: str):
    """Analyzes code complexity by counting logic branches."""
    try:
        # Converts text into a tree structure that Python understands
        tree = ast.parse(code_text)
        
        # We count 'if' statements, 'for' loops, and 'while' loops
        # These are the common causes of 'Spaghetti Code'
        complexity = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While)))
        return complexity
    except Exception:
        # Returns -1 if the code pasted by the user has a syntax error
        return -1

@app.get("/")
def home():
    return {"message": "AuditFlow Backend is Running Successfully"}

@app.post("/analyze")
async def analyze(data: dict):
    code = data.get("code", "")
    score = calculate_spaghetti_score(code)
    
    if score == -1:
        return {
            "error": "Syntax Error",
            "status": "Invalid",
            "advice": "The code you pasted is not valid Python. Please check for typos."
        }
    
    # Logic to determine the debt status
    if score == 0:
        status = "Perfectly Optimized"
        advice = "No technical debt detected."
    elif score < 5:
        status = "Clean"
        advice = "Code is readable and maintainable."
    else:
        status = "High Debt (Spaghetti)"
        advice = "Warning: This code is too complex. Consider breaking it into smaller functions."

    return {
        "score": score,
        "status": status,
        "advice": advice
    }