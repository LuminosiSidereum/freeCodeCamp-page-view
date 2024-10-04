#%%
import matplotlib.pyplot as plt #type: ignore
import pandas as pd #type: ignore
import seaborn as sns #type: ignore
from pandas.plotting import register_matplotlib_converters #type: ignore
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",parse_dates=["date"]).set_index("date")

# Clean data
df = df[(df["value"] >= df["value"].quantile(0.025)) & (df["value"] <= df["value"].quantile(0.975))]

#%%
def draw_line_plot():
#%%
    # Draw line 
    plt.figure(figsize=(20,6))
    plt.plot(df["value"],color="red")

    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")

    fig = plt.gcf()   
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
#%%
    return fig

def draw_bar_plot():
#%%
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Months"] = pd.DatetimeIndex(df_bar.index).month
    df_bar["year"] = pd.DatetimeIndex(df_bar.index).year
    df_bar = df_bar.groupby(["year","Months"])["value"].mean().reset_index()
    df_bar_pivot = df_bar.pivot(values="value",index="year",columns="Months")
    
    month_order = {1: 'January',
                   2: 'February',
                   3: 'March',
                   4: 'April',
                   5: 'May', 
                   6: 'June', 
                   7: 'July', 
                   8: 'August',
                   9: 'September', 
                   10: 'October', 
                   11: 'November', 
                   12: 'December'}

    df_bar_pivot = df_bar_pivot.rename(columns=month_order)
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10,6))
    df_bar_pivot.plot(kind="bar",ax=ax)
    
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
#%%
    return fig

def draw_box_plot():
#%%
   # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    plt.figure(figsize=(25,10))
    plt.subplot(1, 2, 1)
    sns.boxplot(x="year", y="value", data=df_box ,palette="pastel")
    plt.title("Year-wise Box Plot (Trend)")
    plt.xlabel("Year")
    plt.ylabel("Page Views")

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    plt.subplot(1, 2, 2)
    sns.boxplot(x="month", y="value", data=df_box, order=month_order,palette="pastel")
    plt.title("Month-wise Box Plot (Seasonality)")
    plt.xlabel("Month")
    plt.ylabel("Page Views")

    plt.tight_layout()
    fig = plt.gcf()   
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
#%%
    return fig
