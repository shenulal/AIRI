import React from 'react'
import { Link } from 'react-router-dom'
import { BarChart3, Search, BookmarkIcon, Bell } from 'lucide-react'

export default function Navigation() {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2 text-2xl font-bold text-blue-600">
            <BarChart3 size={32} />
            AIRI
          </Link>
          
          <div className="flex items-center gap-6">
            <Link to="/search" className="flex items-center gap-2 text-gray-700 hover:text-blue-600">
              <Search size={20} />
              <span>Search</span>
            </Link>
            
            <Link to="/watchlists" className="flex items-center gap-2 text-gray-700 hover:text-blue-600">
              <BookmarkIcon size={20} />
              <span>Watchlists</span>
            </Link>
            
            <Link to="/alerts" className="flex items-center gap-2 text-gray-700 hover:text-blue-600">
              <Bell size={20} />
              <span>Alerts</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

