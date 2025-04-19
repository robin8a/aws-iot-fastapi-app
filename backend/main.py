from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from dotenv import load_dotenv

from aws_iot import AWSIoTClient
from models import IoTMessage, IoTSubscriptionRequest, IoTPublishRequest, StatusResponse

# Load environment variables
load_dotenv()

app = FastAPI(title="AWS IoT Core FastAPI Web Application")

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")

manager = ConnectionManager()

# Initialize IoT client with the topic from environment variable or use default
iot_topic = os.getenv("AWS_IOT_TOPIC", "test/topic")
iot_client = AWSIoTClient(iot_topic)

# Define a callback function to handle IoT messages
def handle_iot_message(message: Dict[str, Any]):
    """
    Handle messages received from AWS IoT Core
    This function will be called when a message is received from the topic
    """
    # Convert the message to JSON and broadcast to all WebSocket clients
    asyncio.create_task(manager.broadcast(json.dumps(message)))

# Register the callback with the IoT client
iot_client.add_message_callback(handle_iot_message)

# API routes
@app.get("/")
async def root():
    return {"message": "AWS IoT Core FastAPI Web Application"}

@app.get("/status", response_model=StatusResponse)
async def status():
    iot_status = iot_client.get_topic_status()
    return StatusResponse(
        status="running",
        iot_topic=iot_status["topic"],
        connected_clients=len(manager.active_connections)
    )

@app.post("/subscribe")
async def subscribe_to_topic(request: IoTSubscriptionRequest):
    """
    Subscribe to an AWS IoT Core topic
    Note: In this implementation, we're just changing the topic in our client
    """
    global iot_client
    # Create a new client with the new topic
    iot_client = AWSIoTClient(request.topic)
    # Register the callback with the new client
    iot_client.add_message_callback(handle_iot_message)
    # Start listening for messages
    asyncio.create_task(iot_client.start_listening())
    
    return {"message": f"Subscribed to topic: {request.topic}"}

@app.post("/publish")
async def publish_message(request: IoTPublishRequest):
    """
    Publish a message to an AWS IoT Core topic
    """
    result = iot_client.publish_message(request.topic, request.message)
    if result["success"]:
        return {"message": "Message published successfully"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to publish message: {result['error']}")

# WebSocket endpoint for real-time IoT data
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep the connection alive
            # In a real implementation, you might handle client messages here
            data = await websocket.receive_text()
            # Echo the received message back to the client
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Start the IoT listener when the application starts
@app.on_event("startup")
async def startup_event():
    # Start listening for messages from AWS IoT Core
    asyncio.create_task(iot_client.start_listening())
