import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="px-4 py-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Wrestling Analytics Platform
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Track wrestler performance and match statistics
        </p>
        
        <div className="flex justify-center space-x-4">
          <Link 
            href="/wrestlers" 
            className="btn btn-primary"
          >
            View Wrestlers
          </Link>
        </div>
      </div>
    </div>
  )
}