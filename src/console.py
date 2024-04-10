import uvicorn


def dev():
    uvicorn.run("src.main:app", port=8000, reload=True)
