def check(data):
    #check for missing values
    def check_missing_values(data):
        missing_vals = data.isnull().sum()
        print("Missing Values:\n", missing_vals,'\n')
        return missing_vals

    #check for outliers (for daily return)
    def check_outliers(data, threshold=3):
        z_scores = (data['Daily_Return'] - data['Daily_Return'].mean()) / data['Daily_Return'].std()
        outliers = data[(np.abs(z_scores) > threshold)]
        print("Outliers:\n", outliers,'\n')
        return outliers

    #check for extreme price changes
    def check_extreme_price_change(data):
        extreme_change = data[abs((data['Close'] - data['Open']) / data['Open']) > 0.2]
        print("Extreme Price Changes:\n", extreme_change,'\n')
        return extreme_change

    #check for duplicates
    def check_duplicates(data):
        duplicates = data.duplicated().sum()
        print("Duplicates:\n", duplicates,'\n')
        return duplicates


def clean(data):
    #handle missing values: Fill with forward fill method
    def handle_missing_values(data):
        data = data.fillna(method='ffill')
        return data
    """
    # Handle outliers: Replace outliers using mean value
    def handle_outliers(data, threshold=3):
        z_scores = (data['Daily_Return'] - data['Daily_Return'].mean()) / data['Daily_Return'].std()
        outliers = (np.abs(z_scores) > threshold)
        if outliers.any():
            mean_value = data.loc[~outliers, 'Daily_Return'].mean()
            data.loc[outliers, 'Daily_Return'] = mean_value
        return data
    """

    #drop duplicates
    def drop_duplicates(data):
        data = data.drop_duplicates()
        print("Duplicates dropped")
        return data
