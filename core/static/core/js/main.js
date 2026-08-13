// FitTrack AI Interactive JavaScript
document.addEventListener('DOMContentLoaded', () => {
  console.log('FitTrack AI initialized');

  // AI Interactive Demo Search
  const searchInput = document.getElementById('aiSearchInput');
  const searchBtn = document.getElementById('aiSearchBtn');
  const presetTags = document.querySelectorAll('.preset-tag');
  
  const calVal = document.getElementById('resCalories');
  const protVal = document.getElementById('resProtein');
  const carbVal = document.getElementById('resCarbs');
  const fatVal = document.getElementById('resFats');
  const foodTitle = document.getElementById('resFoodTitle');
  const servingVal = document.getElementById('resServingSize');
  const vitVal = document.getElementById('resVitamins');
  
  const protBar = document.getElementById('protBar');
  const carbBar = document.getElementById('carbBar');
  const fatBar = document.getElementById('fatBar');

  async function performAISearch(query) {
    if (!query) return;
    
    if (searchBtn) {
      searchBtn.disabled = true;
      searchBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> AI Analyzing...';
    }

    try {
      const response = await fetch(`/api/ai-analyze/?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      
      if (response.ok) {
        if (foodTitle) foodTitle.textContent = data.name;
        if (servingVal && data.serving_size) {
          servingVal.innerHTML = `<i class="fas fa-weight-hanging"></i> Portion / Serving Size: ${data.serving_size}`;
        }
        if (calVal) calVal.textContent = data.calories;
        if (protVal) protVal.textContent = `${data.protein}g`;
        if (carbVal) carbVal.textContent = `${data.carbs}g`;
        if (fatVal) fatVal.textContent = `${data.fats}g`;
        
        let metaText = `Micronutrients: ${data.vitamins}`;
        if (data.dataset_verification) {
          metaText += ` • ${data.dataset_verification}`;
        } else if (data.accuracy_confidence) {
          metaText += ` • Accuracy: ${data.accuracy_confidence}`;
        }
        if (vitVal) vitVal.textContent = metaText;
        
        // Progress bars calculation
        const total = (data.protein * 4) + (data.carbs * 4) + (data.fats * 9) || 1;
        const pPct = Math.min(Math.round(((data.protein * 4) / total) * 100), 100);
        const cPct = Math.min(Math.round(((data.carbs * 4) / total) * 100), 100);
        const fPct = Math.min(Math.round(((data.fats * 9) / total) * 100), 100);
        
        if (protBar) protBar.style.width = `${pPct}%`;
        if (carbBar) carbBar.style.width = `${cPct}%`;
        if (fatBar) fatBar.style.width = `${fPct}%`;
      }
    } catch (err) {
      console.error('Error fetching nutrient data:', err);
    } finally {
      if (searchBtn) {
        searchBtn.disabled = false;
        searchBtn.innerHTML = '<i class="fas fa-wand-magic-sparkles"></i> AI Analyze';
      }
    }
  }

  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', () => {
      performAISearch(searchInput.value.trim());
    });

    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        performAISearch(searchInput.value.trim());
      }
    });
  }

  presetTags.forEach(tag => {
    tag.addEventListener('click', () => {
      const food = tag.getAttribute('data-food');
      if (searchInput) searchInput.value = food;
      performAISearch(food);
    });
  });
});
