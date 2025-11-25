import React from 'react'
import { useAuth } from '../contexts/AuthContext'

// Emoji icons
const UserIcon = () => <span>👤</span>
const LogoutIcon = () => <span>🚪</span>
const UploadIcon = () => <span>📁</span>
const MessageIcon = () => <span>💬</span>

const Layout = ({ children }) => {
  const { user, logout } = useAuth()

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-lg">
        <div className="p-6 border-b">
          <h1 className="text-xl font-bold text-gray-800">Knowledge Copilot</h1>
          <div className="flex items-center mt-4 text-sm text-gray-600">
            <UserIcon />
            <span className="ml-2">{user?.username}</span>
          </div>
        </div>
        
        <nav className="p-4">
          <div className="flex items-center px-4 py-2 text-gray-700 bg-blue-50 rounded-lg">
            <MessageIcon />
            <span className="ml-3">Chat</span>
          </div>
          <div className="flex items-center px-4 py-2 mt-2 text-gray-600 hover:bg-gray-50 rounded-lg">
            <UploadIcon />
            <span className="ml-3">Documents</span>
          </div>
        </nav>
        
        <div className="absolute bottom-0 w-64 p-4 border-t">
          <button
            onClick={logout}
            className="flex items-center w-full px-4 py-2 text-gray-600 hover:bg-gray-50 rounded-lg"
          >
            <LogoutIcon />
            <span className="ml-3">Logout</span>
          </button>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 overflow-hidden">
        {children}
      </div>
    </div>
  )
}

export default Layout