'use client';

import { useState, useEffect, useRef } from 'react';
import { StatusCard, TopicSubscription } from '../components/ui';
import { DataChart, MessageLog } from '../components/data-display';

export default function IoTDashboard() {
  const [connected, setConnected] = useState(false);
  const [messages, setMessages] = useState([]);
  const [topic, setTopic] = useState('test/topic');
  const [status, setStatus] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const wsRef = useRef(null);
  const maxMessages = 20;

  // Connect to WebSocket
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8001/ws');
      
      ws.onopen = () => {
        console.log('WebSocket connected');
        setConnected(true);
        ws.send(JSON.stringify({ action: 'subscribe', topic }));
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setMessages(prev => {
            const newMessages = [...prev, data];
            // Keep only the last maxMessages
            return newMessages.slice(-maxMessages);
          });
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
        }
      };
      
      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setConnected(false);
        // Try to reconnect after a delay
        setTimeout(connectWebSocket, 3000);
      };
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('WebSocket connection error');
      };
      
      wsRef.current = ws;
    };
    
    connectWebSocket();
    
    // Cleanup function
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [topic]);
  
  // Fetch API status
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await fetch('http://localhost:8001/status');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        setStatus(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching status:', error);
        setError('Failed to fetch API status');
        setIsLoading(false);
      }
    };
    
    fetchStatus();
    // Refresh status every 10 seconds
    const intervalId = setInterval(fetchStatus, 10000);
    
    return () => clearInterval(intervalId);
  }, []);
  
  // Subscribe to a new topic
  const handleSubscribe = async () => {
    try {
      const response = await fetch('http://localhost:8001/subscribe', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic }),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Subscription response:', data);
      
      // Reset messages when subscribing to a new topic
      setMessages([]);
      
      // Reconnect WebSocket
      if (wsRef.current) {
        wsRef.current.close();
      }
    } catch (error) {
      console.error('Error subscribing to topic:', error);
      setError('Failed to subscribe to topic');
    }
  };
  
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">AWS IoT Core Dashboard</h1>
      
      {/* Status Card */}
      <StatusCard 
        status={status}
        connected={connected}
        isLoading={isLoading}
        error={error}
      />
      
      {/* Topic Subscription */}
      <TopicSubscription 
        topic={topic}
        setTopic={setTopic}
        handleSubscribe={handleSubscribe}
      />
      
      {/* Chart */}
      <DataChart messages={messages} />
      
      {/* Message Log */}
      <MessageLog messages={messages} />
    </div>
  );
}
