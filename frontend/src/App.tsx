import { Routes, Route, useNavigate } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { UploadPage } from './pages/UploadPage';
import { JobResultsPage } from './components/JobResultsPage';

function App() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-white dark:bg-slate-900">
      <Routes>
        {/* Public routes without navbar (auth pages) */}
        <Route
          path="/login"
          element={
            <ProtectedRoute requireAuth={false}>
              <LoginPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/register"
          element={
            <ProtectedRoute requireAuth={false}>
              <RegisterPage />
            </ProtectedRoute>
          }
        />

        {/* Public routes with navbar */}
        <Route
          path="/"
          element={
            <>
              <Navbar />
              <HomePage onMatchesComplete={() => navigate('/matches')} />
            </>
          }
        />
        <Route
          path="/upload"
          element={
            <>
              <Navbar />
              <UploadPage />
            </>
          }
        />
        <Route
          path="/jobs"
          element={
            <>
              <Navbar />
              <main className="pt-16">
                <JobResultsPage />
              </main>
            </>
          }
        />
        <Route
          path="/matches"
          element={
            <>
              <Navbar />
              <main className="pt-16">
                <JobResultsPage />
              </main>
            </>
          }
        />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <DashboardPage />
              </>
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <main className="pt-16 pl-64">
                  <div className="p-8">
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Profile</h1>
                    <p className="text-slate-600 dark:text-slate-400 mt-2">Coming soon...</p>
                  </div>
                </main>
              </>
            </ProtectedRoute>
          }
        />
        <Route
          path="/resumes"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <main className="pt-16 pl-64">
                  <div className="p-8">
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">My Resumes</h1>
                    <p className="text-slate-600 dark:text-slate-400 mt-2">Coming soon...</p>
                  </div>
                </main>
              </>
            </ProtectedRoute>
          }
        />
        <Route
          path="/skill-gap"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <main className="pt-16 pl-64">
                  <div className="p-8">
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Skill Gap Analysis</h1>
                    <p className="text-slate-600 dark:text-slate-400 mt-2">Coming soon...</p>
                  </div>
                </main>
              </>
            </ProtectedRoute>
          }
        />
        <Route
          path="/insights"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <main className="pt-16 pl-64">
                  <div className="p-8">
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Career Insights</h1>
                    <p className="text-slate-600 dark:text-slate-400 mt-2">Coming soon...</p>
                  </div>
                </main>
              </>
            </ProtectedRoute>
          }
        />
        <Route
          path="/settings"
          element={
            <ProtectedRoute>
              <>
                <Navbar />
                <main className="pt-16 pl-64">
                  <div className="p-8">
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Settings</h1>
                    <p className="text-slate-600 dark:text-slate-400 mt-2">Coming soon...</p>
                  </div>
                </main>
              </>
            </ProtectedRoute>
          }
        />

        {/* Catch all */}
        <Route
          path="*"
          element={
            <>
              <Navbar />
              <main className="pt-16 flex items-center justify-center min-h-[80vh]">
                <div className="text-center">
                  <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-4">404</h1>
                  <p className="text-slate-600 dark:text-slate-400">Page not found</p>
                </div>
              </main>
            </>
          }
        />
      </Routes>
    </div>
  );
}

export default App;
