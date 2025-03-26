import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from pybaseball import statcast_pitcher, playerid_lookup

# Tampa Bay Rays 2025 Pitchers
rays_pitchers = [
    ("Shane", "Baz"), ("Hunter", "Bigge"), ("Joe", "Boyle"), ("Taj", "Bradley"),
    ("Garrett", "Cleavinger"), ("Yoniel", "Curet"), ("Mason", "Englert"),
    ("Alex", "Faedo"), ("Pete", "Fairbanks"), ("Kevin", "Kelly"), ("Nate", "Lavender"),
    ("Zack", "Littell"), ("Shane", "McClanahan"), ("Mason", "Montgomery"),
    ("Ian", "Seymour"), ("Cole", "Sulser"), ("Edwin", "Uceta"), ("Jacob", "Waguespack"),
]

# Pull Statcast data
def get_pitch_data(first, last, start='2023-01-01', end='2025-03-25'):
    try:
        pid = playerid_lookup(last, first).iloc[0]['key_mlbam']
        return statcast_pitcher(start, end, pid)
    except:
        return pd.DataFrame()

# Collect metrics
results = []

for first, last in rays_pitchers:
    name = f"{first} {last}"
    print(f"Processing {name}...")
    data = get_pitch_data(first, last)

    if data.empty or 'release_pos_x' not in data.columns:
        results.append({'name': name, 'mlb_data': False})
        continue

    data['game_date'] = pd.to_datetime(data['game_date'])
    regular_data = data[data['game_date'].dt.month.isin([4,5,6,7,8,9,10])]

    if regular_data.empty:
        results.append({'name': name, 'mlb_data': False})
        continue

    pitches = len(regular_data)
    release_var = regular_data.groupby('pitch_type')[['release_pos_x', 'release_pos_z']].std().mean().mean()
    velo_means = regular_data.groupby('pitch_type')['release_speed'].mean()
    fb = velo_means.get('FF', 0)
    off = velo_means.drop('FF', errors='ignore').mean()
    velo_sep = fb - off if not pd.isna(off) else 0
    spin_range = regular_data.groupby('pitch_type')['spin_axis'].mean().agg(['max', 'min'])
    spin_diff = spin_range['max'] - spin_range['min'] if not spin_range.isnull().values.any() else 0

    results.append({
        'name': name,
        'release_var': release_var,
        'velo_sep': velo_sep,
        'spin_diff': spin_diff,
        'total_pitches': pitches,
        'mlb_data': True
    })

    time.sleep(1)

# Create DataFrame
df = pd.DataFrame(results)
df = df[df['mlb_data'] == True].dropna(subset=['release_var', 'velo_sep', 'spin_diff'])

# Normalize components
for col in ['release_var', 'velo_sep', 'spin_diff']:
    df[f'norm_{col}'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

# Compute Deception Score
df['deception_score'] = (
    (1 - df['norm_release_var']) * 0.4 +
    df['norm_velo_sep'] * 0.3 +
    (1 - df['norm_spin_diff']) * 0.3
)

# Plot saving function
def save_bar_plot(x, title, xlabel, filename):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=x, y='name', data=df.sort_values(x, ascending=True), palette='Blues_r')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Pitcher")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"✅ Saved: {filename}")

# Save all component plots
save_bar_plot('deception_score',
              "Pitcher Deception Index - Tampa Bay Rays (2025)\n(Regular Season MLB Data Only)",
              "Deception Score", "Rays Deception Score.png")

save_bar_plot('release_var',
              "Release Point Variance - Tampa Bay Rays (2025)",
              "Release Point Variance", "Rays Release Point Variance.png")

save_bar_plot('velo_sep',
              "Velocity Separation (mph) - Tampa Bay Rays (2025)",
              "Velocity Separation (mph)", "Rays Velo Sep.png")

save_bar_plot('spin_diff',
              "Spin Axis Difference (degrees) - Tampa Bay Rays (2025)",
              "Spin Axis Difference (degrees)", "Rays Spin Axis Diff.png")

# Output DataFrame with scores
df_scores = df[['name', 'deception_score', 'release_var', 'velo_sep', 'spin_diff']].sort_values('deception_score', ascending=False)
print("\n🎯 Pitcher Scores:")
print(df_scores.to_string(index=False))

# Save scores as CSV
df_scores.to_csv("rays_deception_scores_2025.csv", index=False)
print("\n📁 Saved: rays_deception_scores_2025.csv")
