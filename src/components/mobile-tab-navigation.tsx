
import { useState } from 'react';
import { Home, BookOpen, Users } from 'lucide-react';

interface MobileTabNavigationProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export function MobileTabNavigation({ activeTab, onTabChange }: MobileTabNavigationProps) {
  const tabs = [
    { id: 'news', label: 'News', icon: Home },
    { id: 'lessons', label: 'Lessons', icon: BookOpen },
    { id: 'community', label: 'Community', icon: Users },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2 z-50">
      <div className="flex justify-around">
        {tabs.map((tab) => {
          const IconComponent = tab.icon;
          const isActive = activeTab === tab.id;
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col items-center py-2 px-4 rounded-lg transition-colors ${
                isActive 
                  ? 'text-finlingo-primary bg-finlingo-primary/10' 
                  : 'text-gray-500'
              }`}
            >
              <IconComponent size={24} />
              <span className="text-xs mt-1 font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
