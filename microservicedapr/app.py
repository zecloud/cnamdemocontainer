import os
from fastapi import FastAPI, HTTPException, Body
from dapr.ext.fastapi import DaprApp
from dapr.clients import DaprClient
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Initialiser FastAPI et DaprApp
app = FastAPI(title="Dapr Microservice Example")
dapr_app = DaprApp(app)

class Message(BaseModel):
    message: str

# Route standard FastAPI
@app.get("/")
async def root():
    return {"message": "Hello from Dapr Microservice"}


# Endpoint pour recevoir des événements via Dapr Input Binding
@dapr_app.binding(name='input-binding')
async def input_binding_handler(data: Dict[str, Any]):
    print(f"Received data from input binding: {data}")
    return {"status": "Success", "data": data}

# Endpoint pour publier un message via Dapr Output Binding
@app.post("/send-message")
async def send_message(message: Message):
    # Appel à un binding Dapr pour envoyer un message
    try:
        # Utiliser le client Dapr pour envoyer au binding
        with DaprClient() as client:
            # Pour Pydantic v2.x
            data = message.model_dump() if hasattr(message, 'model_dump') else message.dict()
            resp = client.invoke_binding(
                binding_name="output-binding",
                operation="create",
                data=data
            )
            return {"status": "Message sent", "binding_response": "Success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

# Endpoint pour invoker un autre service via Dapr
@app.get("/invoke-service/{service_name}")
async def invoke_service(service_name: str, method_name: str = "hello"):
    try:
        # Invoquer une méthode sur un autre service via Dapr
        with DaprClient() as client:
            resp = client.invoke_method(
                app_id=service_name,
                method_name=method_name,
                data={"message": "Hello from caller service"},
                http_verb="GET"
            )
            return {"status": "Service invoked", "response": resp.json() if hasattr(resp, 'json') else resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to invoke service: {str(e)}")

# Endpoint pour publier un événement via pubsub
@app.post("/publish-event")
async def publish_event(message: Message):
    try:
        # Utilisation du client Dapr pour la publication
        with DaprClient() as client:
            # Pour Pydantic v2.x
            data = message.model_dump() if hasattr(message, 'model_dump') else message.dict()
            
            # Publier l'événement sur le topic
            client.publish_event(
                pubsub_name="pubsub",
                topic_name="sample-topic",
                data=data
            )
            return {"status": "Event published", "topic": "sample-topic"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish event: {str(e)}")

# Modèle pour les événements pubsub Cloud Event
class CloudEventModel(BaseModel):
    data: Dict[str, Any]
    datacontenttype: str
    id: str
    pubsubname: str
    source: str
    specversion: str
    topic: str
    traceid: Optional[str] = None
    traceparent: Optional[str] = None
    tracestate: Optional[str] = None
    type: str

# Endpoint pour recevoir des événements pubsub
@dapr_app.subscribe(pubsub='pubsub', topic='sample-topic')
async def pubsub_handler(event_data = Body()):
    print(f"Received pubsub event: {event_data}")
    return {"status": "Success"}

# Endpoint pour recevoir des événements pubsub avec structure CloudEvent
@dapr_app.subscribe(pubsub='pubsub', topic='cloud-topic')
async def cloud_event_handler(event_data: CloudEventModel):
    print(f"Received cloud event: {event_data}")
    user_data = event_data.data
    return {"status": "Success", "user": user_data}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
