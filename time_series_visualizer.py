import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df.loc[(df['value'] <= df['value'].quantile(0.975)) & (df['value'] >= df['value'].quantile(0.025))]


def draw_line_plot():

    fig, ax = plt.subplots(figsize=(12,6))
    ax.plot(df.index, df['value'], color='red', linewidth=1.5)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    plt.tight_layout()
    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar_data = df.copy()
    df_bar_data["date"] = pd.to_datetime(df.index)
    df_bar_data['year'] = df_bar_data['date'].dt.year
    df_bar_data['month'] = df_bar_data['date'].dt.month
    df_bar = df_bar_data.groupby(['year', 'month'])['value'].mean().round(2).unstack()

    fig, ax = plt.subplots(figsize=(12,6))

    df_bar.plot(kind='bar', ax=ax)
    ax.set_title('Average Daily Page Views by Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    ax.legend(title='Months', labels=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])

    plt.tight_layout()
    plt.show()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    
    fig, axes = plt.subplots(1, 2, figsize=(20,6))
    
    df_year = df_box.copy()
    sns.boxplot(data=df_year, x='year', y='value', ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    df_month = df_box.copy()
    sns.boxplot(data=df_month, x='month', y='value', order=month_order, ax=axes[1])
    
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    fig.savefig('box_plot.png')
    return fig
