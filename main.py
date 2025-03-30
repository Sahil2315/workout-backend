from fastapi import FastAPI
import requests
import json

app = FastAPI()

@app.get("/")
async def root():
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a JSON generator."
                    },

                    {
                        "role": "user",
                        "content": "Create a Basic Exercise Plan for a Beginner who does enough Cardio but not enough Weight Training in the JSON Format [{weekDay: String, exercise: [{exerciseName: String, exerciseDescription: String, exerciseSets: number, exerciseReps: String(Reps or Upto Failure)}]}] (Only give me the json no reasoning/introduction required)"
                    }
                ],
                "stream": False,
                "output_format": "json"
            })
        )
        # Process the response content as JSON
        response_json = response.json() 
        message = response_json["choices"][0]["message"]["content"]
        jsonData = json.loads(message.strip("```json\n"))
        return {"message": jsonData}

    
    except requests.exceptions.RequestException as e:
        # Handle HTTP request errors
        return {"error": f"An error occurred: {str(e)}"}
    
    except json.JSONDecodeError:
        # Handle cases where the response isn't valid JSON
        return {"error": "The response could not be decoded as JSON"}
