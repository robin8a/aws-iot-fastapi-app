import asyncio
import json
import os
from typing import Dict, Any, List, Optional, Callable
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AWSIoTClient:
    """
    Client for interacting with AWS IoT Core
    """
    def __init__(self, topic: str):
        # Get AWS credentials from environment variables
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self.topic = topic
        self.callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        # Initialize the IoT data client
        self.client = boto3.client(
            'iot-data',
            region_name=self.region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    
    def publish_message(self, topic: Optional[str] = None, message: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Publish a message to an AWS IoT topic
        
        Args:
            topic: The topic to publish to (defaults to the client's topic)
            message: The message to publish
            
        Returns:
            The response from AWS IoT Core
        """
        if topic is None:
            topic = self.topic
            
        if message is None:
            return {"success": False, "error": "No message provided"}
            
        try:
            response = self.client.publish(
                topic=topic,
                qos=1,
                payload=json.dumps(message)
            )
            return {"success": True, "response": response}
        except ClientError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def add_message_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Add a callback function to be called when a message is received
        
        Args:
            callback: The callback function to call when a message is received
        """
        self.callbacks.append(callback)
    
    async def simulate_message_reception(self, interval: int = 18):
        """
        Simulate receiving messages from AWS IoT Core
        This is a placeholder for testing purposes
        
        In a real implementation, you would use AWS IoT Device SDK with MQTT
        or AWS IoT Core with WebSockets to receive messages
        
        Args:
            interval: The interval in seconds between simulated messages
        """
        while True:
            try:
                # Simulate a message from AWS IoT Core
                message = {
                    "device_id": "test-device-001",
                    "timestamp": asyncio.get_event_loop().time(),
                    "data": {
                        "temperature": 22.5 + (asyncio.get_event_loop().time() % 5),
                        "humidity": 45.2 + (asyncio.get_event_loop().time() % 10),
                        "pressure": 1013.2 + (asyncio.get_event_loop().time() % 20)
                    }
                }
                
                # Call all registered callbacks with the message
                for callback in self.callbacks:
                    callback(message)
                    
                await asyncio.sleep(interval)
            except Exception as e:
                print(f"Error in simulate_message_reception: {e}")
                await asyncio.sleep(interval)
    
    async def start_listening(self):
        """
        Start listening for messages from AWS IoT Core
        
        In a real implementation, this would connect to AWS IoT Core
        using MQTT or WebSockets and set up the necessary callbacks
        
        For this example, we'll use the simulation method
        """
        # For testing purposes, we'll use the simulation method
        await self.simulate_message_reception()
        
    def get_topic_status(self) -> Dict[str, Any]:
        """
        Get the status of the topic subscription
        
        Returns:
            A dictionary with the status information
        """
        return {
            "topic": self.topic,
            "connected": True,  # In a real implementation, this would be determined by the connection state
            "callbacks_registered": len(self.callbacks)
        }
