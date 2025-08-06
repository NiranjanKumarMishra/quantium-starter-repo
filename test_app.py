# test_app.py
import pytest
from dash.testing.application import DashComposite
from app import app # Import your Dash app instance from app.py

# This fixture is provided by dash.testing and sets up a test server
# and a Selenium WebDriver instance for testing your Dash app.
# It automatically starts and stops the app for each test.

def test_app_layout_elements(dash_duo: DashComposite):
    """
    Test to ensure the main layout elements (header, graph, radio buttons) are present.
    """
    # Start the Dash app for testing
    dash_duo.start_server(app)

    # --- Test 1: Check if the Header is present ---
    # We look for the H1 element with the specific title text.
    header_element = dash_duo.find_element("h1")
    assert header_element.text == "Soul Foods: Pink Morsel Sales Visualizer", \
        "Header element with correct title text is not present."
    print("Test Passed: Header is present and has the correct title.")

    # --- Test 2: Check if the Visualization (Graph) is present ---
    # We look for the dcc.Graph component by its ID.
    graph_element = dash_duo.find_element("#sales-line-chart")
    assert graph_element.is_displayed(), \
        "Sales line chart (dcc.Graph) is not present or not displayed."
    print("Test Passed: Visualization (line chart) is present.")

    # --- Test 3: Check if the Region Picker (RadioItems) is present ---
    # We look for the dcc.RadioItems component by its ID.
    radio_items_element = dash_duo.find_element("#region-radio")
    assert radio_items_element.is_displayed(), \
        "Region picker (dcc.RadioItems) is not present or not displayed."
    print("Test Passed: Region picker is present.")

    # You can add more specific checks, e.g., checking the number of radio options
    # radio_options = dash_duo.find_elements("#region-radio input[type='radio']")
    # assert len(radio_options) == 5, "Incorrect number of region radio options."
