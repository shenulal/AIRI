import React from 'react'
import { Link } from 'react-router-dom'
import { TrendingUp, AlertCircle, BookmarkIcon } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          AI Insights & Risk Intelligence Platform
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Real-time company intelligence, sentiment analysis, and risk scoring
        </p>
        <Link
          to="/search"
          className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700"
        >
          Start Searching
        </Link>
      </section>

      {/* Features Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <TrendingUp className="text-blue-600 mb-4" size={32} />
          <h3 className="text-xl font-semibold mb-2">Risk Scoring</h3>
          <p className="text-gray-600">
            Hybrid rule-based and ML-powered risk scores updated in real-time
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <AlertCircle className="text-blue-600 mb-4" size={32} />
          <h3 className="text-xl font-semibold mb-2">Smart Alerts</h3>
          <p className="text-gray-600">
            Get notified of significant changes in company risk and sentiment
          </p>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <BookmarkIcon className="text-blue-600 mb-4" size={32} />
          <h3 className="text-xl font-semibold mb-2">Watchlists</h3>
          <p className="text-gray-600">
            Track multiple companies and monitor their performance over time
          </p>
        </div>
      </section>

      {/* Info Section */}
      <section className="bg-blue-50 p-8 rounded-lg">
        <h2 className="text-2xl font-bold mb-4">How It Works</h2>
        <ul className="space-y-3 text-gray-700">
          <li className="flex items-start gap-3">
            <span className="font-bold text-blue-600">1.</span>
            <span>Search for companies by name or ticker</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="font-bold text-blue-600">2.</span>
            <span>View detailed profiles with risk scores and sentiment analysis</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="font-bold text-blue-600">3.</span>
            <span>Add companies to watchlists for continuous monitoring</span>
          </li>
          <li className="flex items-start gap-3">
            <span className="font-bold text-blue-600">4.</span>
            <span>Subscribe to alerts for important changes</span>
          </li>
        </ul>
      </section>
    </div>
  )
}

