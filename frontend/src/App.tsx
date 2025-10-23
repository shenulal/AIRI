import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import SearchPage from './pages/SearchPage'
import CompanyProfilePage from './pages/CompanyProfilePage'
import WatchlistsPage from './pages/WatchlistsPage'
import AlertsPage from './pages/AlertsPage'
import HomePage from './pages/HomePage'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/companies/:id" element={<CompanyProfilePage />} />
            <Route path="/watchlists" element={<WatchlistsPage />} />
            <Route path="/alerts" element={<AlertsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

