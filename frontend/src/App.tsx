import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import { AuthProvider, isReviewer, useAuth } from './auth';
import { Link } from './components/ui';
import { HomePage } from './pages/HomePage';
import { JobPage } from './pages/JobPage';
import { LoginPage } from './pages/LoginPage';
import { ReviewPage, ReviewQueuePage } from './pages/ReviewPages';
import { useRoute } from './router';

function Shell() {
  const { user, loading, logout } = useAuth();
  const route = useRoute();

  if (loading) return <p className="p-6 text-sm text-slate-400">Loading…</p>;
  if (!user) return <LoginPage />;

  const reviewer = isReviewer(user);
  let page;
  switch (route.name) {
    case 'home':
      page = <HomePage />;
      break;
    case 'job':
      page = <JobPage jobId={route.jobId} />;
      break;
    case 'reviews':
      page = reviewer ? <ReviewQueuePage /> : <p>Reviewer role required.</p>;
      break;
    case 'review':
      page = reviewer ? <ReviewPage extractionId={route.extractionId} /> : <p>Reviewer role required.</p>;
      break;
    default:
      page = <p>Page not found.</p>;
  }

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-800 bg-slate-950">
        <nav className="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3 text-sm">
          <span className="font-semibold">DocuTask Agent</span>
          <Link to="/">Jobs</Link>
          {reviewer && <Link to="/reviews">Review queue</Link>}
          <span className="ml-auto text-slate-400">
            {user.username} ({user.role})
          </span>
          <button className="text-slate-300 hover:text-white" onClick={() => logout()}>
            Sign out
          </button>
        </nav>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-6">{page}</main>
    </div>
  );
}

export default function App() {
  const [queryClient] = useState(
    () => new QueryClient({ defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } } }),
  );
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Shell />
      </AuthProvider>
    </QueryClientProvider>
  );
}
