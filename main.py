from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn
from shortener import Shorten

class LinkIn(BaseModel):
    url: str

app = FastAPI()
sh = Shorten()
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <style>
      body { font-family: system-ui; max-width: 600px; margin: 100px auto; }
      input { width: 100%; padding: 12px; font-size: 16px; border: 1px solid #ccc; border-radius: 6px; }
      button { padding: 12px 24px; font-size: 16px; background: #000; color: #fff; border: none; border-radius: 6px; margin-top: 12px; }
    </style>
    <form action="/shorten" method="post">
      <input type="text" name="url" placeholder="Paste your link">
      <button type="submit">Shorten</button>
    </form>
    """

@app.post("/shorten", response_class=HTMLResponse)
def shorten(url: str = Form()):
    check = sh.check_url_in_db(url)
    if check == None:
        return "http://127.0.0.1:8000/" + sh.send_back_new_short_link(url)
    else:
        take_the_long_ass_spaces_out = check.strip()
        return "http://127.0.0.1:8000/" + take_the_long_ass_spaces_out






@app.get("/{link}")
def somewhere(link):
    original = sh.send_link(link)
    if original is None:
        raise HTTPException(status_code=404, detail="link not found")
    return RedirectResponse(original, status_code=301)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

