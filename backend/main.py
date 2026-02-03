from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ast

app = FastAPI()

# This is the "Magic Key" that lets your Vercel site talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows your Vercel URL to connect
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Backend is Online"}

@app.post("/analyze")
async def analyze(data: dict):
    code = data.get("code", "")
    try:
        tree = ast.parse(code)
        # Simple complexity logic
        complexity = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While)))
        status = "Clean" if complexity < 5 else "High Technical Debt"
        return {
            "score": complexity,
            "status": status,
            "advice": "Keep up the good work!" if complexity < 5 else "Consider breaking down your functions."
        }
    except Exception as e:
        return {"error": str(e)}# refresh
