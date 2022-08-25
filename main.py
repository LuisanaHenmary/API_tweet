from fastapi import FastAPI
#uvicorn main:app --reload 
app = FastAPI()

@app.get(
    path="/"
)
def Home():
    return {"Twitter":"Welcome!"}

@app.get(
    path="/tweets",
    tags=["Tweets"]
)
def ShowAllTwets():
    return {"estado":"en construccion"}