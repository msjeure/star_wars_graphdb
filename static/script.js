// ============================================================================
// STAR WARS GRAPHDB - FRONTEND JAVASCRIPT
// ============================================================================

// API Base URL
const API_BASE_URL = window.location.origin;

// ============================================================================
// TAB MANAGEMENT
// ============================================================================

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active class from all buttons
    document.querySelectorAll('.btn-header').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');

    // Add active class to clicked button
    event.target.classList.add('active');
}

// ============================================================================
// CHAT FUNCTIONALITY
// ============================================================================

async function submitQuery() {
    const input = document.getElementById('query-input');
    const question = input.value.trim();

    if (!question) {
        addMessage('Please enter a question', 'error');
        return;
    }

    // Add user message to chat
    addMessage(question, 'user');
    input.value = '';

    // Show loading indicator
    const loadingEl = document.getElementById('loading');
    loadingEl.style.display = 'flex';

    try {
        // Send query to API
        const response = await fetch(`${API_BASE_URL}/api/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Query failed');
        }

        const data = await response.json();

        // Add assistant message with results
        addQueryResult(data);

    } catch (error) {
        console.error('Error:', error);
        addMessage(`Error: ${error.message}`, 'error');
    } finally {
        loadingEl.style.display = 'none';
    }
}

function addMessage(content, type = 'assistant') {
    const messagesContainer = document.getElementById('chat-messages');
    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;

    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';

    if (type === 'user') {
        contentEl.textContent = content;
    } else if (type === 'error') {
        contentEl.innerHTML = `<p style="color: #f44336;">${escapeHtml(content)}</p>`;
    } else {
        contentEl.innerHTML = content;
    }

    messageEl.appendChild(contentEl);
    messagesContainer.appendChild(messageEl);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addQueryResult(data) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageEl = document.createElement('div');
    messageEl.className = 'message assistant';

    const contentEl = document.createElement('div');
    contentEl.className = 'message-content';

    let html = `<p><strong>Found ${data.result_count} results</strong></p>`;

    // Show query button
    html += `<button onclick="showQueryModal('${escapeHtml(data.sparql_query)}')" style="margin-top: 10px; padding: 8px 12px; background: rgba(255, 215, 0, 0.2); border: 1px solid #ffd700; color: #ffd700; border-radius: 4px; cursor: pointer;">View SPARQL Query</button>`;

    // Display results
    if (data.results.length > 0) {
        if (data.results.length === 1 && Object.keys(data.results[0]).length <= 5) {
            // Single result - show as key-value pairs
            html += '<div style="margin-top: 15px;">';
            Object.entries(data.results[0]).forEach(([key, value]) => {
                html += `<p><strong>${escapeHtml(key)}:</strong> ${escapeHtml(String(value))}</p>`;
            });
            html += '</div>';
        } else if (data.results.length > 0 && Object.keys(data.results[0]).length <= 5) {
            // Multiple results - show as table
            const keys = Object.keys(data.results[0]);
            html += '<table class="results-table" style="margin-top: 15px;">';
            html += '<thead><tr>';
            keys.forEach(key => {
                html += `<th>${escapeHtml(key)}</th>`;
            });
            html += '</tr></thead>';
            html += '<tbody>';
            data.results.forEach(row => {
                html += '<tr>';
                keys.forEach(key => {
                    const value = row[key];
                    let cellContent = escapeHtml(String(value));
                    if (typeof value === 'string' && value.startsWith('https://')) {
                        cellContent = `<a href="${value}" target="_blank" style="color: #ffd700;">${cellContent}</a>`;
                    }
                    html += `<td>${cellContent}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody></table>';
        } else {
            // Complex results - show first 3 as JSON
            html += '<pre style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 4px; overflow-x: auto; margin-top: 10px;"><code>' +
                    escapeHtml(JSON.stringify(data.results.slice(0, 3), null, 2)) +
                    (data.results.length > 3 ? `\n... and ${data.results.length - 3} more results` : '') +
                    '</code></pre>';
        }
    }

    contentEl.innerHTML = html;
    messageEl.appendChild(contentEl);
    messagesContainer.appendChild(messageEl);

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// ============================================================================
// SEARCH FUNCTIONALITY
// ============================================================================

async function performSearch() {
    const input = document.getElementById('search-input');
    const searchTerm = input.value.trim();

    if (!searchTerm || searchTerm.length < 2) {
        alert('Please enter at least 2 characters');
        return;
    }

    const resultsContainer = document.getElementById('search-results');
    resultsContainer.innerHTML = '<p>Searching...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/search/${encodeURIComponent(searchTerm)}`);
        
        if (!response.ok) {
            throw new Error('Search failed');
        }

        const data = await response.json();

        if (data.results.length === 0) {
            resultsContainer.innerHTML = '<p>No results found</p>';
            return;
        }

        // Display results
        let html = '';
        data.results.forEach(result => {
            html += `
                <div class="search-result-item" onclick="viewEntityDetails('${escapeHtml(result.uri.split('/').pop())}')">
                    <div class="search-result-label">${escapeHtml(result.label)}</div>
                    <div class="search-result-uri">${escapeHtml(result.uri)}</div>
                </div>
            `;
        });

        resultsContainer.innerHTML = html;

    } catch (error) {
        console.error('Error:', error);
        resultsContainer.innerHTML = `<p style="color: #f44336;">Error: ${error.message}</p>`;
    }
}

