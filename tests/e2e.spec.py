"""Playwright test outline for the Docker stack; run with pytest-playwright when browsers are installed."""

def test_dashboard_contract(page):
    page.goto("http://localhost:3000")
    assert page.get_by_test_id("page-title").inner_text() == "System status"
    assert page.get_by_test_id("backend-health-card").is_visible()