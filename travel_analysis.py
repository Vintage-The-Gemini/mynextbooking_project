import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set plot style and figure size for better visualization
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = [12, 8]

# Set pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def load_data():
    """Load and prepare the datasets"""
    print("Loading and preparing data...")
    
    # Load datasets
    bookings_df = pd.read_csv('Bookings.csv')
    sessions_df = pd.read_csv('Sessions.csv')
    
    # Convert datetime columns with more flexible parsing
    bookings_df['booking_time'] = pd.to_datetime(bookings_df['booking_time'], format='ISO8601')
    sessions_df['search_time'] = pd.to_datetime(sessions_df['search_time'], format='ISO8601')
    sessions_df['session_starting_time'] = pd.to_datetime(sessions_df['session_starting_time'], format='ISO8601')
    
    # Extract date components for later analysis
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
    
    print("Data loaded and prepared successfully.")
    
    return bookings_df, sessions_df
    """Load and prepare the datasets"""
    print("Loading and preparing data...")
    
    # Load datasets
    bookings_df = pd.read_csv('Bookings.csv')
    sessions_df = pd.read_csv('Sessions.csv')
    
    # Convert datetime columns
    bookings_df['booking_time'] = pd.to_datetime(bookings_df['booking_time'])
    sessions_df['search_time'] = pd.to_datetime(sessions_df['search_time'])
    sessions_df['session_starting_time'] = pd.to_datetime(sessions_df['session_starting_time'])
    
    # Extract date components for later analysis
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
    
    print("Data loaded and prepared successfully.")
    
    return bookings_df, sessions_df

def analyze_distinct_counts(bookings_df, sessions_df):
    """Count distinct bookings, sessions, and searches"""
    print("\n1) DISTINCT COUNTS ANALYSIS")
    print("-" * 50)
    
    distinct_bookings = bookings_df['booking_id'].nunique()
    distinct_sessions = sessions_df['session_id'].nunique()
    distinct_searches = sessions_df['search_id'].nunique()
    
    print(f"Number of distinct bookings: {distinct_bookings}")
    print(f"Number of distinct sessions: {distinct_sessions}")
    print(f"Number of distinct searches: {distinct_searches}")
    
    return distinct_bookings, distinct_sessions, distinct_searches

def analyze_sessions_with_multiple_bookings(sessions_df):
    """Find how many sessions have more than one booking"""
    print("\n2) SESSIONS WITH MULTIPLE BOOKINGS")
    print("-" * 50)
    
    # Count bookings per session
    session_booking_counts = sessions_df[sessions_df['booking_id'].notna()].groupby('session_id')['booking_id'].nunique()
    sessions_with_multiple_bookings = sum(session_booking_counts > 1)
    
    print(f"Number of sessions with more than one booking: {sessions_with_multiple_bookings}")
    
    return sessions_with_multiple_bookings

def analyze_bookings_by_day_of_week(bookings_df):
    """Analyze bookings by day of week and create a pie chart"""
    print("\n3) BOOKINGS BY DAY OF WEEK")
    print("-" * 50)
    
    # Order days of week properly
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Count bookings by day of week
    bookings_by_day = bookings_df['booking_day_of_week'].value_counts().reindex(day_order)
    
    print("Bookings by day of week:")
    for day, count in bookings_by_day.items():
        print(f"{day}: {count}")
    
    # Find day with highest bookings
    max_day = bookings_by_day.idxmax()
    print(f"\nDay with highest number of bookings: {max_day} with {bookings_by_day[max_day]} bookings")
    
    # Create pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(bookings_by_day, labels=bookings_by_day.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribution of Bookings by Day of Week', fontsize=16)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
    plt.savefig('bookings_by_day_of_week_pie.png')
    plt.close()
    
    print("Pie chart saved as 'bookings_by_day_of_week_pie.png'")
    
    return bookings_by_day

