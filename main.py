from fastapi import FastAPI, HTTPException
from google import genai
from pydantic import BaseModel, ValidationError
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
    allow_origins=["*"],  # List of allowed origins
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

class Preferences(BaseModel):
    daysOfWorkout: str
    level: str
    expInYears: str
    expInMonths: str
    gender: str
    location: str  # Gym or Home
    primaryConcern: str  # Fat loss or Muscle Gain or General Fitness
    weight: str
    height: str  # In cm
    age: str # Years
    specificAilment: str  # Any Body Condidtion that should be known before starting the workout
    

@app.get("/gemini")
async def gem():
    client = genai.Client(api_key="AIzaSyAiRRLUh1RQfm9P7H1ntSNNEm5Z0ksgUhs")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=(
            "Generate a Basic Exercise Plan for an Intermediate Fitness Enthusiast focusing on weight training in strictly valid JSON format. (Weights in KG, All 7 WeekDays included along with the rest days. Week starts from Sunday.)"
        ),
        config={
            "response_mime_type": "application/json",
            "response_schema": list[DayPlan]
        }
    )
    return response.parsed


@app.post("/generateWorkout")
async def generate(pref: Preferences):
    try:
        # Construct the input string
        formString = (
            f"Gender: {pref.gender}, Age: {pref.age}, Specific Ailment: {pref.specificAilment}, "
            f"Weight: {pref.weight} kg, Height: {pref.height}cm, Primary Concern: {pref.primaryConcern}, "
            f"Location: {pref.location}, {pref.daysOfWorkout} - Day Workout Plan, Level: {pref.level}, "
            f"Experience: {pref.expInYears} Years and {pref.expInMonths} Months."
        )

        # Initialize the GenAI client
        client = genai.Client(api_key="AIzaSyAiRRLUh1RQfm9P7H1ntSNNEm5Z0ksgUhs")

        # Generate the content
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=(
                "Generate an Exercise Plan in strictly valid JSON format. "
                "(Weights in KG, All 7 WeekDays included along with the rest days. "
                "Leave the workout array empty in case of rest days. The Week Starts from Sunday.)",
                formString
            ),
            config={
                "response_mime_type": "application/json",
                "response_schema": list[DayPlan]
            }
        )

        return response.parsed

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=f"Validation error: {ve}")

    except (AttributeError, ValueError, TypeError) as e:
        raise HTTPException(status_code=400, detail=f"Client-side error: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
