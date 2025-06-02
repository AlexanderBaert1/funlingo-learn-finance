
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface NavbarProps {
  progress?: number;
  streak?: number;
  gems?: number;
}

export function Navbar({ progress = 0, streak = 0, gems = 0 }: NavbarProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-white shadow-md py-2 px-4">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo and Progress Section */}
        <div className="flex items-center gap-4">
          <Link to="/" className="flex items-center">
            <span className="text-[#3D99EC] text-2xl font-bold">Fin<span className="text-[#4CA35A]">lingo</span></span>
          </Link>
          
          {/* Daily Progress */}
          <div className="hidden sm:flex items-center gap-2">
            <Progress value={progress} className="w-32 h-2.5 bg-gray-200" />
            <span className="text-sm font-medium">{progress}%</span>
          </div>
        </div>
        
        {/* Streak & Gems - Middle for mobile, right for desktop */}
        <div className="flex items-center gap-6">
          {/* Streak */}
          <div className="flex items-center">
            <div className="bg-[#3D99EC]/10 p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#3D99EC" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M14.5 4.5 12 2 9.5 4.5"></path>
                <path d="m18 6-2-2"></path>
                <path d="m8 6-2 2"></path>
                <path d="M13.4 10H15a2 2 0 1 1 0 4h-4a1 1 0 0 0-1 1 1 1 0 0 0 1 1h4a4 4 0 1 0 0-8h-1.6"></path>
                <path d="M9 15v1"></path>
                <path d="M9 8v1"></path>
                <path d="M9 12h12"></path>
              </svg>
            </div>
            <span className="ml-1 font-semibold text-sm">{streak}</span>
          </div>
          
          {/* Gems */}
          <div className="flex items-center">
            <div className="bg-[#4CA35A]/10 p-2 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#4CA35A" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M6 3h12l4 6-10 13L2 9Z"></path>
                <path d="M12 22V9"></path>
                <path d="m12 9 4-6"></path>
                <path d="m12 9-4-6"></path>
              </svg>
            </div>
            <span className="ml-1 font-semibold text-sm">{gems}</span>
          </div>
          
          {/* Profile / Login Button */}
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </Button>
          
          {isMenuOpen && (
            <div className="absolute top-14 right-4 bg-white shadow-lg rounded-lg py-2 z-10 min-w-[150px]">
              <Link to="/profile" className="block px-4 py-2 hover:bg-gray-100">Profile</Link>
              <Link to="/settings" className="block px-4 py-2 hover:bg-gray-100">Settings</Link>
              <div className="border-t my-1"></div>
              <button className="w-full text-left px-4 py-2 hover:bg-gray-100">Logout</button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
