from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class IoTMessage(BaseModel):
    """Model for IoT messages received from AWS IoT Core"""
    device_id: str
    timestamp: datetime
    data: Dict[str, Any]
    
class IoTSubscriptionRequest(BaseModel):
    """Model for IoT subscription requests"""
    topic: str
    
class IoTPublishRequest(BaseModel):
    """Model for IoT publish requests"""
    topic: str
    message: Dict[str, Any]
    
class StatusResponse(BaseModel):
    """Model for API status responses"""
    status: str
    iot_topic: str
    connected_clients: Optional[int] = 0
