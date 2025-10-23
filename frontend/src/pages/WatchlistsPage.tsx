import React, { useEffect, useState } from 'react'
import { listWatchlists, createWatchlist, Watchlist } from '../services/api'
import { Plus } from 'lucide-react'

export default function WatchlistsPage() {
  const [watchlists, setWatchlists] = useState<Watchlist[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({ name: '', description: '' })

  useEffect(() => {
    fetchWatchlists()
  }, [])

  const fetchWatchlists = async () => {
    setLoading(true)
    try {
      const response = await listWatchlists()
      setWatchlists(response.data)
    } catch (err) {
      setError('Failed to load watchlists')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateWatchlist = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createWatchlist(formData.name, formData.description)
      setFormData({ name: '', description: '' })
      setShowForm(false)
      await fetchWatchlists()
    } catch (err) {
      setError('Failed to create watchlist')
      console.error(err)
    }
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Loading...</p>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Watchlists</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus size={20} />
          New Watchlist
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {showForm && (
        <form onSubmit={handleCreateWatchlist} className="bg-white p-6 rounded-lg shadow-md space-y-4">
          <input
            type="text"
            placeholder="Watchlist name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <textarea
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
          />
          <div className="flex gap-2">
            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Create
            </button>
            <button
              type="button"
              onClick={() => setShowForm(false)}
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </form>
      )}

      {watchlists.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {watchlists.map((watchlist) => (
            <div key={watchlist.id} className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-2">{watchlist.name}</h3>
              {watchlist.description && (
                <p className="text-gray-600 mb-4">{watchlist.description}</p>
              )}
              <p className="text-sm text-gray-500">
                {watchlist.items.length} companies
              </p>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-600">
          No watchlists yet. Create one to get started!
        </div>
      )}
    </div>
  )
}

