// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Authentication Configuration
// Set REACT_APP_REQUIRE_AUTH=true to enable authentication
const REQUIRE_AUTH = process.env.REACT_APP_REQUIRE_AUTH === 'true';

export { API_BASE_URL, REQUIRE_AUTH };
