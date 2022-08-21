from fastapi import FastAPI, status, Response
import requests
from prometheus_fastapi_instrumentator import Instrumentator
import logging.config
from pydantic import BaseModel

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()

class ResponseData(BaseModel):
    encryptedToken: str = ""
    internalId: int

Instrumentator().instrument(app).expose(app)

@app.get("/authUsers/{internalId}", response_model=ResponseData)
def read_root(internalId: int):
    internalId_string = str(internalId)
    logger.debug("internalId recibido : " + internalId_string)
    
    url = 'https://63025538c6dda4f287b7ee62.mockapi.io/infoUsers/service1'
    responseData = ResponseData(internalId= internalId)
    
    requestResult = requests.get(url + "?internalId=" + internalId_string, timeout=5)
    
    if(len(requestResult.json()) >= 1):
        responseData.encryptedToken = requestResult.json()[0]["encryptedToken"]
        return Response(content= responseData.json())
    else:
        return Response(status_code= status.HTTP_204_NO_CONTENT)