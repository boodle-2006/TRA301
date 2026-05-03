import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})

INPUT_FILE = "weat_genre_results.csv"

GENRE_COLORS = {
    "Pop": "#e74c3c",       # Red
    "Rock": "#3498db",      # Blue
    "R&B/Soul": "#9b59b6",  # Purple
    "Country": "#f39c12",   # Orange
    "Hip-Hop": "#2ecc71"    # Green
}

def load_data():
    try:
        df = pd.read_csv(INPUT_FILE)
        df = df[df['status'] != 'no_lyrics'].copy()
        df = df[df['racial_name_association'].notna()].copy()
        return df
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Run weat_genre_analysis.py first.")
        return None

def plot_genre_trends(df):
    """Plot line chart comparing genres over time."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    decades = sorted(df['decade'].unique())
    
    for genre in sorted(df['genre'].unique()):
        genre_df = df[df['genre'] == genre]
        if len(genre_df) == 0:
            continue
            
        avg_by_decade = genre_df.groupby('decade')['racial_name_association'].mean()
        
        if not avg_by_decade.empty:
            color = GENRE_COLORS.get(genre, 'black')
            ax.plot(avg_by_decade.index, avg_by_decade.values, 
                    marker='o', linewidth=2.5, markersize=8, 
                    label=genre, color=color, alpha=0.8)

    ax.axhline(y=0, color='black', linewidth=1.5, linestyle='--', alpha=0.5)
    
    ax.set_xlabel('Decade', fontweight='bold')
    ax.set_ylabel('Mean Racial Name Association Score', fontweight='bold')
    ax.set_title('Racial Bias in Lyrics by Genre Over Time\n(Positive = closer to EA names, Negative = closer to AA names)',
                 fontweight='bold', fontsize=13)
    
    ax.set_xticks(decades)
    ax.set_xticklabels([f"{d}s" for d in decades])
    ax.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('plot_genre_trends.png')
    print("  Saved: plot_genre_trends.png")
    plt.close()

def plot_genre_heatmap(df):
    """Plot a heatmap of average scores by Genre vs Decade."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    pivot = df.pivot_table(values='racial_name_association', 
                           index='genre', 
                           columns='decade', 
                           aggfunc='mean')
    
    # Sort genres nicely
    genres_sorted = ["Pop", "Rock", "Country", "R&B/Soul", "Hip-Hop"]
    genres_present = [g for g in genres_sorted if g in pivot.index]
    pivot = pivot.reindex(genres_present)
    
    pivot.columns = [f"{c}s" for c in pivot.columns]
    
    # Custom colormap: Blue (negative/AA) to White (neutral) to Red (positive/EA)
    sns.heatmap(pivot, annot=True, fmt=".4f", cmap="coolwarm", center=0, 
                cbar_kws={'label': 'Racial Name Association'}, ax=ax,
                linewidths=1, linecolor='white')
    
    ax.set_title('Average Racial Bias by Genre and Decade', fontweight='bold', pad=20)
    ax.set_ylabel('Genre', fontweight='bold')
    ax.set_xlabel('Decade', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plot_genre_heatmap.png')
    print("  Saved: plot_genre_heatmap.png")
    plt.close()

def plot_genre_distribution(df):
    """Plot violin plots showing score distribution per genre overall."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    genres_sorted = ["Pop", "Rock", "Country", "R&B/Soul", "Hip-Hop"]
    genres_present = [g for g in genres_sorted if g in df['genre'].unique()]
    
    sns.violinplot(data=df, x='genre', y='racial_name_association', 
                   order=genres_present, palette=GENRE_COLORS, ax=ax, inner="quartile")
    
    # Overlay points
    sns.stripplot(data=df, x='genre', y='racial_name_association', 
                  order=genres_present, color='black', alpha=0.3, size=4, jitter=True, ax=ax)
    
    ax.axhline(y=0, color='black', linewidth=1.5, linestyle='--', alpha=0.5)
    
    ax.set_title('Overall Score Distribution by Genre (1950-2020)', fontweight='bold')
    ax.set_ylabel('Racial Name Association Score', fontweight='bold')
    ax.set_xlabel('Genre', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plot_genre_distribution.png')
    print("  Saved: plot_genre_distribution.png")
    plt.close()

def main():
    print("Loading genre results...")
    df = load_data()
    if df is None:
        return
        
    print(f"Loaded {len(df)} genre-labeled song results.\n")

    print("Generating visualizations...")
    plot_genre_trends(df)
    plot_genre_heatmap(df)
    plot_genre_distribution(df)

if __name__ == "__main__":
    main()
