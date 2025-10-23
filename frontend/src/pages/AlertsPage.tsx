import React, { useEffect, useState } from 'react'
import { listAlerts, subscribeToAlerts, deleteAlert, Alert } from '../services/api'
import { Plus, Trash2 } from 'lucide-react'

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    alert_type: 'risk_increase',
    threshold: 70,
  })

  useEffect(() => {
    fetchAlerts()
  }, [])

  const fetchAlerts = async () => {
    setLoading(true)
    try {
      const response = await listAlerts()
      setAlerts(response.data)
    } catch (err) {
      setError('Failed to load alerts')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await subscribeToAlerts(
        formData.email,
        formData.alert_type,
        undefined,
        formData.threshold
      )
      setFormData({ email: '', alert_type: 'risk_increase', threshold: 70 })
      setShowForm(false)
      await fetchAlerts()
    } catch (err) {
      setError('Failed to create alert')
      console.error(err)
    }
  }

  const handleDeleteAlert = async (id: string) => {
    try {
      await deleteAlert(id)
      await fetchAlerts()
    } catch (err) {
      setError('Failed to delete alert')
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
        <h1 className="text-3xl font-bold">Alerts</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus size={20} />
          New Alert
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {showForm && (
        <form onSubmit={handleCreateAlert} className="bg-white p-6 rounded-lg shadow-md space-y-4">
          <input
            type="email"
            placeholder="Email address"
            value={formData.email}
            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            required
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <select
            value={formData.alert_type}
            onChange={(e) => setFormData({ ...formData, alert_type: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="risk_increase">Risk Increase</option>
            <option value="news">New News</option>
            <option value="sentiment">Sentiment Change</option>
          </select>
          {formData.alert_type === 'risk_increase' && (
            <input
              type="number"
              placeholder="Risk threshold"
              value={formData.threshold}
              onChange={(e) => setFormData({ ...formData, threshold: parseFloat(e.target.value) })}
              min="0"
              max="100"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          )}
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

      {alerts.length > 0 ? (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <div key={alert.id} className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
              <div>
                <p className="font-semibold text-gray-900">{alert.email}</p>
                <p className="text-gray-600 text-sm">
                  Type: {alert.alert_type}
                  {alert.threshold && ` • Threshold: ${alert.threshold}`}
                </p>
                <p className="text-gray-500 text-xs mt-1">
                  Created: {new Date(alert.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                onClick={() => handleDeleteAlert(alert.id)}
                className="text-red-600 hover:text-red-800 p-2"
              >
                <Trash2 size={20} />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-600">
          No alerts yet. Create one to get started!
        </div>
      )}
    </div>
  )
}

