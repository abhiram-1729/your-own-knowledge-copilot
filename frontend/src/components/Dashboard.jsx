import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import toast, { Toaster } from 'react-hot-toast'
import { 
  Send, 
  Upload, 
  FileText, 
  Trash2, 
  MessageCircle, 
  Brain, 
  Search, 
  Sparkles, 
  File,
  X,
  CheckCircle,
  AlertCircle,
  Clock,
  TrendingUp
} from 'lucide-react'

const Dashboard = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [documents, setDocuments] = useState([])
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [dragActive, setDragActive] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    fetchDocuments()
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/api/documents')
      setDocuments(response.data)
    } catch (error) {
      toast.error('Failed to fetch documents')
    }
  }

  const handleFileUpload = async (file) => {
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      fetchDocuments()
      toast.success('Document uploaded successfully!')
    } catch (error) {
      toast.error('Upload failed: ' + (error.response?.data?.detail || 'Unknown error'))
    } finally {
      setUploading(false)
    }
  }

  const handleFileInputChange = (event) => {
    const file = event.target.files[0]
    if (file) {
      handleFileUpload(file)
    }
    event.target.value = ''
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0])
    }
  }

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/query', { question: input })
      const assistantMessage = { 
        role: 'assistant', 
        content: response.data.answer,
        sources: response.data.sources
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      toast.error('Failed to get response')
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error processing your request.',
        error: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (documentId) => {
    try {
      await axios.delete(`/api/documents/${documentId}`)
      fetchDocuments()
      toast.success('Document deleted successfully!')
    } catch (error) {
      toast.error('Delete failed: ' + (error.response?.data?.detail || 'Unknown error'))
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const getFileIcon = (filename) => {
    const extension = filename.split('.').pop().toLowerCase()
    switch (extension) {
      case 'pdf': return <FileText className="w-4 h-4 text-red-500" />
      case 'docx':
      case 'doc': return <FileText className="w-4 h-4 text-blue-500" />
      case 'txt':
      case 'md': return <FileText className="w-4 h-4 text-gray-500" />
      default: return <File className="w-4 h-4 text-gray-500" />
    }
  }

  const formatResponse = (content) => {
    if (!content) return content
    
    // Split into paragraphs
    const paragraphs = content.split('\n').filter(p => p.trim())
    const formattedElements = []
    
    paragraphs.forEach((paragraph, index) => {
      const trimmed = paragraph.trim()
      
      // Check if it's a main heading (contains Philosophy, Strategies, etc.)
      if (trimmed.includes('Philosophy') || trimmed.includes('Strategies') || 
          trimmed.includes('Rituals') || trimmed.includes('Execution') ||
          (trimmed.includes(':') && !trimmed.includes('because') && trimmed.length < 120)) {
        formattedElements.push(
          <div key={index} className="font-bold text-gray-900 mb-3 mt-4 text-base border-l-3 border-blue-500 pl-3">
            {trimmed.replace(/\*\*/g, '').replace(/\*/g, '').trim()}
          </div>
        )
        return
      }
      
      // Check if it's a subheading (contains **bold text**)
      if (trimmed.includes('**')) {
        const parts = trimmed.split('**')
        formattedElements.push(
          <div key={index} className="font-semibold text-gray-800 mb-2 mt-3 text-sm">
            {parts.map((part, i) => (
              i % 2 === 1 ? <span key={i} className="text-blue-600">{part}</span> : part
            ))}
          </div>
        )
        return
      }
      
      // Check if it's a bullet point with sub-points
      if (trimmed.match(/^[\*\-\•]\s+/) || trimmed.match(/^\d+\.\s+/)) {
        const bulletText = trimmed.replace(/^[\*\-\•]\s+|^\d+\.\s+/, '').trim()
        
        // Check if this bullet contains multiple concepts (separated by commas or "and")
        if (bulletText.includes(':') || (bulletText.includes(',') && bulletText.length > 50)) {
          const [mainConcept, ...details] = bulletText.split(':')
          const detailText = details.join(':')
          
          formattedElements.push(
            <div key={index} className="mb-3">
              <div className="flex items-start space-x-2 mb-1">
                <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-1.5 flex-shrink-0"></div>
                <span className="font-medium text-gray-800 text-sm">{mainConcept.trim()}</span>
              </div>
              {detailText && (
                <div className="ml-4 text-sm text-gray-600 leading-relaxed">
                  {detailText.trim()}
                </div>
              )}
            </div>
          )
        } else {
          // Simple bullet point
          formattedElements.push(
            <div key={index} className="flex items-start space-x-2 mb-2">
              <div className="w-1.5 h-1.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mt-2 flex-shrink-0"></div>
              <span className="text-sm leading-relaxed text-gray-700">{bulletText}</span>
            </div>
          )
        }
        return
      }
      
      // Regular paragraph
      if (trimmed) {
        formattedElements.push(
          <p key={index} className="text-sm leading-relaxed mb-3 text-gray-700">
            {trimmed}
          </p>
        )
      }
    })
    
    return formattedElements
  }

  return (
    <>
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 3000,
          style: {
            background: '#1f2937',
            color: '#fff',
          },
        }}
      />
      
      <div className="flex h-screen bg-gradient-to-br from-slate-50 to-blue-50">
        {/* Main Content */}
        <div className={`flex-1 flex flex-col transition-all duration-300 ${isSidebarOpen ? 'mr-0' : 'mr-0'}`}>
          {/* Header */}
          <motion.header 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/80 backdrop-blur-lg border-b border-gray-200/50 px-6 py-4"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                    Knowledge Copilot
                  </h1>
                  <p className="text-sm text-gray-600">AI-powered document intelligence</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span>Online</span>
                </div>
                <button
                  onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <FileText className="w-5 h-5 text-gray-600" />
                </button>
              </div>
            </div>
          </motion.header>

          {/* Messages Area */}
          <div 
            className="flex-1 overflow-y-auto px-6 py-4"
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {messages.length === 0 ? (
              <motion.div 
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="flex flex-col items-center justify-center h-full text-center"
              >
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-xl opacity-20 animate-pulse"></div>
                  <div className="relative p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full">
                    <MessageCircle className="w-8 h-8 text-white" />
                  </div>
                </div>
                
                <h2 className="text-2xl font-bold text-gray-900 mt-6">
                  Welcome to your Knowledge Copilot
                </h2>
                <p className="text-gray-600 mt-2 max-w-md">
                  Upload your documents and ask questions. I'll provide intelligent answers based on your content.
                </p>
                
                <div className="grid grid-cols-3 gap-4 mt-8 max-w-lg">
                  <div className="p-4 bg-white rounded-xl border border-gray-200/50">
                    <Upload className="w-6 h-6 text-blue-500 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">Upload Documents</p>
                  </div>
                  <div className="p-4 bg-white rounded-xl border border-gray-200/50">
                    <Search className="w-6 h-6 text-purple-500 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">Ask Questions</p>
                  </div>
                  <div className="p-4 bg-white rounded-xl border border-gray-200/50">
                    <Sparkles className="w-6 h-6 text-green-500 mx-auto mb-2" />
                    <p className="text-sm text-gray-600">Get AI Insights</p>
                  </div>
                </div>
              </motion.div>
            ) : (
              <div className="space-y-4 max-w-4xl mx-auto">
                <AnimatePresence>
                  {messages.map((message, index) => (
                    <motion.div
                      key={index}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`flex items-start space-x-3 max-w-3xl ${
                        message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      }`}>
                        <div className={`p-2 rounded-full ${
                          message.role === 'user' 
                            ? 'bg-gradient-to-r from-blue-500 to-purple-600' 
                            : message.error 
                              ? 'bg-red-500' 
                              : 'bg-gradient-to-r from-green-500 to-teal-600'
                        }`}>
                          {message.role === 'user' ? (
                            <div className="w-4 h-4 bg-white rounded-full"></div>
                          ) : message.error ? (
                            <AlertCircle className="w-4 h-4 text-white" />
                          ) : (
                            <Brain className="w-4 h-4 text-white" />
                          )}
                        </div>
                        
                        <div className={`px-4 py-3 rounded-2xl ${
                          message.role === 'user'
                            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                            : message.error
                              ? 'bg-red-50 text-red-800 border border-red-200'
                              : 'bg-white text-gray-800 border border-gray-200 shadow-sm'
                        }`}>
                          <div className="text-sm leading-relaxed">
                            {message.role === 'assistant' ? formatResponse(message.content) : message.content}
                          </div>
                          
                          {message.sources && message.sources.length > 0 && (
                            <div className="mt-3 pt-3 border-t border-gray-200">
                              <div className="flex items-center space-x-2 mb-2">
                                <FileText className="w-4 h-4 text-gray-500" />
                                <span className="text-xs font-medium text-gray-700">Sources</span>
                              </div>
                              <div className="space-y-1">
                                {message.sources.map((source, idx) => (
                                  <div key={idx} className="flex items-center space-x-2 text-xs text-gray-600 bg-gray-50 rounded-lg px-2 py-1">
                                    {getFileIcon(source.filename)}
                                    <span className="truncate">{source.filename}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
                
                {loading && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="flex justify-start"
                  >
                    <div className="flex items-start space-x-3">
                      <div className="p-2 rounded-full bg-gradient-to-r from-green-500 to-teal-600">
                        <Brain className="w-4 h-4 text-white" />
                      </div>
                      <div className="px-4 py-3 rounded-2xl bg-white border border-gray-200 shadow-sm">
                        <div className="flex items-center space-x-2">
                          <div className="flex space-x-1">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                          <span className="text-sm text-gray-600">Thinking...</span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Area */}
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="border-t border-gray-200/50 bg-white/80 backdrop-blur-lg px-6 py-4"
          >
            <div className="max-w-4xl mx-auto">
              <div className="flex items-end space-x-3">
                <div className="flex-1">
                  <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask anything about your documents..."
                    className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    rows="2"
                  />
                </div>
                <button
                  onClick={handleSend}
                  disabled={loading || !input.trim()}
                  className="p-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl hover:shadow-lg transform hover:scale-105 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
              
              <div className="flex items-center justify-between mt-2">
                <p className="text-xs text-gray-500">
                  Press Enter to send, Shift+Enter for new line
                </p>
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <Clock className="w-3 h-3" />
                  <span>AI responses in seconds</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Documents Sidebar */}
        <motion.aside 
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 100 }}
          className={`w-80 bg-white/80 backdrop-blur-lg border-l border-gray-200/50 transition-all duration-300 ${
            isSidebarOpen ? 'translate-x-0' : 'translate-x-full'
          }`}
        >
          <div className="p-6 border-b border-gray-200/50">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Documents</h2>
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                <TrendingUp className="w-3 h-3" />
                <span>{documents.length}</span>
              </div>
            </div>
            
            <div className="relative">
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileInputChange}
                accept=".pdf,.docx,.txt,.md,.eml,.html"
                disabled={uploading}
              />
              
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className={`w-full p-4 border-2 border-dashed rounded-xl transition-all ${
                  dragActive 
                    ? 'border-blue-500 bg-blue-50' 
                    : 'border-gray-300 hover:border-gray-400'
                } ${uploading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
              >
                <div className="flex flex-col items-center space-y-2">
                  <div className={`p-2 rounded-full ${
                    uploading 
                      ? 'bg-gray-200' 
                      : 'bg-gradient-to-r from-blue-500 to-purple-600'
                  }`}>
                    {uploading ? (
                      <div className="w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                    ) : (
                      <Upload className="w-5 h-5 text-white" />
                    )}
                  </div>
                  <span className={`text-sm ${
                    uploading ? 'text-gray-500' : 'text-gray-700'
                  }`}>
                    {uploading ? 'Uploading...' : 'Upload Document'}
                  </span>
                  <span className="text-xs text-gray-500">
                    PDF, DOCX, TXT, MD, EML, HTML
                  </span>
                </div>
              </motion.button>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-6">
            {documents.length === 0 ? (
              <div className="text-center py-8">
                <FileText className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-500">No documents uploaded yet</p>
                <p className="text-xs text-gray-400 mt-1">Upload your first document to get started</p>
              </div>
            ) : (
              <div className="space-y-3">
                <AnimatePresence>
                  {documents.map((doc) => (
                    <motion.div
                      key={doc.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      className="group p-3 bg-gray-50 rounded-xl border border-gray-200/50 hover:shadow-sm transition-all"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start space-x-3 flex-1 min-w-0">
                          <div className="p-2 bg-white rounded-lg border border-gray-200">
                            {getFileIcon(doc.filename)}
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900 truncate">
                              {doc.filename}
                            </p>
                            <div className="flex items-center space-x-2 mt-1">
                              <span className="text-xs text-gray-500">
                                {new Date(doc.upload_date).toLocaleDateString()}
                              </span>
                              <span className="text-xs text-gray-400">•</span>
                              <span className="text-xs text-gray-500">
                                {doc.file_type}
                              </span>
                            </div>
                          </div>
                        </div>
                        
                        <motion.button
                          whileHover={{ scale: 1.1 }}
                          whileTap={{ scale: 0.9 }}
                          onClick={() => handleDelete(doc.id)}
                          className="p-1 text-gray-400 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100"
                        >
                          <Trash2 className="w-4 h-4" />
                        </motion.button>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>
            )}
          </div>
        </motion.aside>
      </div>
    </>
  )
}

export default Dashboard