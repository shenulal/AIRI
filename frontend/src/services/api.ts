import axios from 'axios'

const API_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Company {
  id: string
  name: string
  ticker?: string
  industry?: string
  country?: string
  website?: string
  description?: string
  risk_score: number
  executive_summary?: string
  created_at: string
  updated_at: string
}

export interface Document {
  id: string
  company_id: string
  title: string
  content: string
  source: string
  source_url?: string
  sentiment_score?: number
  sentiment_label?: string
  ingested_at: string
}

export interface Watchlist {
  id: string
  user_id: string
  name: string
  description?: string
  items: any[]
  created_at: string
  updated_at: string
}

export interface Alert {
  id: string
  user_id: string
  email: string
  alert_type: string
  threshold?: number
  is_active: boolean
  created_at: string
}

// Companies
export const searchCompanies = (query: string, skip = 0, limit = 10) =>
  api.get('/search/companies', { params: { q: query, skip, limit } })

export const getCompany = (id: string) =>
  api.get(`/companies/${id}`)

export const getCompanyDocuments = (id: string, skip = 0, limit = 20) =>
  api.get(`/companies/${id}/documents`, { params: { skip, limit } })

export const getCompanyRiskScore = (id: string) =>
  api.get(`/companies/${id}/risk-score`)

export const getCompanySummary = (id: string) =>
  api.get(`/companies/${id}/summary`)

// Watchlists
export const listWatchlists = () =>
  api.get('/watchlists')

export const createWatchlist = (name: string, description?: string) =>
  api.post('/watchlists', { name, description })

export const getWatchlist = (id: string) =>
  api.get(`/watchlists/${id}`)

export const addCompanyToWatchlist = (watchlistId: string, companyId: string) =>
  api.post(`/watchlists/${watchlistId}/companies`, { company_id: companyId })

export const removeCompanyFromWatchlist = (watchlistId: string, companyId: string) =>
  api.delete(`/watchlists/${watchlistId}/companies/${companyId}`)

// Alerts
export const listAlerts = () =>
  api.get('/alerts')

export const subscribeToAlerts = (email: string, alertType: string, watchlistId?: string, threshold?: number) =>
  api.post('/alerts/subscribe', {
    email,
    alert_type: alertType,
    watchlist_id: watchlistId,
    threshold,
  })

export const updateAlert = (id: string, isActive: boolean) =>
  api.patch(`/alerts/${id}`, { is_active: isActive })

export const deleteAlert = (id: string) =>
  api.delete(`/alerts/${id}`)

// Health
export const healthCheck = () =>
  api.get('/health')

export default api

