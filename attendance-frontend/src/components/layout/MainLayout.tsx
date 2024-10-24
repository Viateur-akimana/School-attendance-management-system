export const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
      <div className="flex min-h-screen bg-gray-100">
        <Sidebar />
        <div className="flex-1 ml-64">
          <Header />
          <main className="p-6 mt-16">{children}</main>
        </div>
      </div>
    );
  };
  