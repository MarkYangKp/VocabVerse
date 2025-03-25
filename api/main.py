from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from controllers import (learning_router)

origins = [
   "*" 
]


from fastapi.staticfiles import StaticFiles

import uvicorn

from pathlib import Path

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # 允许的域名
    allow_credentials=True,           # 允许携带凭证
    allow_methods=["*"],              # 允许的 HTTP 方法，如 GET, POST 等
    allow_headers=["*"],              # 允许的请求头
)

router = APIRouter()

router.include_router(learning_router, prefix="/learning", tags=[ "learning"])

app.include_router(router, prefix="/v1/api", tags=["v1"])


if __name__ == "__main__":

  config = uvicorn.Config("main:app", host="0.0.0.0", port=9988, reload=True)
  server = uvicorn.Server(config)
  server.run()