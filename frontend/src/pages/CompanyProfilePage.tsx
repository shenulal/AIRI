import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { AlertTriangle, ExternalLink } from 'lucide-react'
import { getCompany, getCompanyDocuments, Document } from '../services/api'

export default function CompanyProfilePage() {
  const { id } = useParams<{ id: string }>()
  const [company, setCompany] = useState<any>(null)
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return
      
      setLoading(true)
      setError('')
      try {
        const companyRes = await getCompany(id)
        setCompany(companyRes.data)
        
        const docsRes = await getCompanyDocuments(id)
        setDocuments(docsRes.data)
      } catch (err) {
        setError('Failed to load company profile')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [id])

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <p className="mt-2 text-gray-600">Loading...</p>
      </div>
    )
  }

  if (error || !company) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {error || 'Company not found'}
      </div>
    )
  }

  const getRiskColor = (score: number) => {
    if (score < 30) return 'bg-green-100 text-green-800'
    if (score < 60) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  const getSentimentColor = (label?: string) => {
    if (label === 'positive') return 'text-green-600'
    if (label === 'negative') return 'text-red-600'
    return 'text-gray-600'
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white p-8 rounded-lg shadow-md">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">
              {company.name}
              {company.ticker && <span className="text-gray-500 ml-2">({company.ticker})</span>}
            </h1>
            {company.industry && (
              <p className="text-gray-600 mt-2">{company.industry}</p>
            )}
          </div>
          <div className={`px-4 py-2 rounded-lg font-semibold ${getRiskColor(company.risk_score)}`}>
            <div className="flex items-center gap-2">
              <AlertTriangle size={20} />
              <div>
                <p className="text-sm">Risk Score</p>
                <p className="text-2xl font-bold">{company.risk_score.toFixed(1)}</p>
              </div>
            </div>
          </div>
        </div>

        {company.description && (
          <p className="text-gray-700 mb-4">{company.description}</p>
        )}

        {company.website && (
          <a
            href={company.website}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 flex items-center gap-2"
          >
            Visit Website
            <ExternalLink size={16} />
          </a>
        )}
      </div>

      {/* Executive Summary */}
      {company.executive_summary && (
        <div className="bg-blue-50 p-8 rounded-lg border border-blue-200">
          <h2 className="text-2xl font-bold mb-4 text-gray-900">Executive Summary</h2>
          <p className="text-gray-700 leading-relaxed">{company.executive_summary}</p>
        </div>
      )}

      {/* Recent Documents */}
      <div>
        <h2 className="text-2xl font-bold mb-4 text-gray-900">Recent News & Documents</h2>
        {documents.length > 0 ? (
          <div className="space-y-4">
            {documents.map((doc) => (
              <div key={doc.id} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold text-gray-900 flex-1">{doc.title}</h3>
                  {doc.sentiment_label && (
                    <span className={`ml-4 px-3 py-1 rounded-full text-sm font-semibold ${getSentimentColor(doc.sentiment_label)}`}>
                      {doc.sentiment_label}
                    </span>
                  )}
                </div>
                <p className="text-gray-600 text-sm mb-2">
                  {new Date(doc.published_at || doc.ingested_at).toLocaleDateString()} • {doc.source}
                </p>
                <p className="text-gray-700 line-clamp-3">{doc.content}</p>
                {doc.source_url && (
                  <a
                    href={doc.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-flex items-center gap-1"
                  >
                    Read More
                    <ExternalLink size={14} />
                  </a>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-600">No documents found</p>
        )}
      </div>
    </div>
  )
}

