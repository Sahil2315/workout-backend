from fastapi import FastAPI
from google import genai
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8081",
    "http://127.0.0.1:8081"
    "http://localhost:19006",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class Exercise(BaseModel):
    exName: str
    exDesc: str
    exSets: int
    exReps: int
    exWeight: str

class DayPlan(BaseModel):
    weekDay: str
    workout: list[Exercise]


@app.get("/gemini")
async def gem():
    client = genai.Client(api_key="AIzaSyAiRRLUh1RQfm9P7H1ntSNNEm5Z0ksgUhs")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            "Generate a Basic Exercise Plan for an Intermediate Gymbro focusing on weight training in strictly valid JSON format. (Weights in KG)"
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": list[DayPlan]
        }
    )

    # jsonObject = json.loads(response["parsed"])

    return response.parsed