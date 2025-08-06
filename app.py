# app.py
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

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
        'sales': [100, 120, 80, 150, 110, 180, 160, 200, 190, 210, 220, 250,
                  105, 125, 85, 155, 115, 185, 165, 205, 195, 215, 225, 255,
                  90, 110, 70, 140, 100, 170, 150, 190, 180, 200, 210, 240,
                  110, 130, 90, 160, 120, 190, 170, 210, 200, 220, 230, 260],
        'date': pd.to_datetime([
            '2021-01-01', '2021-01-05', '2021-01-10', '2021-01-14', # Before price increase - North
            '2021-01-16', '2021-01-20', '2021-01-25', '2021-01-30', # After price increase - North
            '2021-01-02', '2021-01-06', '2021-01-11', '2021-01-13', # Before price increase - East
            '2021-01-17', '2021-01-21', '2021-01-26', '2021-01-31', # After price increase - East
            '2021-01-03', '2021-01-07', '2021-01-09', '2021-01-12', # Before price increase - South
            '2021-01-18', '2021-01-22', '2021-01-27', '2021-02-01', # After price increase - South
            '2021-01-04', '2021-01-08', '2021-01-12', '2021-01-14', # Before price increase - West
            '2021-01-19', '2021-01-23', '2021-01-28', '2021-02-02'  # After price increase - West
        ]),
        'region': ['North', 'North', 'North', 'North', 'North', 'North', 'North', 'North',
                   'East', 'East', 'East', 'East', 'East', 'East', 'East', 'East',
                   'South', 'South', 'South', 'South', 'South', 'South', 'South', 'South',
                   'West', 'West', 'West', 'West', 'West', 'West', 'West', 'West']
    })
    # Sort the dummy data by date
    df = df.sort_values(by='date')
    print("Using dummy data for demonstration.")


# --- 2. Initialize the Dash App ---
app = Dash(__name__)

# --- 3. Define the App Layout ---
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
                'fontSize': '2.5em',
                'fontWeight': 'bold'
            }
        ),
        html.Div(
            [
                html.P(
                    "This interactive chart visualizes the daily sales of Pink Morsels. Use the region filter below to analyze sales performance before and after the price increase on January 15, 2021, for specific regions or all regions combined.",
                    style={
                        'textAlign': 'center',
                        'color': '#34495e', # Slightly lighter dark blue-grey for paragraph
                        'marginBottom': '30px',
                        'fontSize': '1.1em',
                        'maxWidth': '700px'
                    }
                ),
                html.Div(
                    [
                        html.Label("Select Region:", style={'fontWeight': 'bold', 'marginRight': '10px', 'color': '#2c3e50'}),
                        dcc.RadioItems(
                            id='region-radio',
                            options=[
                                {'label': 'All', 'value': 'all'},
                                {'label': 'North', 'value': 'North'},
                                {'label': 'East', 'value': 'East'},
                                {'label': 'South', 'value': 'South'},
                                {'label': 'West', 'value': 'West'}
                            ],
                            value='all', # Default selected value
                            inline=True, # Display radio buttons in a single line
                            style={'color': '#34495e'},
                            inputStyle={'marginRight': '5px', 'marginLeft': '15px'} # Spacing for radio buttons
                        ),
                    ],
                    style={
                        'textAlign': 'center',
                        'marginBottom': '20px',
                        'padding': '15px',
                        'backgroundColor': '#f0f8ff', # Lighter blue background for filter
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.08)'
                    }
                ),
                dcc.Graph(
                    id='sales-line-chart',
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

# --- 4. Implement Callbacks ---
@app.callback(
    Output('sales-line-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_graph(selected_region):
    # Filter DataFrame based on selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    # Create the line chart
    fig = px.line(
        filtered_df,
        x='date',
        y='sales',
        title=f'Pink Morsel Sales Over Time (Region: {selected_region.capitalize()})',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'},
        hover_data={'region': True, 'sales': ':.2f'} # Format sales on hover
    )

    # Add a vertical line to indicate the price increase date (January 15, 2021)
    price_increase_date = pd.to_datetime('2021-01-15')
    fig.add_vline(
        x=price_increase_date.timestamp() * 1000, # Convert to milliseconds for Plotly
        line_dash="dash", # Make the line dashed
        line_color="red", # Color the line red
        annotation_text="Price Increase Date", # Text annotation for the line
        annotation_position="top right", # Position of the annotation
        name="Price Increase" # Name for hover text
    )

    # Customize the layout for better readability and aesthetics
    fig.update_layout(
        plot_bgcolor='#f9f9f9', # Light background for the plot area
        paper_bgcolor='#ffffff', # White background for the entire figure
        font_family="Arial, sans-serif", # Consistent font
        margin=dict(l=40, r=40, t=80, b=40), # Adjust margins
        hovermode="x unified" # Unified hover for better comparison
    )

    return fig

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True)