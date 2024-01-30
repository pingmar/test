import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch, FontManager, Sblocal, Pitch
import streamlit as st

def make_graph(ids, ff, padding=[None,None,None,None]):
  COLOR_U = 'blue'
  COLOR_N = 'orange'
  SIZE = 1
  pitch = VerticalPitch(goal_type='box', half=True, pad_left = padding[0], pad_right = padding[1], pad_top = padding[2], pad_bottom = padding[3])
  fig, axs = pitch.grid(figheight=8, endnote_height=0,
                        title_height=0.1, title_space=0.02,
                        axis=False,
                        grid_height=0.83)
  for ID, tp in zip(ids, ff): 
    if tp:
      df_freeze_frame = freeze[freeze.id == ID].copy()
      df_shot_event = events[events.id == ID].dropna(axis=1, how='all').copy()
      df_freeze_frame = df_freeze_frame.merge(df_lineup, how='left', on='player_id')
      team1 = df_shot_event.team_name.iloc[0]
      team2 = list(set(events.team_name.unique()) - {team1})[0]
      COLOR_1 = COLOR_U if team1 == 'Ukraine' else COLOR_N
      COLOR_2 = COLOR_U if team2 == 'Ukraine' else COLOR_N
      df_team1 = df_freeze_frame[df_freeze_frame.teammate == True]
      df_team2 = df_freeze_frame[df_freeze_frame.teammate == False]
      pitch.goal_angle(df_shot_event.x, df_shot_event.y, ax=axs['pitch'], alpha=0.2, zorder=1.1,
                  color='#cb5a4c', goal='right')
      pitch.scatter(df_team1.x, df_team1.y, s=600, c=COLOR_1, label='Attacker', ax=axs['pitch'])
      pitch.scatter(df_team2.x, df_team2.y, s=600, c=COLOR_2, label='Defender', ax=axs['pitch'])
      pitch.scatter(df_shot_event.x, df_shot_event.y, c=COLOR_1, marker='football',
                      s=600, ax=axs['pitch'], label='Shooter', zorder=1.2)
      pitch.lines(df_shot_event.x, df_shot_event.y,
                    df_shot_event.end_x, df_shot_event.end_y, comet=True,
                    label='shot', color='#cb5a4c', ax=axs['pitch'])
      for i, label in enumerate(df_freeze_frame.jersey_number):
        pitch.annotate(label, (df_freeze_frame.x[i], df_freeze_frame.y[i]),
                   va='center', ha='center', color='white', fontsize=15, ax=axs['pitch'])
    else:
      df_shot_event = events[events.id == ID].dropna(axis=1, how='all').copy()
      team1 = df_shot_event.team_name.iloc[0]
      team2 = list(set(events.team_name.unique()) - {team1})[0]
      COLOR_1 = COLOR_U if team1 == 'Ukraine' else COLOR_N
      COLOR_2 = COLOR_U if team2 == 'Ukraine' else COLOR_N
      pitch.scatter(df_shot_event.x, df_shot_event.y, c = COLOR_1, marker='football',
                      s=600, ax=axs['pitch'], label='Shooter', zorder=1.2)
      pitch.scatter(df_shot_event.end_x, df_shot_event.end_y, s=600, c=COLOR_1, label='Reciver', ax=axs['pitch'])
      pitch.lines(df_shot_event.x, df_shot_event.y,
                    df_shot_event.end_x, df_shot_event.end_y, comet=True,
                    label='shot', color='#cb5a4c', ax=axs['pitch'])
  axs['title'].text(0.5, 0.5, f'ABC',
                    va='center', ha='center', color='black',
                    fontsize=25)
  st.pyplot(fig)

COLOR_U = 'blue'
COLOR_N = 'orange'
SIZE = 1
competition_id=55
season_id=43
match_id=3788746
parser = Sblocal()
PATH_EVENT = f'app/data/json/events/3788746.json'
PATH_LINEUP = f'app/data/json/lineups/3788746.json'
events, related, freeze, tactics = parser.event(PATH_EVENT)
lineup = parser.lineup(PATH_LINEUP)
df_lineup = lineup[['player_id', 'jersey_number', 'team_name']].copy()
