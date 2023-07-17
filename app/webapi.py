from fastapi import FastAPI

from main import get_typos, get_distance

app = FastAPI()


@app.post("/ping")
def ping():

    return {"status": "ok"}


@app.post("/find_typos")
def find_typos(
    text: str, max_distance: int = 0, max_options: int = 3, engine: str = "lev"
):

    return get_typos(text, max_distance, max_options, engine)


@app.post("/calc_distance")
def calc_distance(word1: str, word2: str, engine: str="lev"):

    return get_distance(word1, word2, max_distance=0, engine=engine)
