import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from matplotlib.figure import Figure

def load_data():
    """Load and prepare the datasets"""
    # Load datasets
    bookings_df = pd.read_csv('Bookings.csv')
    sessions_df = pd.read_csv('Sessions.csv')
    
    # Convert datetime columns with flexible parsing
    bookings_df['booking_time'] = pd.to_datetime(bookings_df['booking_time'], format='ISO8601')
    sessions_df['search_time'] = pd.to_datetime(sessions_df['search_time'], format='ISO8601')
    sessions_df['session_starting_time'] = pd.to_datetime(sessions_df['session_starting_time'], format='ISO8601')
    
    # Extract date components
    bookings_df['booking_date'] = bookings_df['booking_time'].dt.date
    bookings_df['booking_year'] = bookings_df['booking_time'].dt.year
    bookings_df['booking_month'] = bookings_df['booking_time'].dt.month
    bookings_df['booking_month_name'] = bookings_df['booking_time'].dt.strftime('%B')
    bookings_df['booking_day'] = bookings_df['booking_time'].dt.day
    bookings_df['booking_day_of_week'] = bookings_df['booking_time'].dt.day_name()
    bookings_df['booking_quarter'] = bookings_df['booking_time'].dt.quarter
    
    sessions_df['search_date'] = sessions_df['search_time'].dt.date
    sessions_df['search_year'] = sessions_df['search_time'].dt.year
    sessions_df['search_month'] = sessions_df['search_time'].dt.month
    sessions_df['search_month_name'] = sessions_df['search_time'].dt.strftime('%B')
    sessions_df['search_day'] = sessions_df['search_time'].dt.day
    sessions_df['search_day_of_week'] = sessions_df['search_time'].dt.day_name()
    sessions_df['search_quarter'] = sessions_df['search_time'].dt.quarter
    
    return bookings_df, sessions_df

def get_distinct_counts(bookings_df, sessions_df):
    """Count distinct bookings, sessions, and searches"""
    distinct_bookings = bookings_df['booking_id'].nunique()
    distinct_sessions = sessions_df['session_id'].nunique()
    distinct_searches = sessions_df['search_id'].nunique()
    
    return distinct_bookings, distinct_sessions, distinct_searches

def get_sessions_with_multiple_bookings(sessions_df):
    """Find how many sessions have more than one booking"""
    session_booking_counts = sessions_df[sessions_df['booking_id'].notna()].groupby('session_id')['booking_id'].nunique()
    sessions_with_multiple_bookings = sum(session_booking_counts > 1)
    
    return sessions_with_multiple_bookings

