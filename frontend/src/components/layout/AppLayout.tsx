import React from 'react';
import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export const AppLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-bg flex flex-col lg:flex-row">
      {/* Sidebar — desktop only */}
      <Sidebar />

      {/* Mobile Navbar */}
      <div className="lg:hidden">
        <Navbar />
      </div>

      {/* Main content - Flex item that naturally avoids the sticky sidebar */}
      <main className="flex-1 pt-16 lg:pt-0 min-h-screen flex flex-col min-w-0">
        <div className="p-4 sm:p-6 lg:p-10 w-full max-w-7xl mx-auto flex-1">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
