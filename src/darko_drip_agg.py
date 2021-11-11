
current_darko_df = pd.read_csv('https://docs.google.com/spreadsheets/d/1mhwOLqPu2F9026EQiVxFPIN1t9RGafGpl-dokaIsm9c/gviz/tq?tqx=out:csv&gid=284274620')
current_drip_df = pd.io.json.read_json("https://dataviz.theanalyst.com/nba-stats-hub/drip.json")

current_darko_df[['nba_id', 'available', 'tm_id', 'current_min', 'fs_min', 'minutes', 'pace', 'pts_100', 'orb_100', 'drb_100', 'ast_100', 'blk_100', 'stl_100', 'tov_100', 'fta_100', 'fg3a_100', 'fg_pct', 'fg3_pct', 'ft_pct']]
current_drip_df[['player', 'player_id', 'PTS', 'AST', 'STL', 'ORB', 'DRB', 'BLK', 'TOV', 'FT%', '3PT%', '2PT%', '3PAr', 'FTr']]
current_drip_df.rename(columns={'FT%':'ft_pct', '3PT%':'fg3_pct', '2PT%': 'fg2_pct'})

# merge
# need to get FGA for DRIP
def get_drip_fga(drip_df):
	drip_df['fga'] = drip_df.PTS / (2*drip_df.fg2_pct*(1-drip_df['3PAr']) + 3*drip_df.fg3_pct*drip_df['3PAr'] + drip_df.ft_pct*drip_df.FTr)
	return drip_df

def get_drip_fg_pct(drip_df):
	drip_df['fg_pct'] = drip_df.fg2_pct*(1-drip_df['3PAr']) + drip_df.fg3_pct*drip_df['3PAr']
	return drip_df

# get DRIP 3pm from fga, 3PAr, and 3p_pct
def get_drip_fg3m(drip_df):
	drip_df['fg3m'] = drip_df.fga*drip_df['3PAr']*drip_df.fg3_pct

# combine through concat and collapse? would have to line up the columns correctly
# can't do straight average of FG% and FT% b/c of differences in number of attempts
# will have to use DARKO pace and minutes for converting DRIP to per game values

simple_scoring_values = {
	'points': 1,
	'rebounds': 1,
	'assists': 1,
	'steals': 1,
	'blocks': 1,
	'turnovers': -1,
	'fga': 0,
	'fgm': 0,
	'fta': 0,
	'ftm': 0
}

trad_scoring_values = {
	'points': 1,
	'rebounds': 1,
	'assists': 2,
	'steals': 4,
	'blocks': 4,
	'turnovers': -2,
	'fga': -1,
	'fgm': 2,
	'fta': -1,
	'ftm': 1
}

def get_drip_fantast_pts(is_simple_scoring=True):
	scoring_dict = simple_scoring_values if is_simple_scoring else trad_scoring_values

def get_darko_fantasy_pts(scoring_type='simple'):
	scoring_dict = simple_scoring_values if is_simple_scoring else trad_scoring_values