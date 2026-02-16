import pandas as pd
import plotly.graph_objects as go

def create_plots(df, x_axis_column, plot_title_prefix):
    """
    Generates a set of interactive plots for cache performance metrics.

    Args:
        df (pd.DataFrame): The dataframe containing the cache simulation data.
        x_axis_column (str): The name of the column to be used for the x-axis.
        plot_title_prefix (str): A prefix for the title of each plot.

    Returns:
        list: A list of plotly Figure objects.
    """
    # Columns to be plotted on the y-axis
    y_axis_columns = {
        'Total': 'Total Misses',
        'Capacity': 'Capacity Misses',
        'Cold': 'Cold Misses',
        'Miss Rate': 'Overall Miss Rate',
        'MPKI': 'MPKI (Misses Per Kilo Instruction)'
    }

    figures = []
    for y_col, y_title in y_axis_columns.items():
        fig = go.Figure(data=go.Scatter(
            x=df[x_axis_column],
            y=df[y_col],
            mode='lines+markers',
            name=y_title
        ))
        fig.update_layout(
            title=f'{plot_title_prefix}: {y_title} vs. {x_axis_column}',
            xaxis_title=x_axis_column,
            yaxis_title=y_title,
            hovermode='x unified'
        )
        figures.append(fig)

    return figures

def main():
    """
    Main function to load data, generate plots, and create the HTML report.
    """
    # File paths for the CSV files
    # The first file is assumed to be the 'BlockSize' data
    block_size_file = 'cache_simulation_resultsMatrixMultWithReqConfigs.xlsx - cache_simulation_resultsMatrixM.csv'
    cache_size_file = 'cache_simulation_resultsMatrixMultWithReqConfigs.xlsx - CacheSize.csv'
    associativity_file = 'cache_simulation_resultsMatrixMultWithReqConfigs.xlsx - Associativity.csv'

    # Load the data into pandas DataFrames
    try:
        df_block_size = pd.read_csv(block_size_file)
        df_cache_size = pd.read_csv(cache_size_file)
        df_associativity = pd.read_csv(associativity_file)
    except FileNotFoundError as e:
        print(f"Error: {e}. Please make sure the CSV files are in the same directory as the script.")
        return

    # Generate the plots for each dataset
    block_size_plots = create_plots(df_block_size, 'Block Size (B)', 'Varying Block Size')
    cache_size_plots = create_plots(df_cache_size, 'Cache Size (KB)', 'Varying Cache Size')
    associativity_plots = create_plots(df_associativity, 'Associativity', 'Varying Associativity')

    # --- Create the HTML file ---
    with open('cache_analysis.html', 'w') as f:
        f.write('<html><head><title>Cache Simulation Analysis</title></head><body>')
        f.write('<h1 style="text-align:center;">Cache Performance Analysis</h1>')

        # Section for Block Size plots
        f.write('<hr><h2>Analysis for Varying Block Size</h2>')
        for plot in block_size_plots:
            f.write(plot.to_html(full_html=False, include_plotlyjs='cdn'))

        # Section for Cache Size plots
        f.write('<hr><h2>Analysis for Varying Cache Size</h2>')
        for plot in cache_size_plots:
            f.write(plot.to_html(full_html=False, include_plotlyjs='cdn'))

        # Section for Associativity plots
        f.write('<hr><h2>Analysis for Varying Associativity</h2>')
        for plot in associativity_plots:
            f.write(plot.to_html(full_html=False, include_plotlyjs='cdn'))

        f.write('</body></html>')

    print("Successfully generated the HTML file: cache_analysis.html")


if __name__ == '__main__':
    main()