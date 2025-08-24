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
  // Operator button selection
  document.querySelectorAll(".op-btn").forEach(btn => {
    btn.addEventListener("click", function() {
      document.querySelectorAll(".op-btn").forEach(b => b.classList.remove("active"));
      this.classList.add("active");
    });
  });

  // Apply filter button
  document.getElementById("applyFilterBtn").addEventListener("click", applyFilter);
  
  // Apply search button
  document.getElementById("applySearchBtn").addEventListener("click", applySearch);
}

/**
 * Apply a new filter
 */
function applyFilter() {
  const field = document.getElementById("fieldInput").value.trim();
  const value = document.getElementById("valueInput").value.trim();
  const activeOp = document.querySelector(".op-btn.active");

  if (!field || !value || !activeOp) {
    alert("Please enter field, operator, and value.");
    return;
  }

  const op = activeOp.dataset.op;
  const queryText = `${field} ${op} ${value}`;

  // Send filter request to backend
  fetch(APPLY_FILTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      field: field,
      operator: op,
      value: value
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Create filter chip using the helper function
      addFilterChip(field, op, value);

      // Clear inputs
      document.getElementById("fieldInput").value = "";
      document.getElementById("valueInput").value = "";
      activeOp.classList.remove("active");

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
 * @param {string} field - Filter field
 * @param {string} operator - Filter operator
 * @param {string} value - Filter value
 * @param {HTMLElement} chipElement - The chip element to remove
 */
function removeFilter(field, operator, value, chipElement) {
  fetch(REMOVE_FILTER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRF_TOKEN
    },
    body: JSON.stringify({
      field: field,
      operator: operator,
      value: value
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
      addFilterChip(filter.field, filter.operator, filter.value);
    }
  });
  
  updateNoFiltersMessage();
}

/**
 * Add a filter chip to the UI
 * @param {string} field - Filter field
 * @param {string} operator - Filter operator
 * @param {string} value - Filter value
 */
function addFilterChip(field, operator, value) {
  const queryText = `${field} ${operator} ${value}`;
  
  const chip = document.createElement("div");
  chip.className = "query-chip";
  chip.innerHTML = `${queryText} <span class="remove">&times;</span>`;
  chip.dataset.field = field;
  chip.dataset.operator = operator;
  chip.dataset.value = value;

  // Add remove functionality
  chip.querySelector(".remove").addEventListener("click", function() {
    removeFilter(field, operator, value, chip);
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
