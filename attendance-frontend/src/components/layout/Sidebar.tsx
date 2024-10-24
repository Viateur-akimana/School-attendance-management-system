import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { 
  Home, Users, BookOpen, Calendar, FileText, 
  Settings, Bell, LogOut 
} from 'lucide-react';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  const navigation = [
    { name: 'Dashboard', path: '/dashboard', icon: Home },
    { name: 'Students', path: '/students', icon: Users },
    { name: 'Classes', path: '/classes', icon: BookOpen },
    { name: 'Attendance', path: '/attendance', icon: Calendar },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <div className="h-screen w-64 bg-gray-800 text-white fixed left-0 top-0">
      <div className="p-4">
        <h1 className="text-xl font-bold">School Attendance</h1>
      </div>
      
      <nav className="mt-8">
        {navigation.map((item) => {
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center px-6 py-3 text-sm ${
                isActive(item.path)
                  ? 'bg-gray-900 text-white'
                  : 'text-gray-300 hover:bg-gray-700'
              }`}
            >
              <Icon className="w-5 h-5 mr-3" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-0 w-full p-4">
        <button
          onClick={logout}
          className="flex items-center px-6 py-3 text-sm text-gray-300 hover:bg-gray-700 w-full"
        >
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </div>
    </div>
  );
};