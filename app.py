from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from typing import Dict, Any, Optional

# Initialize FastAPI app
app = FastAPI(title="Python Dapr Microservice")

# Pydantic models for request and response
class MessageRequest(BaseModel):
    message: str
    metadata: Optional[Dict[str, Any]] = None

class MessageResponse(BaseModel):
    message: str
    processed: bool

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"status": "online", "service": "Python Dapr Microservice", "version": "1.0.0"}

@app.post("/echo", response_model=MessageResponse)
async def echo_message(request: MessageRequest):
    """
    Echo endpoint that demonstrates a simple request/response pattern.
    """
    return MessageResponse(
        message=f"You sent: {request.message}",
        processed=True
    )

@app.get("/healthz")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

# Dapr pub/sub subscription endpoint
@app.get("/dapr/subscribe")
async def subscribe():
    """
    Dapr subscription endpoint that defines which topics this microservice subscribes to.
    """
    return [
        {
            "pubsubname": "pubsub",  # Name of the pubsub component
            "topic": "messages",     # Topic to subscribe to
            "route": "/messages",    # Route for the messages
        }
    ]

# Endpoint to handle messages from the subscribed topic
@app.post("/messages")
async def messages(request: dict):
    """
    Endpoint that handles messages from Dapr pub/sub.
    """
    # Extract data from Dapr's CloudEvent format
    data = request.get("data", {})
    message = data.get("message", "No message provided")
    
    print(f"Received message via pub/sub: {message}")
    
    return {"status": "Message processed successfully"}

# Dapr binding input handler
@app.post("/binding")
async def binding_handler(request: dict):
    """
    Endpoint that handles Dapr binding inputs.
    """
    binding_name = request.get("metadata", {}).get("name", "unknown")
    data = request.get("data", {})
    
    print(f"Received data from binding '{binding_name}': {data}")
    
    return {"status": "Binding data processed successfully"}
