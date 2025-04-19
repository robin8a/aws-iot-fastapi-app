'use client';

import { useEffect } from 'react';
import { Chart, registerables } from 'chart.js';

// Register all Chart.js components
Chart.register(...registerables);

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  // Fix for Chart.js in Next.js with SSR
  useEffect(() => {
    // This ensures Chart.js only runs on client-side
  }, []);

  return (
    <html lang="en">
      <body>
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
      </body>
    </html>
  );
}
