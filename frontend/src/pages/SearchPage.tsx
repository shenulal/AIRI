import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Search as SearchIcon, AlertTriangle } from 'lucide-react'
import { searchCompanies, Company } from '../services/api'

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Company[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError('')
    try {
      const response = await searchCompanies(query)
      setResults(response.data.results)
    } catch (err) {
      setError('Failed to search companies')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return 'text-green-600'
    if (score < 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-4">Search Companies</h1>
        
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by company name or ticker..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 flex items-center gap-2"
          >
            <SearchIcon size={20} />
            Search
          </button>
        </form>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {loading && (
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <p className="mt-2 text-gray-600">Searching...</p>
        </div>
      )}

      {results.length > 0 && (
        <div className="space-y-4">
          <p className="text-gray-600">Found {results.length} companies</p>
          {results.map((company) => (
            <Link
              key={company.id}
              to={`/companies/${company.id}`}
              className="block bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {company.name}
                    {company.ticker && <span className="text-gray-500 ml-2">({company.ticker})</span>}
                  </h3>
                  {company.industry && (
                    <p className="text-gray-600 mt-1">{company.industry}</p>
                  )}
                  {company.description && (
                    <p className="text-gray-600 mt-2 line-clamp-2">{company.description}</p>
                  )}
                </div>
                <div className="ml-4 text-right">
                  <div className="flex items-center gap-2 justify-end">
                    <AlertTriangle size={20} className={getRiskColor(company.risk_score)} />
                    <div>
                      <p className="text-sm text-gray-600">Risk Score</p>
                      <p className={`text-2xl font-bold ${getRiskColor(company.risk_score)}`}>
                        {company.risk_score.toFixed(1)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}

      {!loading && results.length === 0 && query && (
        <div className="text-center py-8 text-gray-600">
          No companies found for "{query}"
        </div>
      )}

      {!loading && results.length === 0 && !query && (
        <div className="text-center py-8 text-gray-600">
          Enter a company name or ticker to search
        </div>
      )}
    </div>
  )
}

