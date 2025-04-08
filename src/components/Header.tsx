import React from 'react';

const Header: React.FC = () => {
  return (
    <div className="flex justify-center items-center py-4 bg-white shadow-md">
      <img
        src="@/public/logo.ico" // Replace with the path to your logo
        className="h-12" // Adjust the height as needed
      />
    </div>
  );
};

export default Header;