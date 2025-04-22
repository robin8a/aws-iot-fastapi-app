import asyncio
import json
import os
from typing import Dict, Any, List, Optional, Callable
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from awscrt import mqtt, http
from awsiot import mqtt_connection_builder

# --- Configuration ---
# Replace with your AWS IoT endpoint
ENDPOINT = "a3t35frz37six-ats.iot.us-east-1.amazonaws.com"  # Find this in your AWS IoT Core settings
CLIENT_ID = "fastapi_device_simulator"  # Choose a unique client ID
TOPIC_PUB = "colab/device/pub"
TOPIC_SUB = "ts/proy_id/predio_id/device_id"

# Ensure the paths are correctly set - you might need to adjust these
CERT_PATH = "_certs/e35e4416fb8e8f1dd201c2f2edce8a39145fbfc1d42574b55d17700e12495b85-certificate.pem.crt"
PRIVATE_KEY_PATH = "_certs//e35e4416fb8e8f1dd201c2f2edce8a39145fbfc1d42574b55d17700e12495b85-private.pem.key"
ROOT_CA_PATH = "_certs/AmazonRootCA1.pem"

# from utils.command_line_utils import CommandLineUtils

# Load environment variables
load_dotenv()

# cmdData is the arguments/input from the command line placed into a single struct for
# use in this sample. This handles all of the command line parsing, validating, etc.
# See the Utils/CommandLineUtils for more information.
# cmdData = CommandLineUtils.parse_sample_input_pubsub()

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
        # await self.simulate_message_reception()

        mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        # port=cmdData.input_port,
        cert_filepath=CERT_PATH,
        pri_key_filepath=PRIVATE_KEY_PATH,
        ca_filepath=ROOT_CA_PATH,
        on_connection_interrupted=self.on_connection_interrupted,
        on_connection_resumed=self.on_connection_resumed,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=30,
        # http_proxy_options=proxy_options,
        on_connection_success=self.on_connection_success,
        on_connection_failure=self.on_connection_failure,
        on_connection_closed=self.on_connection_closed)

        
        
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

    # Callback when connection is accidentally lost.
    def on_connection_interrupted(connection, error, **kwargs):
        print("Connection interrupted. error: {}".format(error))

    # Callback when an interrupted connection is re-established.
    def on_connection_resumed(connection, return_code, session_present, **kwargs):
        print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

        if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
            print("Session did not persist. Resubscribing to existing topics...")
            resubscribe_future, _ = connection.resubscribe_existing_topics()

            # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
            # evaluate result with a callback instead.
            resubscribe_future.add_done_callback(on_resubscribe_complete)


    def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                print('qos is None')
                # sys.exit("Server rejected resubscribe to topic: {}".format(topic))


    # Callback when the subscribed topic receives a message
    def on_message_received(topic, payload, dup, qos, retain, **kwargs):
        print("Received message from topic '{}': {}".format(topic, payload))
        global received_count
        received_count += 1
        # if received_count == cmdData.input_count:
        #     received_all_event.set()

    # Callback when the connection successfully connects
    def on_connection_success(connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionSuccessData)
        print("Connection Successful with return code: {} session present: {}".format(callback_data.return_code, callback_data.session_present))

    # Callback when a connection attempt fails
    def on_connection_failure(connection, callback_data):
        assert isinstance(callback_data, mqtt.OnConnectionFailureData)
        print("Connection failed with error code: {}".format(callback_data.error))

    # Callback when a connection has been disconnected or shutdown successfully
    def on_connection_closed(connection, callback_data):
        print("Connection closed")
