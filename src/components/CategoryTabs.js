export default function CategoryTabs({ categories, activeCategory, setActiveCategory }) {
  return (
    <div className="border-b border-gray-200 mb-6">
      <nav className="flex space-x-8">
        {categories.map(category => (
          <button
            key={category.id}
            className={`py-4 px-1 border-b-2 font-medium text-sm ${
              activeCategory === category.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
            onClick={() => setActiveCategory(category.id)}
          >
            {category.name}
          </button>
        ))}
      </nav>
    </div>
  )
}