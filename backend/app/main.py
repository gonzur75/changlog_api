from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hi I'm Changelog  nice to meet you"}
