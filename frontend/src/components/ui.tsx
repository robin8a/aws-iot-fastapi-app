'use client';

import React from 'react';

interface WebSocketStatusProps {
  connected: boolean;
}

export const WebSocketStatus: React.FC<WebSocketStatusProps> = ({ connected }) => {
  return (
    <div className="flex items-center">
      <div 
        className={`w-3 h-3 rounded-full mr-2 ${connected ? 'bg-green-500' : 'bg-red-500'}`}
      ></div>
      <span className={`text-sm ${connected ? 'text-green-600' : 'text-red-600'}`}>
        {connected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  );
};

interface MessageCardProps {
  message: any;
  index: number;
}

export const MessageCard: React.FC<MessageCardProps> = ({ message, index }) => {
  return (
    <div className="border-b py-2 last:border-b-0">
      <div className="flex justify-between text-sm">
        <span className="font-medium">Device: {message.device_id}</span>
        <span className="text-gray-500">Message {index + 1}</span>
      </div>
      <pre className="text-xs bg-gray-100 p-2 mt-1 rounded overflow-x-auto">
        {JSON.stringify(message, null, 2)}
      </pre>
    </div>
  );
};

interface TopicSubscriptionProps {
  topic: string;
  setTopic: (topic: string) => void;
  handleSubscribe: () => void;
}

export const TopicSubscription: React.FC<TopicSubscriptionProps> = ({ 
  topic, 
  setTopic, 
  handleSubscribe 
}) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      <h2 className="text-xl font-semibold mb-2">Topic Subscription</h2>
      <div className="flex flex-col md:flex-row gap-2">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="flex-grow p-2 border rounded"
          placeholder="Enter topic name"
        />
        <button
          onClick={handleSubscribe}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Subscribe
        </button>
      </div>
    </div>
  );
};

interface StatusCardProps {
  status: any;
  connected: boolean;
  isLoading: boolean;
  error: string | null;
}

export const StatusCard: React.FC<StatusCardProps> = ({ 
  status, 
  connected, 
  isLoading, 
  error 
}) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-4 mb-6">
      <h2 className="text-xl font-semibold mb-2">Connection Status</h2>
      {isLoading ? (
        <p>Loading status...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <p className="text-gray-600">API Status:</p>
            <p className="font-medium">{status.status || 'Unknown'}</p>
          </div>
          <div>
            <p className="text-gray-600">Current Topic:</p>
            <p className="font-medium">{status.iot_topic || 'None'}</p>
          </div>
          <div>
            <p className="text-gray-600">WebSocket:</p>
            <WebSocketStatus connected={connected} />
          </div>
        </div>
      )}
    </div>
  );
};
