
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import TopicPage from "./pages/TopicPage";
import LessonPage from "./pages/LessonPage";
import Profile from "./pages/Profile";
import NewsFeed from "./pages/NewsFeed";
import Lessons from "./pages/Lessons";
import Community from "./pages/Community";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/news" element={<NewsFeed />} />
          <Route path="/lessons" element={<Lessons />} />
          <Route path="/community" element={<Community />} />
          <Route path="/topic/:topicId" element={<TopicPage />} />
          <Route path="/lesson/:topicId/:lessonId" element={<LessonPage />} />
          <Route path="/profile" element={<Profile />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