def analyze_service_performance(bookings_df):
    """Analyze total bookings and GBV by service name"""
    print("\n4) SERVICE PERFORMANCE ANALYSIS")
    print("-" * 50)
    
    # Group by service name and aggregate
    service_performance = bookings_df.groupby('service_name').agg(
        total_bookings=('booking_id', 'count'),
        total_GBV_INR=('INR_Amount', 'sum')
    ).sort_values('total_bookings', ascending=False)
    
    print("Service Performance:")
    print(service_performance)
    
    # Create bar chart for visualization
    plt.figure(figsize=(12, 6))
    
    # Create subplots
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
    plt.savefig('service_performance.png')
    plt.close()
    
    print("Service performance chart saved as 'service_performance.png'")
    
    return service_performance

def analyze_most_booked_route_for_frequent_customers(bookings_df):
    """Find most booked route for customers with more than 1 booking"""
    print("\n5) MOST BOOKED ROUTE FOR FREQUENT CUSTOMERS")
    print("-" * 50)
    
    # Find customers with more than 1 booking
    frequent_customers = bookings_df.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique()
    
    print(f"Number of customers with more than 1 booking: {len(frequent_customers)}")
    
    # Filter bookings for these customers
    frequent_customer_bookings = bookings_df[bookings_df['customer_id'].isin(frequent_customers)]
    
    # Create route column
    frequent_customer_bookings['route'] = frequent_customer_bookings['from_city'] + ' to ' + frequent_customer_bookings['to_city']
    
    # Find the most booked route
    route_counts = frequent_customer_bookings['route'].value_counts()
    most_booked_route = route_counts.idxmax()
    most_booked_route_count = route_counts.max()
    
    print(f"Most booked route for frequent customers: {most_booked_route} with {most_booked_route_count} bookings")
    
    # Show top 5 routes
    print("\nTop 5 routes for frequent customers:")
    print(route_counts.head(5))
    
    return most_booked_route, most_booked_route_count

def analyze_advance_booking_cities(bookings_df):
    """Find top 3 departure cities where customers book mostly in advance"""
    print("\n6) TOP CITIES FOR ADVANCE BOOKINGS")
    print("-" * 50)
    
    # Group by departure city and filter for cities with at least 5 departures
    city_booking_stats = bookings_df.groupby('from_city').filter(lambda x: len(x) >= 5).groupby('from_city').agg(
        avg_days_to_departure=('days_to_departure', 'mean'),
        num_departures=('booking_id', 'count')
    ).sort_values('avg_days_to_departure', ascending=False)
    
    print("Top departure cities for advance bookings (with at least 5 departures):")
    print(city_booking_stats.head(3))
    
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
    plt.savefig('advance_booking_cities.png')
    plt.close()
    
    print("Top cities chart saved as 'advance_booking_cities.png'")
    
    return city_booking_stats.head(3)

def analyze_numerical_correlations(bookings_df):
    """Analyze correlations between numerical columns"""
    print("\n7) CORRELATION ANALYSIS OF NUMERICAL COLUMNS")
    print("-" * 50)
    
    # Select numerical columns
    numerical_columns = ['INR_Amount', 'no_of_passengers', 'days_to_departure', 'distance_km']
    
    # Calculate correlation matrix
    correlation_matrix = bookings_df[numerical_columns].corr()
    
    print("Correlation matrix of numerical columns:")
    print(correlation_matrix)
    
    # Find maximum correlation (excluding diagonal)
    corr_values = correlation_matrix.unstack()
    corr_values = corr_values[corr_values < 1.0]  # Exclude self-correlations (1.0)
    max_corr = corr_values.max()
    max_corr_pair = corr_values.idxmax()
    
    print(f"\nMaximum correlation: {max_corr:.4f} between {max_corr_pair[0]} and {max_corr_pair[1]}")
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
    plt.title('Correlation Matrix of Numerical Variables', fontsize=16)
    plt.tight_layout()
    plt.savefig('correlation_heatmap.png')
    plt.close()
    
    print("Correlation heatmap saved as 'correlation_heatmap.png'")
    
    return correlation_matrix, max_corr_pair, max_corr

