import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.ticker import MaxNLocator

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 200,
    'savefig.bbox': 'tight',
})

INPUT_FILE = "weat_results.csv"


def load_data():
    df = pd.read_csv(INPUT_FILE)
    df = df[df['status'] != 'no_lyrics'].copy() 
    return df


def plot_decade_trend(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    decade_avg = df.groupby('decade')['racial_name_association'].agg(['mean', 'std', 'count']).reset_index()
    decade_avg.columns = ['decade', 'mean', 'std', 'count']
    decade_avg['se'] = decade_avg['std'] / np.sqrt(decade_avg['count'])

    decades = decade_avg['decade'].values
    means = decade_avg['mean'].values
    ses = decade_avg['se'].values

    colors = ['#e74c3c' if m > 0 else '#3498db' for m in means]

    bars = ax.bar(decades, means, width=4, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
    ax.errorbar(decades, means, yerr=ses, fmt='none', ecolor='gray', capsize=5, capthick=1.5, linewidth=1.5)
    z = np.polyfit(decades, means, 2)
    p = np.poly1d(z)
    x_smooth = np.linspace(min(decades), max(decades), 100)
    ax.plot(x_smooth, p(x_smooth), '--', color='#2c3e50', linewidth=2, alpha=0.7, label='Quadratic trend')

    ax.axhline(y=0, color='black', linewidth=1, linestyle='-', alpha=0.3)

    ax.set_xlabel('Decade', fontweight='bold')
    ax.set_ylabel('Mean Racial Name Association Score', fontweight='bold')
    ax.set_title('Racial Bias in Popular Song Lyrics Over Time\n(WEAT Association with European American vs. African American Names)',
                 fontweight='bold', fontsize=13)

    ea_patch = mpatches.Patch(color='#e74c3c', alpha=0.8, label='Closer to EA names (positive)')
    aa_patch = mpatches.Patch(color='#3498db', alpha=0.8, label='Closer to AA names (negative)')
    ax.legend(handles=[ea_patch, aa_patch], loc='upper right', framealpha=0.9)

    ax.set_xticks(decades)
    ax.set_xticklabels([f"{d}s" if d < 2000 else str(d) for d in decades], rotation=45)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('plot_decade_trend.png')
    print("  Saved: plot_decade_trend.png")
    plt.close()


def plot_per_song_heatmap(df):
    df_plot = df[df['racial_name_association'].notna()].copy()
    df_plot['label'] = df_plot['artist'] + '\n' + df_plot['title']

    fig, ax = plt.subplots(figsize=(14, 16))

    decades = sorted(df_plot['decade'].unique())
    all_labels = []
    heatmap_data = []

    for decade in decades:
        decade_songs = df_plot[df_plot['decade'] == decade].sort_values('racial_name_association', ascending=False)
        for _, row in decade_songs.iterrows():
            all_labels.append(f"{row['artist']} - {row['title']} ({decade}s)")
            heatmap_data.append(row['racial_name_association'])

    colors = ['#e74c3c' if v > 0 else '#3498db' for v in heatmap_data]

    y_pos = np.arange(len(all_labels))
    ax.barh(y_pos, heatmap_data, color=colors, alpha=0.8, height=0.7, edgecolor='white', linewidth=0.5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(all_labels, fontsize=7)
    ax.invert_yaxis()

    ax.axvline(x=0, color='black', linewidth=1, alpha=0.5)
    ax.set_xlabel('Racial Name Association Score', fontweight='bold')
    ax.set_title('Per-Song Racial Name Association\n(Positive = closer to EA names, Negative = closer to AA names)',
                 fontweight='bold')

    song_count = 0
    for decade in decades:
        n = len(df_plot[df_plot['decade'] == decade])
        if song_count > 0:
            ax.axhline(y=song_count - 0.5, color='gray', linewidth=1.5, linestyle='--', alpha=0.5)
        song_count += n

    ax.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.savefig('plot_per_song.png')
    print("  Saved: plot_per_song.png")
    plt.close()


def plot_weat_effect_by_decade(df):
    fig, ax = plt.subplots(figsize=(12, 6))

    decade_weat = df.groupby('decade')['weat_effect_size'].first().reset_index()
    decades = decade_weat['decade'].values
    effects = decade_weat['weat_effect_size'].values

    colors = ['#e74c3c' if e > 0 else '#3498db' for e in effects]
    ax.bar(decades, effects, width=4, color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)

    ax.axhline(y=0, color='black', linewidth=1, alpha=0.3)

    ax.axhline(y=0.2, color='orange', linewidth=1, linestyle=':', alpha=0.5)
    ax.axhline(y=-0.2, color='orange', linewidth=1, linestyle=':', alpha=0.5)
    ax.axhline(y=0.8, color='red', linewidth=1, linestyle=':', alpha=0.5)
    ax.axhline(y=-0.8, color='red', linewidth=1, linestyle=':', alpha=0.5)

    ax.text(max(decades) + 3, 0.2, 'small effect', fontsize=8, color='orange', alpha=0.7, va='center')
    ax.text(max(decades) + 3, 0.8, 'large effect', fontsize=8, color='red', alpha=0.7, va='center')

    ax.set_xlabel('Decade', fontweight='bold')
    ax.set_ylabel('WEAT Effect Size (Cohen\'s d)', fontweight='bold')
    ax.set_title('WEAT Effect Size Across Decades\n(EA Names/AA Names × Pleasant/Unpleasant Attributes)',
                 fontweight='bold')

    ax.set_xticks(decades)
    ax.set_xticklabels([f"{d}s" if d < 2000 else str(d) for d in decades], rotation=45)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('plot_weat_effect.png')
    print("  Saved: plot_weat_effect.png")
    plt.close()


def plot_distribution_by_decade(df):
    df_plot = df[df['racial_name_association'].notna()].copy()
    df_plot['decade_label'] = df_plot['decade'].apply(lambda x: f"{x}s" if x < 2000 else str(x))

    fig, ax = plt.subplots(figsize=(12, 6))

    decades_sorted = sorted(df_plot['decade_label'].unique())

    parts = ax.violinplot(
        [df_plot[df_plot['decade_label'] == d]['racial_name_association'].values for d in decades_sorted],
        positions=range(len(decades_sorted)),
        showmeans=True,
        showmedians=True,
    )

    for pc in parts['bodies']:
        pc.set_facecolor('#9b59b6')
        pc.set_alpha(0.3)
    for i, d in enumerate(decades_sorted):
        vals = df_plot[df_plot['decade_label'] == d]['racial_name_association'].values
        jitter = np.random.normal(0, 0.05, len(vals))
        ax.scatter(np.full_like(vals, i) + jitter, vals, alpha=0.7, s=40,
                   color=['#e74c3c' if v > 0 else '#3498db' for v in vals],
                   edgecolor='white', linewidth=0.5, zorder=5)

    ax.axhline(y=0, color='black', linewidth=1, alpha=0.3)

    ax.set_xticks(range(len(decades_sorted)))
    ax.set_xticklabels(decades_sorted, rotation=45)
    ax.set_xlabel('Decade', fontweight='bold')
    ax.set_ylabel('Racial Name Association Score', fontweight='bold')
    ax.set_title('Distribution of Per-Song Racial Bias Scores by Decade',
                 fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('plot_distribution.png')
    print("  Saved: plot_distribution.png")
    plt.close()


def plot_vocab_coverage(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    decade_stats = df.groupby('decade').agg({
        'unique_content_words': 'mean',
        'words_in_vocab': 'mean',
    }).reset_index()

    decades = decade_stats['decade'].values

    coverage = decade_stats['words_in_vocab'] / decade_stats['unique_content_words'] * 100

    ax1.bar(decades, decade_stats['unique_content_words'], width=4, alpha=0.4,
            color='#3498db', label='Total unique content words')
    ax1.bar(decades, decade_stats['words_in_vocab'], width=4, alpha=0.8,
            color='#2ecc71', label='Found in SGNS vocab')

    ax1.set_xlabel('Decade', fontweight='bold')
    ax1.set_ylabel('Average Words per Song', fontweight='bold')
    ax1.set_title('Vocabulary Coverage', fontweight='bold')
    ax1.set_xticks(decades)
    ax1.set_xticklabels([f"{d}s" if d < 2000 else str(d) for d in decades], rotation=45)
    ax1.legend(loc='upper left')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    ax2.plot(decades, coverage, 'o-', color='#e67e22', linewidth=2, markersize=8)
    ax2.fill_between(decades, coverage, alpha=0.2, color='#e67e22')
    ax2.set_xlabel('Decade', fontweight='bold')
    ax2.set_ylabel('Coverage (%)', fontweight='bold')
    ax2.set_title('% of Lyric Words Found in SGNS Vocab', fontweight='bold')
    ax2.set_xticks(decades)
    ax2.set_xticklabels([f"{d}s" if d < 2000 else str(d) for d in decades], rotation=45)
    ax2.set_ylim(0, 100)
    ax2.grid(alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig('plot_vocab_coverage.png')
    print("  Saved: plot_vocab_coverage.png")
    plt.close()


def print_summary_table(df):
    print(f"\n{'='*80}")
    print("  RESULTS SUMMARY TABLE")
    print(f"{'='*80}")
    print(f"{'Decade':<10} {'Mean Assoc':>11} {'Std':>8} {'WEAT d':>8} {'Songs':>6} {'Interpretation'}")
    print(f"{'-'*80}")

    for decade in sorted(df['decade'].unique()):
        dd = df[df['decade'] == decade]
        valid = dd['racial_name_association'].dropna()
        if len(valid) > 0:
            mean = valid.mean()
            std = valid.std()
            weat = dd['weat_effect_size'].iloc[0]
            n = len(valid)
            if abs(mean) < 0.005:
                interp = "Neutral"
            elif mean > 0:
                interp = f"EA-leaning ({'strong' if abs(mean) > 0.02 else 'weak'})"
            else:
                interp = f"AA-leaning ({'strong' if abs(mean) > 0.02 else 'weak'})"
            weat_str = f"{weat:.3f}" if weat is not None else "N/A"
            print(f"  {decade}s    {mean:+.5f}   {std:.5f}  {weat_str:>8}  {n:>5}  {interp}")
        else:
            print(f"  {decade}s    {'N/A':>10}   {'N/A':>7}  {'N/A':>8}  {'0':>5}")

    print(f"{'='*80}")


def main():
    print("Loading results...")
    df = load_data()
    print(f"Loaded {len(df)} song results across {df['decade'].nunique()} decades.\n")

    print("Generating visualizations...")
    plot_decade_trend(df)
    plot_per_song_heatmap(df)
    plot_weat_effect_by_decade(df)
    plot_distribution_by_decade(df)
    plot_vocab_coverage(df)

    print_summary_table(df)

    print("\nAll plots saved! Files:")
    print("  • plot_decade_trend.png — Average bias by decade")
    print("  • plot_per_song.png — Per-song breakdown")
    print("  • plot_weat_effect.png — WEAT effect sizes")
    print("  • plot_distribution.png — Score distributions")
    print("  • plot_vocab_coverage.png — Vocabulary coverage")


if __name__ == "__main__":
    main()
