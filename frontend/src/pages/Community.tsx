
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { MessageSquare, Users, Trophy, Plus } from 'lucide-react';

const Community = () => {
  const communityGroups = [
    {
      id: 1,
      name: "Beginner Investors",
      members: 1247,
      description: "A supportive space for those just starting their investment journey",
      recent: "Active 2 minutes ago"
    },
    {
      id: 2,
      name: "Budget Masters",
      members: 892,
      description: "Share tips and tricks for managing your money effectively",
      recent: "Active 15 minutes ago"
    },
    {
      id: 3,
      name: "Debt-Free Journey",
      members: 634,
      description: "Support group for those working towards becoming debt-free",
      recent: "Active 1 hour ago"
    }
  ];

  const topContributors = [
    { name: "Alex Rivera", points: 2450, badge: "🏆" },
    { name: "Sam Park", points: 1890, badge: "🥈" },
    { name: "Jordan Lee", points: 1560, badge: "🥉" },
  ];

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <div className="bg-white shadow-sm p-4 sticky top-0 z-10">
        <h1 className="text-xl font-bold text-center">Community</h1>
      </div>
      
      <div className="container mx-auto px-4 py-4 space-y-6">
        {/* Quick Stats */}
        <Card>
          <CardContent className="p-4">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="flex items-center justify-center mb-1">
                  <Users className="text-finlingo-primary" size={20} />
                </div>
                <p className="text-lg font-bold">3.2k</p>
                <p className="text-xs text-gray-500">Members</p>
              </div>
              <div>
                <div className="flex items-center justify-center mb-1">
                  <MessageSquare className="text-finlingo-secondary" size={20} />
                </div>
                <p className="text-lg font-bold">847</p>
                <p className="text-xs text-gray-500">Discussions</p>
              </div>
              <div>
                <div className="flex items-center justify-center mb-1">
                  <Trophy className="text-yellow-500" size={20} />
                </div>
                <p className="text-lg font-bold">156</p>
                <p className="text-xs text-gray-500">Achievements</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Top Contributors */}
        <Card>
          <CardContent className="p-4">
            <h3 className="font-bold mb-3">Top Contributors This Week</h3>
            <div className="space-y-3">
              {topContributors.map((contributor, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-lg">{contributor.badge}</span>
                    <div>
                      <p className="font-semibold text-sm">{contributor.name}</p>
                      <p className="text-xs text-gray-500">{contributor.points} points</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Community Groups */}
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-bold text-lg">Popular Groups</h3>
          <Button size="sm" className="bg-finlingo-primary">
            <Plus size={16} className="mr-1" />
            Join
          </Button>
        </div>
        
        <div className="space-y-4">
          {communityGroups.map((group) => (
            <Card key={group.id}>
              <CardContent className="p-4">
                <div className="flex items-start justify-between mb-2">
                  <h4 className="font-semibold">{group.name}</h4>
                  <span className="text-xs text-gray-500">{group.members} members</span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{group.description}</p>
                <div className="flex items-center justify-between">
                  <span className="text-xs text-green-600">{group.recent}</span>
                  <Button size="sm" variant="outline">
                    Join Group
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Community;
