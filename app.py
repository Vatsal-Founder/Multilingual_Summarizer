# app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from src.MultilingualSummarizer.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Multilingual Summarizer")
templates = Jinja2Templates(directory="templates")

# Optional: serve /static if you add assets later
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# ---- Load model once (faster) ----
@app.on_event("startup")
def _load_pipeline():
    app.state.predictor = PredictionPipeline()

# ---- Schemas ----
class SummaryRequest(BaseModel):
    text: str

# ---- Routes ----
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/docs_redirect")
async def docs_redirect():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return HTMLResponse("Training successful !!")
    except Exception as e:
        return HTMLResponse(f"Error Occurred! {e}", status_code=500)

@app.post("/predict")
async def predict(req: SummaryRequest):
    try:
        # use the already-loaded model
        predictor: PredictionPipeline = app.state.predictor
        summary = predictor.predict(req.text)
        return {"summary": summary}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run: uvicorn app:app --reload --port 8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