// ============================================================================
// STATISTICS
// ============================================================================

async function loadStats() {
    const container = document.getElementById('stats-container');
    container.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        
        if (!response.ok) {
            throw new Error('Failed to load statistics');
        }

        const data = await response.json();

        let html = `
            <div class="stat-card">
                <div class="stat-value">${data.total_triples.toLocaleString()}</div>
                <div class="stat-label">Total Triples</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.total_entities.toLocaleString()}</div>
                <div class="stat-label">Total Entities</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${data.total_relations}</div>
                <div class="stat-label">Relations</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${Object.keys(data.entity_types).length}</div>
                <div class="stat-label">Entity Types</div>
            </div>
        `;

        // Add entity type breakdown
        html += '<div class="stat-card" style="grid-column: 1 / -1;">';
        html += '<h3 style="margin-top: 0; margin-bottom: 10px; color: #ffd700;">Top Entity Types</h3>';
        const sorted = Object.entries(data.entity_types)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10);
        
        sorted.forEach(([type, count]) => {
            html += `<p style="margin: 5px 0;"><strong>${escapeHtml(type)}:</strong> ${count}</p>`;
        });
        html += '</div>';

        container.innerHTML = html;

    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `<p style="color: #f44336;">Error: ${error.message}</p>`;
    }
}

// ============================================================================
// SCHEMA
// ============================================================================

