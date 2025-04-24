from django.shortcuts import render
from analysis_utils import (
    load_data, 
    get_distinct_counts, 
    get_sessions_with_multiple_bookings,
    get_bookings_by_day_of_week,
    get_service_performance,
    get_most_booked_routes,
    get_advance_booking_cities,
    get_correlation_analysis,
    get_device_usage,
    get_quarterly_device_bookings,
    get_booking_search_ratio
)

def index(request):
    """Dashboard home page with summary statistics"""
    bookings_df, sessions_df = load_data()
    distinct_bookings, distinct_sessions, distinct_searches = get_distinct_counts(bookings_df, sessions_df)
    sessions_with_multiple_bookings = get_sessions_with_multiple_bookings(sessions_df)
    
    # Calculate overall conversion rate
    conversion_rate = (distinct_bookings / distinct_searches) * 100
    
    context = {
        'distinct_bookings': distinct_bookings,
        'distinct_sessions': distinct_sessions,
        'distinct_searches': distinct_searches,
        'sessions_with_multiple_bookings': sessions_with_multiple_bookings,
        'conversion_rate': conversion_rate
    }
    return render(request, 'dashboard/index.html', context)

def bookings_by_day(request):
    """View for bookings by day of week analysis"""
    bookings_df, _ = load_data()
    bookings_by_day, max_day, max_bookings, plot_data = get_bookings_by_day_of_week(bookings_df)
    
    # Prepare data for the table
    day_data = [{'day': day, 'bookings': bookings_by_day[day]} for day in bookings_by_day.index]
    
    context = {
        'day_data': day_data,
        'max_day': max_day,
        'max_bookings': max_bookings,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/bookings_by_day.html', context)

def service_performance(request):
    """View for service performance analysis"""
    bookings_df, _ = load_data()
    service_perf, plot_data = get_service_performance(bookings_df)
    
    # Convert DataFrame to list of dictionaries for template
    service_data = []
    for index, row in service_perf.iterrows():
        service_data.append({
            'service_name': index,
            'total_bookings': row['total_bookings'],
            'total_GBV_INR': f"₹{row['total_GBV_INR']:,.2f}"
        })
    
    context = {
        'service_data': service_data,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/service_performance.html', context)

def most_booked_routes(request):
    """View for most booked routes analysis"""
    bookings_df, _ = load_data()
    frequent_customers_count, most_booked_route, most_booked_count, top_routes, plot_data = get_most_booked_routes(bookings_df)
    
    # Convert Series to list of dictionaries for template
    route_data = []
    for route, count in top_routes.items():
        route_data.append({
            'route': route,
            'count': count
        })
    
    context = {
        'frequent_customers_count': frequent_customers_count,
        'most_booked_route': most_booked_route,
        'most_booked_count': most_booked_count,
        'route_data': route_data,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/most_booked_routes.html', context)

def advance_booking_cities(request):
    """View for advance booking cities analysis"""
    bookings_df, _ = load_data()
    city_stats, plot_data = get_advance_booking_cities(bookings_df)
    
    # Convert DataFrame to list of dictionaries for template
    city_data = []
    for index, row in city_stats.iterrows():
        city_data.append({
            'city': index,
            'avg_days': f"{row['avg_days_to_departure']:.2f}",
            'num_departures': row['num_departures']
        })
    
    context = {
        'city_data': city_data,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/advance_booking_cities.html', context)

def correlation_analysis(request):
    """View for correlation analysis"""
    bookings_df, _ = load_data()
    corr_matrix, max_corr_pair, max_corr, plot_data = get_correlation_analysis(bookings_df)
    
    # Convert correlation matrix to list for template
    corr_data = []
    for col in corr_matrix.columns:
        row_data = []
        for idx in corr_matrix.index:
            row_data.append({
                'col': col,
                'row': idx,
                'value': f"{corr_matrix.loc[idx, col]:.2f}"
            })
        corr_data.append(row_data)
    
    context = {
        'corr_data': corr_data,
        'max_corr_var1': max_corr_pair[0],
        'max_corr_var2': max_corr_pair[1],
        'max_corr_value': f"{max_corr:.4f}",
        'plot_data': plot_data
    }
    return render(request, 'dashboard/correlation_analysis.html', context)

def device_usage(request):
    """View for device usage by service analysis"""
    bookings_df, _ = load_data()
    most_used_devices, pivot_data, plot_data = get_device_usage(bookings_df)
    
    # Convert most_used_devices dictionary to list for template
    device_data = []
    for service, (device, count, percentage) in most_used_devices.items():
        device_data.append({
            'service': service,
            'device': device,
            'count': count,
            'percentage': f"{percentage:.1f}%"
        })
    
    context = {
        'device_data': device_data,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/device_usage.html', context)

def quarterly_trends(request):
    """View for quarterly booking trends analysis"""
    bookings_df, _ = load_data()
    quarterly_bookings, plot_data = get_quarterly_device_bookings(bookings_df)
    
    # Convert DataFrame to list of dictionaries for template
    quarter_data = []
    for quarter, row in quarterly_bookings.iterrows():
        quarter_dict = {'quarter': quarter}
        for device in row.index:
            quarter_dict[device] = int(row[device])
        quarter_data.append(quarter_dict)
    
    # Get device types for table headers
    device_types = quarterly_bookings.columns.tolist()
    
    context = {
        'quarter_data': quarter_data,
        'device_types': device_types,
        'plot_data': plot_data
    }
    return render(request, 'dashboard/quarterly_trends.html', context)

def booking_search_ratio(request):
    """View for booking to search ratio analysis"""
    bookings_df, sessions_df = load_data()
    monthly_obsr, day_obsr, ts_plot_data, monthly_plot_data, day_plot_data = get_booking_search_ratio(bookings_df, sessions_df)
    
    # Convert Series to list of dictionaries for templates
    monthly_data = []
    for month, ratio in monthly_obsr.items():
        monthly_data.append({
            'month': month,
            'ratio': f"{ratio:.4f}"
        })
    
    day_data = []
    for day, ratio in day_obsr.items():
        day_data.append({
            'day': day,
            'ratio': f"{ratio:.4f}"
        })
    
    context = {
        'monthly_data': monthly_data,
        'day_data': day_data,
        'ts_plot_data': ts_plot_data,
        'monthly_plot_data': monthly_plot_data,
        'day_plot_data': day_plot_data
    }
    return render(request, 'dashboard/booking_search_ratio.html', context)