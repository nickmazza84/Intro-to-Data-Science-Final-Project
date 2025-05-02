def evaluate_spread(row):
    home = row['team_home']
    away = row['team_away']
    favorite = row['Team']
    spread = row['spread_favorite']
    
    point_diff = row['score_home'] - row['score_away']
    
    # If home team is favorite, spread is as-is; else invert
    if favorite == home:
        adjusted_spread = spread
    else:
        adjusted_spread = -spread

    # Determine if favorite covered
    covered = point_diff > adjusted_spread
    push = point_diff == adjusted_spread

    result = {
        'home_team': home,
        'home_season': row['Season'],
        'home_cover': None,
        'away_team': away,
        'away_season': row['Season'],
        'away_cover': None}

    if push:
        result['home_cover'] = 'push'
        result['away_cover'] = 'push'
    elif favorite == home:
        result['home_cover'] = 'cover' if covered else 'no_cover'
        result['away_cover'] = 'no_cover' if covered else 'cover'
    else:
        result['home_cover'] = 'no_cover' if covered else 'cover'
        result['away_cover'] = 'cover' if covered else 'no_cover'

    return pd.Series(result)

# Apply the function to get cover results
spread_results = df_2005.apply(evaluate_spread, axis=1)

# Combine and format for aggregation
home_df = spread_results[['home_team', 'home_season', 'home_cover']].rename(
    columns={'home_team': 'Team', 'home_season': 'Season', 'home_cover': 'Result'}
)
away_df = spread_results[['away_team', 'away_season', 'away_cover']].rename(
    columns={'away_team': 'Team', 'away_season': 'Season', 'away_cover': 'Result'}
)

combined = pd.concat([home_df, away_df])

# Count number of covers, no_covers, and pushes per team per season
spread_summary = combined.groupby(['Team', 'Season', 'Result']).size().unstack(fill_value=0).reset_index()

spread_summary.columns.name = None  # Clean up the column names
spread_summary.to_csv('spreads.csv', index=False)