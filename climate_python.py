import csv
import time
from datetime import datetime
from collections import defaultdict

# Define the ClimateData class for data representation
class ClimateData:
    def __init__(self, LOCAL_DATE,SPEED_MAX_GUST,TOTAL_PRECIPITATION,MIN_TEMPERATURE,MAX_TEMPERATURE,MEAN_TEMPERATURE):
        self.local_date = LOCAL_DATE
        self.speed_max_gust = SPEED_MAX_GUST
        self.total_precipitation = TOTAL_PRECIPITATION
        self.min_temperature = MIN_TEMPERATURE
        self.max_temperature = MAX_TEMPERATURE
        self.mean_temperature = MEAN_TEMPERATURE

    @classmethod
    def from_csv_row(cls, row):
        # Parse the date
        local_date = datetime.strptime(row['LOCAL_DATE'], '%Y-%m-%d %H:%M')
        
        # Parse numeric fields with proper error handling
        try:
            speed_max_gust = float(row['SPEED_MAX_GUST']) if row['SPEED_MAX_GUST'] else None
            total_precipitation = float(row['TOTAL_PRECIPITATION']) if row['TOTAL_PRECIPITATION'] else 0.0
            min_temperature = float(row['MIN_TEMPERATURE']) if row['MIN_TEMPERATURE'] else None
            max_temperature = float(row['MAX_TEMPERATURE']) if row['MAX_TEMPERATURE'] else None
            mean_temperature = float(row['MEAN_TEMPERATURE']) if row['MEAN_TEMPERATURE'] else None
        except ValueError:
            # Skip malformed records
            return None
        
        return cls(local_date, speed_max_gust, total_precipitation, min_temperature, max_temperature, mean_temperature)

# Load and Parse the CSV data
def load_and_parse_csv(filename):
    data = []
    with open(filename, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            record = ClimateData.from_csv_row(row)
            if record:
                data.append(record)
    return data

# Analysis functions
def analyze_data(data):
    # Initialize containers for analysis
    precipitation_by_month = defaultdict(float)
    highest_gust_day = {'speed': 0, 'date': None}
    largest_temp_fluctuation_day = {'fluctuation': 0, 'date': None}

    for record in data:
        # Update total precipitation by month
        month_year_key = record.local_date.strftime('%B %Y')
        precipitation_by_month[month_year_key] += record.total_precipitation

        # Update highest speed max gust
        if record.speed_max_gust and record.speed_max_gust > highest_gust_day['speed']:
            highest_gust_day = {'speed': record.speed_max_gust, 'date': record.local_date}

        # Update largest temperature fluctuation
        if record.min_temperature is not None and record.max_temperature is not None:
            fluctuation = record.max_temperature - record.min_temperature
            if fluctuation > largest_temp_fluctuation_day['fluctuation']:
                largest_temp_fluctuation_day = {'fluctuation': fluctuation, 'date': record.local_date}

    # Find month with highest total precipitation
    highest_precipitation_month = max(precipitation_by_month, key=precipitation_by_month.get)
    highest_precipitation_amount = precipitation_by_month[highest_precipitation_month]

    return {
        'highest_precipitation_month': highest_precipitation_month,
        'highest_precipitation_amount': highest_precipitation_amount,
        'highest_gust_day': highest_gust_day,
        'largest_temp_fluctuation_day': largest_temp_fluctuation_day,
    }

# Example usage:
filename = 'climate-daily.csv'
data = load_and_parse_csv(filename)
analysis_results = analyze_data(data)
print(analysis_results)

def generate_monthly_reports(climate_data_list):
    monthly_data = defaultdict(list)

    for data in climate_data_list:
        month_year = data.local_date.strftime('%B %Y')
        monthly_data[month_year].append(data)

    for month_year, data_list in monthly_data.items():
        avg_speed_max_gust = sum(data.speed_max_gust for data in data_list if data.speed_max_gust is not None) / len([data for data in data_list if data.speed_max_gust is not None])
        avg_total_precipitation = sum(data.total_precipitation for data in data_list) / len(data_list)
        min_temperatures = [data.min_temperature for data in data_list if data.min_temperature is not None]
        min_temperature = min(min_temperatures) if min_temperatures else None
        max_temperature = max((data.max_temperature for data in data_list if data.max_temperature is not None), default=None)
        mean_temperatures = [data.mean_temperature for data in data_list if data.mean_temperature is not None]
        avg_mean_temperature = sum(mean_temperatures) / len(mean_temperatures) if mean_temperatures else None


        print(f"\nReport for {month_year}:")
        print(f"Average SPEED_MAX_GUST: {avg_speed_max_gust} km/h")
        print(f"Average TOTAL_PRECIPITATION: {avg_total_precipitation} mm")
        print(f"MIN_TEMPERATURE: {min_temperature} °C")
        print(f"MAX_TEMPERATURE: {max_temperature} °C")
        print(f"Average MEAN_TEMPERATURE: {avg_mean_temperature} °C")

def generate_records_between_dates(climate_data_list, start_date, end_date):
    # Convert input strings to date objects
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError as e:
        print(f"Error: {e}. Please enter the date in 'YYYY-MM-DD' format.")
        # Here you might want to loop back and ask for the input again or exit the function

    # Ensure the dates are within the range of the dataset
    # Assuming you know the range of your dataset
    data_start_date = datetime(2010, 1, 1)  # Replace with your dataset's start date
    data_end_date = datetime(2024, 12, 31)  # Replace with your dataset's end date

    if start_date < data_start_date or end_date > data_end_date or start_date > end_date:
        print("Dates are out of the range of the dataset or invalid range.")
    else:
        generate_records_between_dates(climate_data_list, start_date, end_date)

if __name__ == "__main__":
    file_path = 'climate-daily.csv'
    climate_data_list = load_and_parse_csv(file_path)

while True:
    print("\nSelect an option:")
    print("1. Generate Monthly Reports")
    print("2. Generate Records Between Dates")
    print("3. Exit")
    
    choice = input("Enter your choice (1, 2, or 3): ")

    if choice == '1':
        start_time = time.time()
        generate_monthly_reports(climate_data_list)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"The `generate_monthly_reports` function took {elapsed_time:.3f} seconds to complete.")
    elif choice == '2':
        start_date_str = input("Enter the start date (YYYY-MM-DD): ")
        end_date_str = input("Enter the end date (YYYY-MM-DD): ")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError as e:
            print(f"Error: {e}. Please enter the date in 'YYYY-MM-DD' format.")
            # Exit or ask for the dates again

        # Now call the function with the parsed dates
        generate_records_between_dates(climate_data_list, start_date, end_date)
    elif choice == '3':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
