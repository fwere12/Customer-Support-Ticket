import pandas as pd

def download_cleaned_dataset():
    """
    Load and clean the dataset.
    
    Returns:
        DataFrame: The cleaned dataset.
    """
    # Load the dataset
    df = pd.read_csv(r"C:\Users\Faith\Documents\GitHub\Customer-Support-Ticket\customer_support_tickets.csv")
    
    # Convert columns to datetime
    df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'], format='%Y-%m-%d')
    df['First Response Time'] = pd.to_datetime(df['First Response Time'], format='%Y-%m-%d %H:%M:%S')
    df['Time to Resolution'] = pd.to_datetime(df['Time to Resolution'], format='%Y-%m-%d %H:%M:%S')

    # Drop Ticket ID column
    df = df.drop(columns=['Ticket ID'])

    # Fill missing values
    df['Resolution'] = df['Resolution'].fillna('None')
    df['First Response Time'] = df['First Response Time'].fillna('No response')
    df['Time to Resolution'] = df['Time to Resolution'].fillna('No resolution')
    df['Customer Satisfaction Rating'] = df['Customer Satisfaction Rating'].fillna('No rating')

    # Save the cleaned dataset to CSV
    cleaned_file_path = "cleaned_customer_support_tickets.csv"
    df.to_csv(cleaned_file_path, index=False)
    print(f"Cleaned dataset saved to {downloads}")
    
    return df

# Download and get the cleaned dataset
cleaned_dataset = download_cleaned_dataset()
