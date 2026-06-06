import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { LayoutDashboard, Dumbbell, Users, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const navItems = [
  { to: '/admin', icon: LayoutDashboard, label: 'Overview', end: true },
  { to: '/admin/exercises', icon: Dumbbell, label: 'Exercises' },
  { to: '/admin/users', icon: Users, label: 'Users' },
];

export const AdminLayout: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-bg flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border p-6 hidden md:flex flex-col">
        <div className="mb-8">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-text-muted hover:text-text-primary transition-colors text-sm mb-4"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to App
          </button>
          <h2 className="text-lg font-heading font-bold text-text-primary">Admin Panel</h2>
        </div>

        <nav className="space-y-1 flex-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-primary/10 text-primary-light border border-primary/20'
                    : 'text-text-muted hover:text-text-primary hover:bg-white/[0.03]'
                }`
              }
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Content */}
      <main className="flex-1 p-6 md:p-8 overflow-auto">
        <Outlet />
      </main>
    </div>
  );
};
