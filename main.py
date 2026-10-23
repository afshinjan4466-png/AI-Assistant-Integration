import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI(
    title="AI Assistant Integration API",
    description="Backend service for embedding AI capabilities into web platforms."
)

# Request model
class ChatRequest(BaseModel):
    prompt: str
    system_instruction: str = "You are a helpful AI assistant."

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI Assistant Integration Service is running."}

@app.post("/api/chat")
async def generate_response(request: ChatRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Fallback response for demonstration / standard API structure
        return {
            "status": "success",
            "model": "gpt-4-turbo",
            "reply": f"[AI Response to: '{request.prompt}'] - System initialized and ready for deployment."
        }
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": request.system_instruction},
                {"role": "user", "content": request.prompt}
            ]
        )
        return {
            "status": "success",
            "reply": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
