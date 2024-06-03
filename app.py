from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def home():
    # Read the dataset
    df = pd.read_csv("Universities_Schoolarships_All_Around_the_World.csv")

    # Data cleaning and standardization
    df['degrees'] = df['degrees'].str.strip().str.lower()
    df['location'] = df['location'].str.strip()

    # Standardize degree categories
    degree_mapping = {
        'master': "Master's",
        'bachelor': "Bachelor's",
        'phd': 'PhD',
        'course': 'Course'
    }
    df['degrees'] = df['degrees'].map(degree_mapping)

    # Create a pivot table to count scholarships by degree and location
    pivot_table = df.pivot_table(index='location', columns='degrees', aggfunc='size', fill_value=0)

    # Generate the heatmap
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 8))

    sns.heatmap(pivot_table, cmap='Blues', annot=True, fmt='d', linewidths=.5, ax=axes[0])
    axes[0].set_title('Scholarship Counts by Degree and Location')
    axes[0].set_xlabel('Degree')
    axes[0].set_ylabel('Location')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45)

    pivot_table.plot(kind='bar', stacked=True, ax=axes[1], color=['skyblue', 'lightgreen', 'lightcoral', 'lightsalmon'])
    axes[1].set_title('Distribution of Scholarships by Degree and Location')
    axes[1].set_xlabel('Location')
    axes[1].set_ylabel('Number of Scholarships')
    axes[1].legend(title='Degree')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45)

    plt.tight_layout()

    # Save plot to a string in base64 format
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
