export const Card: React.FC<{
    title?: string;
    children: React.ReactNode;
    className?: string;
  }> = ({ title, children, className = '' }) => {
    return (
      <div className={`bg-white rounded-lg shadow p-6 ${className}`}>
        {title && <h3 className="text-lg font-semibold mb-4">{title}</h3>}
        {children}
      </div>
    );
  };
  