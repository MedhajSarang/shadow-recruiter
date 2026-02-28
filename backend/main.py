from fastapi import FastAPI

#Initialize the application
app = FastAPI(title = "Shadow Recruiter API")

#Create the first endoint
@app.get("/")
def read_root():
    return {
        "status": "success",
        "message": "Shadow Recruiter API is running!"
    }