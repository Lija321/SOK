/**
 * Filter functionality for the Graph Explorer
 * Handles applying, removing, and displaying filters as chips
 */

// Global variables for CSRF token and URLs (will be set from template)
let CSRF_TOKEN = '';
let APPLY_FILTER_URL = '';
let REMOVE_FILTER_URL = '';
let APPLY_SEARCH_URL = '';
let REMOVE_SEARCH_URL = '';

/**
 * Initialize filter functionality
 * @param {string} csrfToken - Django CSRF token
 * @param {string} applyFilterUrl - URL for applying filters
 * @param {string} removeFilterUrl - URL for removing filters
 * @param {string} applySearchUrl - URL for applying searches
 * @param {string} removeSearchUrl - URL for removing searches
 */
function initializeFilters(csrfToken, applyFilterUrl, removeFilterUrl, applySearchUrl, removeSearchUrl) {
  CSRF_TOKEN = csrfToken;
  APPLY_FILTER_URL = applyFilterUrl;
  REMOVE_FILTER_URL = removeFilterUrl;
  APPLY_SEARCH_URL = applySearchUrl;
  REMOVE_SEARCH_URL = removeSearchUrl;
  
  setupFilterEventListeners();
  loadExistingFilters();
}

/**
 * Set up event listeners for filter functionality
 */
function setupFilterEventListeners() {
  // Apply filter button
  document.getElementById("applyFilterBtn").addEventListener("click", applyFilter);
  
  // Apply search button
  document.getElementById("applySearchBtn").addEventListener("click", applySearch);
}

/**
 * Apply a new filter
 */
function applyFilter() {
  const filterQuery = document.getElementById("filterQueryInput").value.trim();

  if (!filterQuery) {
    alert("Please enter a filter query (e.g., age > 30).");
    return;
  }

  // Send filter request to backend
  fetch(APPLY_FILTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      query: filterQuery
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Create filter chip using the helper function
      addFilterChip(filterQuery);

      // Clear input
      document.getElementById("filterQueryInput").value = "";

      // Reload page to show filtered results
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      alert("Error applying filter: " + data.error);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error applying filter. Please try again.");
  });
}

/**
 * Apply a new search
 */
function applySearch() {
  const searchValue = document.getElementById("searchInput").value.trim();

  if (!searchValue) {
    alert("Please enter a search value.");
    return;
  }

  // Send search request to backend
  fetch(APPLY_SEARCH_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      value: searchValue
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Create search chip using the helper function
      addSearchChip(searchValue);

      // Clear input
      document.getElementById("searchInput").value = "";

      // Reload page to show filtered results
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      alert("Error applying search: " + data.error);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error applying search. Please try again.");
  });
}

/**
 * Remove a search
 * @param {string} searchValue - Search value
 * @param {HTMLElement} chipElement - The chip element to remove
 */
function removeSearch(searchValue, chipElement) {
  fetch(REMOVE_SEARCH_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      value: searchValue
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      chipElement.remove();
      updateNoFiltersMessage();
      // Reload page to show updated results
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      alert("Error removing search: " + data.error);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error removing search. Please try again.");
  });
}

/**
 * Remove a filter
 * @param {string} filterQuery - Filter query string
 * @param {HTMLElement} chipElement - The chip element to remove
 */
function removeFilter(filterQuery, chipElement) {
  fetch(REMOVE_FILTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      query: filterQuery
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      chipElement.remove();
      updateNoFiltersMessage();
      // Reload page to show updated results
      setTimeout(() => {
        window.location.reload();
      }, 500);
    } else {
      alert("Error removing filter: " + data.error);
    }
  })
  .catch(error => {
    console.error("Error:", error);
    alert("Error removing filter. Please try again.");
  });
}

/**
 * Load existing filters on page load
 */
function loadExistingFilters() {
  // This will be populated by the template with existing filters
  const existingFilters = window.EXISTING_FILTERS || [];
  
  existingFilters.forEach(filter => {
    if (filter.type === 'search') {
      addSearchChip(filter.value);
    } else {
      addFilterChip(filter.query);
    }
  });
  
  updateNoFiltersMessage();
}

/**
 * Add a filter chip to the UI
 * @param {string} filterQuery - Filter query string (e.g., "age > 30")
 */
function addFilterChip(filterQuery) {
  const chip = document.createElement("div");
  chip.className = "query-chip";
  chip.innerHTML = `${filterQuery} <span class="remove">&times;</span>`;
  chip.dataset.filterQuery = filterQuery;

  // Add remove functionality
  chip.querySelector(".remove").addEventListener("click", function() {
    removeFilter(filterQuery, chip);
  });

  const appliedQueries = document.getElementById("appliedQueries");
  const noFiltersMessage = document.getElementById("noFiltersMessage");
  
  // Hide "no filters" message and add the chip
  if (noFiltersMessage) {
    noFiltersMessage.style.display = "none";
  }
  
  appliedQueries.appendChild(chip);
}

/**
 * Add a search chip to the UI
 * @param {string} searchValue - Search value
 */
function addSearchChip(searchValue) {
  const queryText = `Search: ${searchValue}`;
  
  const chip = document.createElement("div");
  chip.className = "query-chip search-chip";
  chip.innerHTML = `${queryText} <span class="remove">&times;</span>`;
  chip.dataset.searchValue = searchValue;
  chip.dataset.type = "search";

  // Add remove functionality
  chip.querySelector(".remove").addEventListener("click", function() {
    removeSearch(searchValue, chip);
  });

  const appliedQueries = document.getElementById("appliedQueries");
  const noFiltersMessage = document.getElementById("noFiltersMessage");
  
  // Hide "no filters" message and add the chip
  if (noFiltersMessage) {
    noFiltersMessage.style.display = "none";
  }
  
  appliedQueries.appendChild(chip);
}

/**
 * Update the "no filters" message visibility
 */
function updateNoFiltersMessage() {
  const appliedQueries = document.getElementById("appliedQueries");
  const noFiltersMessage = document.getElementById("noFiltersMessage");
  const chips = appliedQueries.querySelectorAll(".query-chip");
  
  if (chips.length === 0) {
    if (noFiltersMessage) {
      noFiltersMessage.style.display = "inline";
    }
  } else {
    if (noFiltersMessage) {
      noFiltersMessage.style.display = "none";
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
  // Wait for template to set up the initialization call
  if (typeof window.initFilters === 'function') {
    window.initFilters();
  }
});
