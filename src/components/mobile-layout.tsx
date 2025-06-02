
import { useState } from 'react';
import { MobileTabNavigation } from './mobile-tab-navigation';
import NewsFeed from '@/pages/NewsFeed';
import Lessons from '@/pages/Lessons';
import Community from '@/pages/Community';

export function MobileLayout() {
  const [activeTab, setActiveTab] = useState('lessons');

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'news':
        return <NewsFeed />;
      case 'lessons':
        return <Lessons />;
      case 'community':
        return <Community />;
      default:
        return <Lessons />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {renderActiveTab()}
      <MobileTabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
}
