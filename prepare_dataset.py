import pandas as pd


# Load Excel file
df = pd.read_excel("dataset/HDI.xlsx", skiprows=4)


print("Original Columns:")
print(df.columns.tolist())


# Rename columns
df = df.rename(columns={
    'Unnamed: 1': 'Country',
    'Human Development Index (HDI) ': 'HDI',
    'Life expectancy at birth': 'Life_Expectancy',
    'Expected years of schooling': 'Expected_Schooling',
    'Mean years of schooling': 'Mean_Schooling',
    'Gross national income (GNI) per capita': 'GNI_Per_Capita'
})


# Remove unwanted columns
df = df[
    [
        'Country',
        'Life_Expectancy',
        'Expected_Schooling',
        'Mean_Schooling',
        'GNI_Per_Capita',
        'HDI'
    ]
]


# Remove rows containing text headers
df = df[df['Country'].notna()]


# Convert numeric columns
columns = [
    'Life_Expectancy',
    'Expected_Schooling',
    'Mean_Schooling',
    'GNI_Per_Capita',
    'HDI'
]


for col in columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')


# Remove empty values
df = df.dropna()


# Create HDI category
def category(value):

    if value >= 0.800:
        return "Very High"

    elif value >= 0.700:
        return "High"

    elif value >= 0.550:
        return "Medium"

    else:
        return "Low"


df['HDI_Category'] = df['HDI'].apply(category)


# Save cleaned dataset
df.to_csv("dataset/clean_hdi.csv", index=False)


print("\nDataset cleaned successfully!")
print(df.head())

print("\nShape:")
print(df.shape)

print("\nCategories:")
print(df['HDI_Category'].value_counts())