export const Header = () => {
    const { user } = useAuth();
    
    return (
      <header className="h-16 bg-white border-b flex items-center justify-between px-6 fixed top-0 right-0 left-64">
        <div className="flex items-center">
          <h2 className="text-xl font-semibold text-gray-800">
            Welcome, {user?.firstName}
          </h2>
        </div>
        
        <div className="flex items-center space-x-4">
          <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-full">
            <Bell className="w-6 h-6" />
            <span className="absolute top-0 right-0 h-4 w-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
              3
            </span>
          </button>
          
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gray-300 rounded-full"></div>
            <span className="text-sm text-gray-700">{user?.username}</span>
          </div>
        </div>
      </header>
    );
  };