async function loadSchema() {
    const container = document.getElementById('schema-container');
    container.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/schema`);
        
        if (!response.ok) {
            throw new Error('Failed to load schema');
        }

        const data = await response.json();

        let html = '';

        // Classes section
        html += '<div class="schema-section">';
        html += '<h4>Classes (' + data.classes.length + ')</h4>';
        html += '<div class="schema-list">';
        data.classes.forEach(cls => {
            html += `<span class="schema-tag">${escapeHtml(cls)}</span>`;
        });
        html += '</div></div>';

        // Properties section
        html += '<div class="schema-section">';
        html += '<h4>Properties (' + data.properties.length + ')</h4>';
        html += '<div class="schema-list">';
        data.properties.forEach(prop => {
            html += `<span class="schema-tag">${escapeHtml(prop)}</span>`;
        });
        html += '</div></div>';

        container.innerHTML = html;

    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `<p style="color: #f44336;">Error: ${error.message}</p>`;
    }
}

// ============================================================================
// CAPABILITIES
// ============================================================================

async function loadCapabilities() {
    const container = document.getElementById('capabilities-container');
    container.innerHTML = '<p>Loading...</p>';

    try {
        const response = await fetch(`${API_BASE_URL}/api/capabilities`);
        
        if (!response.ok) {
            throw new Error('Failed to load capabilities');
        }

        const data = await response.json();

        let html = '';

        // Supported queries
        html += '<div class="capability-item">';
        html += '<strong>Supported Query Types:</strong>';
        html += '<ul style="margin-left: 20px; margin-top: 10px;">';
        data.supported_queries.forEach(query => {
            html += `<li>${escapeHtml(query)}</li>`;
        });
        html += '</ul></div>';

        // Entity types
        html += '<div class="capability-item">';
        html += '<strong>Entity Types (' + data.entity_types.length + '):</strong>';
        html += '<div class="schema-list" style="margin-top: 10px;">';
        data.entity_types.slice(0, 10).forEach(type => {
            html += `<span class="schema-tag">${escapeHtml(type)}</span>`;
        });
        if (data.entity_types.length > 10) {
            html += `<span class="schema-tag">+ ${data.entity_types.length - 10} more</span>`;
        }
        html += '</div></div>';

        // Data points
        html += '<div class="capability-item">';
        html += '<strong>Total Data Points:</strong>';
        html += `<p style="margin-top: 10px; color: #ffd700; font-size: 20px; font-weight: bold;">${data.total_data_points.toLocaleString()}</p>`;
        html += '</div>';

        container.innerHTML = html;

    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `<p style="color: #f44336;">Error: ${error.message}</p>`;
    }
}

// ============================================================================
// QUERY MODAL
// ============================================================================

function showQueryModal(sparqlQuery) {
    const modal = document.getElementById('query-modal');
    const codeEl = document.getElementById('sparql-code');
    codeEl.textContent = sparqlQuery;
    modal.style.display = 'flex';
}

function closeQueryModal() {
    document.getElementById('query-modal').style.display = 'none';
}

function copySPARQL() {
    const code = document.getElementById('sparql-code').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('SPARQL query copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// ============================================================================
// ENTITY DETAILS
// ============================================================================

async function viewEntityDetails(entityId) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/entity/${encodeURIComponent(entityId)}`);
        
        if (!response.ok) {
            throw new Error('Failed to load entity details');
        }

        const data = await response.json();

        // Switch to chat tab and display details
        showTab('chat');

        // Add entity details to chat
        addMessage(`Entity: ${escapeHtml(data.entity_id)}`, 'user');

        let html = `<p><strong>URI:</strong> ${escapeHtml(data.uri)}</p>`;
        html += '<h3>Properties:</h3>';
        html += '<table class="results-table">';
        html += '<thead><tr><th>Property</th><th>Value</th></tr></thead>';
        html += '<tbody>';

        Object.entries(data.properties).forEach(([key, value]) => {
            let valueStr;
            if (Array.isArray(value)) {
                valueStr = value.map(v => escapeHtml(String(v))).join(', ');
            } else {
                valueStr = escapeHtml(String(value));
            }
            html += `<tr><td><strong>${escapeHtml(key)}</strong></td><td>${valueStr}</td></tr>`;
        });

        html += '</tbody></table>';

        addMessage(html, 'assistant');

    } catch (error) {
        console.error('Error:', error);
        addMessage(`Error: ${error.message}`, 'error');
    }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🌟 Star Wars GraphDB Frontend Loaded');
    
    // Focus on input
    document.getElementById('query-input').focus();
    
    // Add welcome message
    addMessage('Welcome to Star Wars GraphDB! Ask me anything about the Star Wars universe.', 'system');
});

// Close modal when clicking outside
window.addEventListener('click', function(event) {
    const modal = document.getElementById('query-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});
