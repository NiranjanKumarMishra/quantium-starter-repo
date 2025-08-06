# app.py
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

# --- 1. Load and Prepare Data ---
# Load the data generated from the previous task (formatted_output.csv)
try:
    df = pd.read_csv('formatted_output.csv')
    # Ensure the 'date' column is in datetime format for proper sorting and plotting
    df['date'] = pd.to_datetime(df['date'])
    # Sort the DataFrame by date to ensure the line chart is chronological
    df = df.sort_values(by='date')
except FileNotFoundError:
    print("Error: formatted_output.csv not found. Please ensure the previous task was completed successfully.")
    # If the file is not found, create a dummy DataFrame for demonstration purposes.
    # This dummy data simulates sales before and after the price increase on Jan 15, 2021.
    df = pd.DataFrame({
        'sales': [100, 120, 80, 150, 110, 180, 160, 200, 190, 210, 220, 250],
        'date': pd.to_datetime([
            '2021-01-01', '2021-01-05', '2021-01-10', '2021-01-14', # Before price increase
            '2021-01-16', '2021-01-20', '2021-01-25', '2021-01-30', # After price increase
            '2021-02-05', '2021-02-10', '2021-02-15', '2021-02-20'
        ]),
        'region': ['North', 'South', 'East', 'West', 'North', 'South', 'East', 'West', 'North', 'South', 'East', 'West']
    })
    print("Using dummy data for demonstration.")

# --- 2. Initialize the Dash App ---
app = Dash(__name__)

# --- 3. Create the Line Chart ---
# Use Plotly Express to create a line chart of sales over time
fig = px.line(
    df,
    x='date',
    y='sales',
    title='Pink Morsel Sales Over Time', # Chart title
    labels={'date': 'Date', 'sales': 'Total Sales ($)'}, # Axis labels
    hover_data={'region': True} # Show region on hover for more detail
)

# Add a vertical line to indicate the price increase date (January 15, 2021)
price_increase_date = pd.to_datetime('2021-01-15')
fig.add_vline(
    x=price_increase_date.timestamp() * 1000, # Convert to milliseconds for Plotly
    line_dash="dash", # Make the line dashed
    line_color="red", # Color the line red
    annotation_text="Price Increase Date", # Text annotation for the line
    annotation_position="top right" # Position of the annotation
)

# Customize the layout for better readability and aesthetics
fig.update_layout(
    plot_bgcolor='#f9f9f9', # Light background for the plot area
    paper_bgcolor='#ffffff', # White background for the entire figure
    font_family="Arial, sans-serif", # Consistent font
    margin=dict(l=40, r=40, t=80, b=40) # Adjust margins
)

# --- 4. Define the App Layout ---
app.layout = html.Div(
    style={
        'fontFamily': 'Arial, sans-serif',
        'padding': '20px',
        'backgroundColor': '#e0f2f7', # Light blue background for the page
        'minHeight': '100vh', # Ensure it covers the full viewport height
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center'
    },
    children=[
        html.H1(
            "Soul Foods: Pink Morsel Sales Visualizer",
            style={
                'textAlign': 'center',
                'color': '#2c3e50', # Dark blue-grey for header
                'marginBottom': '20px',
                'fontSize': '2.5em'
            }
        ),
        html.Div(
            [
                html.P(
                    "This interactive chart visualizes the daily sales of Pink Morsels, allowing us to easily compare sales performance before and after the price increase on January 15, 2021. Observe the trend to determine the impact of the price change.",
                    style={
                        'textAlign': 'center',
                        'color': '#34495e', # Slightly lighter dark blue-grey for paragraph
                        'marginBottom': '30px',
                        'fontSize': '1.1em',
                        'maxWidth': '700px'
                    }
                ),
                dcc.Graph(
                    id='sales-line-chart',
                    figure=fig,
                    style={
                        'height': '600px', # Adjust height for better visibility
                        'width': '100%', # Make it responsive
                        'minWidth': '300px' # Minimum width for small screens
                    }
                )
            ],
            style={
                'maxWidth': '900px', # Max width for the content container
                'width': '95%', # Responsive width
                'margin': 'auto',
                'border': '1px solid #b3e0ff', # Light blue border
                'borderRadius': '12px', # More rounded corners
                'padding': '25px',
                'boxShadow': '0 6px 12px rgba(0,0,0,0.15)', # More pronounced shadow
                'backgroundColor': '#ffffff' # White background for the content box
            }
        )
    ]
)

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True allows for auto-reloading on code changes