def analyze_device_usage_by_service(bookings_df):
    """Find most used device type for each service"""
    print("\n8) DEVICE USAGE BY SERVICE")
    print("-" * 50)
    
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
    
    print("Most used device type by service:")
    for service, (device, count, percentage) in most_used_devices.items():
        print(f"{service}: {device} ({count} bookings, {percentage:.1f}% of service bookings)")
    
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
    plt.savefig('device_usage_by_service.png')
    plt.close()
    
    print("Device usage chart saved as 'device_usage_by_service.png'")
    
    return most_used_devices

def analyze_bookings_by_device_quarterly(bookings_df):
    """Plot time series of bookings by device type at quarterly frequency"""
    print("\n9) QUARTERLY BOOKING TRENDS BY DEVICE TYPE")
    print("-" * 50)
    
    # Create year-quarter field
    bookings_df['year_quarter'] = bookings_df['booking_year'].astype(str) + '-Q' + bookings_df['booking_quarter'].astype(str)
    
    # Group by year-quarter and device type
    quarterly_device_bookings = bookings_df.groupby(['year_quarter', 'device_type_used']).size().unstack(fill_value=0)
    
    print("Quarterly booking counts by device type:")
    print(quarterly_device_bookings)
    
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
    plt.savefig('quarterly_device_bookings.png')
    plt.close()
    
    print("Quarterly booking trends chart saved as 'quarterly_device_bookings.png'")
    
    return quarterly_device_bookings

def calculate_booking_search_ratio(bookings_df, sessions_df):
    """Calculate overall booking to search ratio (oBSR) metrics"""
    print("\n10) BOOKING TO SEARCH RATIO (oBSR) ANALYSIS")
    print("-" * 50)
    
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
    
    print("Average oBSR by month:")
    for month, ratio in monthly_obsr.items():
        print(f"{month}: {ratio:.4f}")
    
    # Average oBSR by day of week
    day_obsr = all_dates.groupby('day_of_week')['oBSR'].mean()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_obsr = day_obsr.reindex(day_order)
    
    print("\nAverage oBSR by day of week:")
    for day, ratio in day_obsr.items():
        print(f"{day}: {ratio:.4f}")
    
    # Create time series plot
    plt.figure(figsize=(14, 8))
    plt.plot(all_dates['date'], all_dates['oBSR'], marker='o', linestyle='-', color='purple')
    plt.title('Booking to Search Ratio (oBSR) Over Time', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('oBSR')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('obsr_time_series.png')
    plt.close()
    
    print("oBSR time series chart saved as 'obsr_time_series.png'")
    
    # Additional monthly chart
    plt.figure(figsize=(12, 6))
    monthly_obsr.plot(kind='bar', color='teal')
    plt.title('Average oBSR by Month', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Average oBSR')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('monthly_obsr.png')
    plt.close()
    
    # Additional day of week chart
    plt.figure(figsize=(12, 6))
    day_obsr.plot(kind='bar', color='orange')
    plt.title('Average oBSR by Day of Week', fontsize=16)
    plt.xlabel('Day of Week')
    plt.ylabel('Average oBSR')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('day_of_week_obsr.png')
    plt.close()
    
    print("Additional oBSR charts saved as 'monthly_obsr.png' and 'day_of_week_obsr.png'")
    
    return monthly_obsr, day_obsr, all_dates
def main():
    """Main function to execute all analyses"""
    print("=" * 80)
    print("MYNEXTBOOKING DATA ANALYSIS PROJECT")
    print("=" * 80)
    
    # Load data
    bookings_df, sessions_df = load_data()
    
    # Run all analyses
    analyze_distinct_counts(bookings_df, sessions_df)
    analyze_sessions_with_multiple_bookings(sessions_df)
    analyze_bookings_by_day_of_week(bookings_df)
    analyze_service_performance(bookings_df)
    analyze_most_booked_route_for_frequent_customers(bookings_df)
    analyze_advance_booking_cities(bookings_df)
    analyze_numerical_correlations(bookings_df)
    analyze_device_usage_by_service(bookings_df)
    analyze_bookings_by_device_quarterly(bookings_df)
    calculate_booking_search_ratio(bookings_df, sessions_df)
    
    print("\n" + "=" * 80)
    print("Analysis complete! All results and visualizations have been saved.")
    print("=" * 80)

if __name__ == "__main__":
    main()