def get_bookings_by_day_of_week(bookings_df):
    """Analyze bookings by day of week and create a pie chart"""
    # Order days of week properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count bookings by day of week
    bookings_by_day = bookings_df['booking_day_of_week'].value_counts().reindex(day_order)
    
    # Find day with highest bookings
    max_day = bookings_by_day.idxmax()
    max_bookings = bookings_by_day[max_day]
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(bookings_by_day, labels=bookings_by_day.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Bookings by Day of Week', fontsize=16)
    plt.axis('equal')
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return bookings_by_day, max_day, max_bookings, plot_data

def get_service_performance(bookings_df):
    """Analyze total bookings and GBV by service name"""
    # Group by service name and aggregate
    service_performance = bookings_df.groupby('service_name').agg(
        total_bookings=('booking_id', 'count'),
        total_GBV_INR=('INR_Amount', 'sum')
    ).sort_values('total_bookings', ascending=False)
    
    # Create plot
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot bars for total bookings
    bars = ax1.bar(service_performance.index, service_performance['total_bookings'], color='skyblue')
    ax1.set_xlabel('Service Name')
    ax1.set_ylabel('Total Bookings', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Add a second y-axis for GBV
    ax2 = ax1.twinx()
    line = ax2.plot(service_performance.index, service_performance['total_GBV_INR'], 'ro-', linewidth=2)
    ax2.set_ylabel('Total GBV (INR)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    ax2.grid(False)
    
    plt.title('Service Performance - Bookings & GBV', fontsize=16)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return service_performance, plot_data

def get_most_booked_routes(bookings_df):
    """Find most booked route for customers with more than 1 booking"""
    # Find customers with more than 1 booking
    frequent_customers = bookings_df.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique()
    
    # Filter bookings for these customers
    frequent_customer_bookings = bookings_df[bookings_df['customer_id'].isin(frequent_customers)].copy()
    
    # Create route column
    frequent_customer_bookings.loc[:, 'route'] = frequent_customer_bookings['from_city'] + ' to ' + frequent_customer_bookings['to_city']
    
    # Find the most booked route
    route_counts = frequent_customer_bookings['route'].value_counts()
    most_booked_route = route_counts.idxmax()
    most_booked_route_count = route_counts.max()
    
    # Create bar chart for top routes
    top_routes = route_counts.head(10)
    plt.figure(figsize=(12, 6))
    top_routes.plot(kind='bar', color='teal')
    plt.title('Top 10 Routes for Frequent Customers', fontsize=16)
    plt.xlabel('Route')
    plt.ylabel('Number of Bookings')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return frequent_customers.size, most_booked_route, most_booked_route_count, top_routes, plot_data

def get_advance_booking_cities(bookings_df):
    """Find top 3 departure cities where customers book mostly in advance"""
    # Group by departure city and filter for cities with at least 5 departures
    city_booking_stats = bookings_df.groupby('from_city').filter(lambda x: len(x) >= 5).groupby('from_city').agg(
        avg_days_to_departure=('days_to_departure', 'mean'),
        num_departures=('booking_id', 'count')
    ).sort_values('avg_days_to_departure', ascending=False)
    
    # Create bar chart
    top_cities = city_booking_stats.head(3)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top_cities.index, top_cities['avg_days_to_departure'], color='lightgreen')
    
    # Add departure count as text on bars
    for i, bar in enumerate(bars):
        plt.text(bar.get_x() + bar.get_width()/2, 5, 
                 f"Deps: {int(top_cities.iloc[i]['num_departures'])}",
                 ha='center', va='bottom', fontweight='bold')
    
    plt.title('Top 3 Cities for Advance Bookings', fontsize=16)
    plt.xlabel('Departure City')
    plt.ylabel('Average Days to Departure')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return city_booking_stats.head(10), plot_data

def get_correlation_analysis(bookings_df):
    """Analyze correlations between numerical columns"""
    # Select numerical columns
    numerical_columns = ['INR_Amount', 'no_of_passengers', 'days_to_departure', 'distance_km']
    
    # Calculate correlation matrix
    correlation_matrix = bookings_df[numerical_columns].corr()
    
    # Find maximum correlation (excluding diagonal)
    corr_values = correlation_matrix.unstack()
    corr_values = corr_values[corr_values < 1.0]  # Exclude self-correlations (1.0)
    max_corr = corr_values.max()
    max_corr_pair = corr_values.idxmax()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
    plt.title('Correlation Matrix of Numerical Variables', fontsize=16)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return correlation_matrix, max_corr_pair, max_corr, plot_data

def get_device_usage(bookings_df):
    """Find most used device type for each service"""
    service_device_counts = pd.DataFrame()
    
    # For each service, find the most used device
    services = bookings_df['service_name'].unique()
    
    most_used_devices = {}
    for service in services:
        service_data = bookings_df[bookings_df['service_name'] == service]
        device_counts = service_data['device_type_used'].value_counts()
        most_used_device = device_counts.idxmax()
        device_percentage = (device_counts.max() / device_counts.sum()) * 100
        
        most_used_devices[service] = (most_used_device, device_counts.max(), device_percentage)
        
        # Store counts for visualization
        service_device_counts = pd.concat([
            service_device_counts,
            pd.DataFrame({'service': service, 'device': device_counts.index, 'count': device_counts.values})
        ])
    
    # Create grouped bar chart
    plt.figure(figsize=(12, 8))
    pivot_data = service_device_counts.pivot(index='service', columns='device', values='count').fillna(0)
    pivot_data.plot(kind='bar', stacked=False)
    plt.title('Device Usage by Service', fontsize=16)
    plt.xlabel('Service')
    plt.ylabel('Number of Bookings')
    plt.legend(title='Device Type')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return most_used_devices, pivot_data, plot_data

def get_quarterly_device_bookings(bookings_df):
    """Analyze bookings by device type at quarterly frequency"""
    # Create year-quarter field
    bookings_df = bookings_df.copy()
    bookings_df['year_quarter'] = bookings_df['booking_year'].astype(str) + '-Q' + bookings_df['booking_quarter'].astype(str)
    
    # Group by year-quarter and device type
    quarterly_device_bookings = bookings_df.groupby(['year_quarter', 'device_type_used']).size().unstack(fill_value=0)
    
    # Plot time series
    plt.figure(figsize=(14, 8))
    for device in quarterly_device_bookings.columns:
        plt.plot(quarterly_device_bookings.index, quarterly_device_bookings[device], marker='o', linewidth=2, label=device)
    
    plt.title('Quarterly Booking Trends by Device Type', fontsize=16)
    plt.xlabel('Year-Quarter')
    plt.ylabel('Number of Bookings')
    plt.legend(title='Device Type')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return quarterly_device_bookings, plot_data

def get_booking_search_ratio(bookings_df, sessions_df):
    """Calculate overall booking to search ratio (oBSR) metrics"""
    # Count searches by date
    searches_by_date = sessions_df.groupby(sessions_df['search_time'].dt.date)['search_id'].nunique()
    
    # Count bookings by date
    bookings_by_date = bookings_df.groupby(bookings_df['booking_time'].dt.date)['booking_id'].nunique()
    
    # Create a DataFrame with all unique dates from both searches and bookings
    all_dates = pd.DataFrame(index=sorted(set(searches_by_date.index) | set(bookings_by_date.index)))
    
    # Add searches and bookings columns
    all_dates['searches'] = searches_by_date
    all_dates['bookings'] = bookings_by_date
    
    # Fill NaN values with 0
    all_dates.fillna(0, inplace=True)
    
    # Calculate oBSR
    all_dates['oBSR'] = all_dates['bookings'] / all_dates['searches']
    all_dates['oBSR'] = all_dates['oBSR'].replace([np.inf, -np.inf], 0)  # Handle division by zero
    
    # Reset index to make date a column and ensure it's properly named
    all_dates.reset_index(inplace=True)
    all_dates.rename(columns={'index': 'date'}, inplace=True)
    
    # Convert date to datetime if it's not already
    all_dates['date'] = pd.to_datetime(all_dates['date'])
    
    # Extract date components
    all_dates['month'] = all_dates['date'].dt.month
    all_dates['month_name'] = all_dates['date'].dt.strftime('%B')
    all_dates['day_of_week'] = all_dates['date'].dt.day_name()
    
    # Average oBSR by month
    monthly_obsr = all_dates.groupby('month_name')['oBSR'].mean()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    monthly_obsr = monthly_obsr.reindex(month_order)
    
    # Average oBSR by day of week
    day_obsr = all_dates.groupby('day_of_week')['oBSR'].mean()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_obsr = day_obsr.reindex(day_order)
    
    # Create time series plot
    plt.figure(figsize=(14, 8))
    plt.plot(all_dates['date'], all_dates['oBSR'], marker='o', linestyle='-', color='purple')
    plt.title('Booking to Search Ratio (oBSR) Over Time', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('oBSR')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    ts_buffer = io.BytesIO()
    plt.savefig(ts_buffer, format='png', dpi=100)
    ts_buffer.seek(0)
    ts_plot_data = base64.b64encode(ts_buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Monthly chart
    plt.figure(figsize=(12, 6))
    monthly_obsr.plot(kind='bar', color='teal')
    plt.title('Average oBSR by Month', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Average oBSR')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    monthly_buffer = io.BytesIO()
    plt.savefig(monthly_buffer, format='png', dpi=100)
    monthly_buffer.seek(0)
    monthly_plot_data = base64.b64encode(monthly_buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Day of week chart
    plt.figure(figsize=(12, 6))
    day_obsr.plot(kind='bar', color='orange')
    plt.title('Average oBSR by Day of Week', fontsize=16)
    plt.xlabel('Day of Week')
    plt.ylabel('Average oBSR')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    # Convert plot to base64 for web display
    day_buffer = io.BytesIO()
    plt.savefig(day_buffer, format='png', dpi=100)
    day_buffer.seek(0)
    day_plot_data = base64.b64encode(day_buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return monthly_obsr, day_obsr, ts_plot_data, monthly_plot_data, day_plot_data