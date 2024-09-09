import numpy as np
import pandas as pd

# Function to generate random service dataset
def generate_random_service_dataset(num_services):
    np.random.seed(0)  # To make the results reproducible

    # Generate random data
    ids = np.arange(1, num_services + 1)
    titles = np.random.choice(['Consulting', 'Software Development', 'Marketing Strategy', 'SEO Optimization',
                               'Data Analysis', 'Cloud Migration', 'Cybersecurity Assessment',
                               'Web Design', 'Mobile App Development', 'Customer Support'], size=num_services)
    descriptions = np.random.choice(['High-quality service', 'Affordable and reliable', 'Expert-led service',
                                     'Top-rated by clients', 'Comprehensive and efficient'], size=num_services)
    base_prices = np.random.randint(100, 1000, size=num_services)
    availability = np.random.choice([True, False], size=num_services)
    owners = np.random.choice(['Provider A', 'Provider B', 'Provider C'], size=num_services)
    total_reviews = np.random.randint(1, 1000, size=num_services)
    average_stars = np.round(np.random.uniform(1, 5, size=num_services), 1)  # Stars between 1 and 5
    plus_achetes = np.random.randint(1, 500, size=num_services)  # Additional attribute

    # Create a DataFrame
    data = {
        'ID': ids,
        'Title': titles,
        'Description': descriptions,
        'Base Price': base_prices,
        'Availability': availability,
        'Owner': owners,
        'Total Reviews': total_reviews,
        'Average Stars': average_stars,
        'Plus Achetés': plus_achetes
    }

    return pd.DataFrame(data)

# Generate a dataset of 1000+ services
num_services = 1000
service_dataset = generate_random_service_dataset(num_services)

# Save the dataset to a CSV file
csv_filename = 'random_service_dataset.csv'
service_dataset.to_csv(csv_filename, index=False)

# Display a message when the file is saved
print(f"Dataset saved to {csv_filename}")
