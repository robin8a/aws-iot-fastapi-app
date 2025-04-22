# AWS IoT Core FastAPI Web Application

This web application connects to AWS IoT Core using the AWS SDK and provides a real-time dashboard for monitoring IoT data. It consists of a FastAPI backend and a Next.js frontend.

## Features

- Real-time IoT data visualization with Chart.js
- WebSocket connection for live updates
- Topic subscription functionality
- AWS IoT Core integration
- Responsive UI with Tailwind CSS

## Prerequisites

- Python 3.10+
- Node.js 16+
- npm
- AWS account with IoT Core access (optional for testing)

## Project Structure

```
aws-iot-fastapi-app/
├── backend/                # FastAPI backend
│   ├── certs/              # AWS IoT certifications .crt, RootCA .pem, Keys .key
│   ├── venv/               # Python virtual environment
│   ├── main.py             # Main FastAPI application
│   ├── aws_iot.py          # AWS IoT Core client
│   ├── models.py           # Pydantic models
│   ├── requirements.txt    # Python dependencies
│   ├── .env.example        # Example environment variables
│   └── start.sh            # Backend start script
├── frontend/               # Next.js frontend
│   ├── src/                # Source code
│   │   ├── app/            # Next.js app directory
│   │   │   ├── page.tsx    # Main dashboard page
│   │   │   └── layout.tsx  # App layout
│   │   └── components/     # React components
│   ├── public/             # Static files
│   └── start.sh            # Frontend start script
├── start_app.sh            # Script to start both backend and frontend
├── stop_app.sh             # Script to stop all running servers
├── test.sh                 # Test script for API endpoints
└── test_aws_iot.sh         # Test script for AWS IoT Core client
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/robin8a/aws-iot-fastapi-app.git
cd aws-iot-fastapi-app
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials (for production use)
cp .env.example .env
# Edit .env with your AWS credentials and IoT topic
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Replace

- /Users/robinochoa/Documents/fast_api_ws for your own path in .sh files

### Option 1: Using the start_app.sh Script

This script starts both the backend and frontend servers:

```bash
./start_app.sh
```

The application will be available at:

- [Backend](http://localhost:8001)
- [Frontend](http://localhost:3000)

### Option 2: Starting Servers Separately

#### Start the Backend

```bash
cd backend
source venv/bin/activate
./start.sh
```

#### Start the Frontend

```bash
cd frontend
./start.sh
```

## Stopping the Application

To stop all running servers:

```bash
./stop_app.sh
```

## Testing

### Test API Endpoints and WebSocket

```bash
./test.sh
```

### Test AWS IoT Core Client

```bash
./test_aws_iot.sh
```

## API Endpoints

- `GET /`: Root endpoint
- `GET /status`: Get application status
- `POST /subscribe`: Subscribe to an IoT topic
- `POST /publish`: Publish a message to an IoT topic
- `WebSocket /ws`: WebSocket endpoint for real-time updates

## AWS IoT Core Configuration

For production use, you need to configure AWS credentials in the `.env` file:

```
AWS_IOT_TOPIC=your/topic/name
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

## Development Mode

The application runs in simulation mode if AWS credentials are not provided, generating test data for development and testing purposes.

## Customization

### Changing the IoT Topic

1. Update the `AWS_IOT_TOPIC` in the `.env` file
2. Restart the backend server
3. Use the topic subscription form in the UI to subscribe to the new topic

### Adding New Sensor Data Types

1. Modify the `aws_iot.py` file to include new data fields
2. Update the chart components in the frontend to display the new data

## Troubleshooting

### Backend Issues

- Check the backend logs: `backend/backend.log`
- Ensure AWS credentials are correctly configured (if using real AWS IoT Core)
- Verify that the required ports (8000 for backend) are available

### Frontend Issues

- Check the frontend logs: `frontend/frontend.log`
- Ensure all dependencies are installed: `cd frontend && npm install`
- Verify that the required ports (3000 for frontend) are available

### WebSocket Connection Issues

- Ensure the backend server is running
- Check browser console for WebSocket errors
- Verify that your network allows WebSocket connections
