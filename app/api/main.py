from fastapi import FastAPI
from .routers import models
from .core import LoggingMiddleware

# instância o app
app = FastAPI()

# adiciona o middleware
app.add_middleware(LoggingMiddleware)

# Registrar rotas - modelos
app.include_router(models.router)
