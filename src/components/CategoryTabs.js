export default function CategoryTabs({ categories, activeCategory, setActiveCategory }) {
  return (
    <div className="border-b border-gray-200 mb-6">
      <nav className="flex flex-wrap gap-2 sm:gap-0 sm:space-x-8">
        {categories.map(category => (
          <button
            key={category.id}
            className={`py-3 px-4 sm:px-1 border-b-2 font-medium text-sm rounded-t-lg sm:rounded-none transition-all duration-200 ${
              activeCategory === category.id
                ? 'border-blue-500 text-blue-600 bg-blue-50 sm:bg-transparent'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 hover:bg-gray-50 sm:hover:bg-transparent'
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