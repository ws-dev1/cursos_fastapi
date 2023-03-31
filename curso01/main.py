from fastapi import FastAPI
from routers import router

app = FastAPI()
app.include_router(router=router)

@app.get('/hello')
def hello_world():
    return "heloo world"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)

