from fastapi import FastAPI, status, Response
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import logging.config
from pydantic import BaseModel
import datetime

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

class ResponseData(BaseModel):
    encryptedToken: str 
    role: int = 0
    expirationDate: datetime.date = datetime.date.today().strftime("%d/%m/%Y")

Instrumentator().instrument(app).expose(app)

@app.get("/roleUsers/{encryptedToken}", response_model=ResponseData)
def read_root(encryptedToken: str):
    logger.debug("encryptedToken recibido: " + encryptedToken)
    
    url = 'https://63025538c6dda4f287b7ee62.mockapi.io/infoUsers/service1'
    responseData = ResponseData(encryptedToken= encryptedToken)
    
    requestResult = requests.get(url + "?encryptedToken=" + encryptedToken, timeout=5)
    
    if(len(requestResult.json()) >= 1):
        responseData.role = requestResult.json()[0]["role"]
        return Response(content= responseData.json())
    else:
        return Response(status_code= status.HTTP_204_NO_CONTENT)