import streamlit as st
import pandas as pd
import pickle

# --- 1. SETTINGS & ASSETS ---
st.set_page_config(page_title="IPL Pro Predictor", layout="wide")

# Load Brain & History
model = pickle.load(open('models/ipl_model.pkl', 'rb'))
scaler = pickle.load(open('models/scaler.pkl', 'rb'))
columns = pickle.load(open('models/columns.pkl', 'rb'))
h2h_stats = pickle.load(open('models/h2h_stats.pkl', 'rb'))

# --- 2. CUSTOM IPL STYLING (The "Amazing" Factor) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { background: linear-gradient(160deg, #0e1117 0%, #1c2d5e 100%); }
    h1 { color: #fbba00 !important; font-family: 'Arial Black'; text-shadow: 2px 2px #000; }
    .stButton>button { 
        background-color: #fbba00; color: #1c2d5e; font-weight: bold; 
        width: 100%; border-radius: 20px; border: none; height: 3em;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #ffffff; transform: scale(1.02); }
    .h2h-card { 
        background: rgba(255, 255, 255, 0.05); padding: 20px; 
        border-radius: 15px; border-left: 5px solid #fbba00;
    }
    .metric-box { text-align: center; padding: 10px; border-radius: 10px; background: rgba(0,0,0,0.3); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR INPUTS ---
st.title("🏏 IPL MATCH PRO-PREDICTOR")
st.markdown("### *Simulating Data-Driven Victory*")

with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    
    with c1:
        st.subheader("Team 1 (Batting)")
        batting_team = st.selectbox('Select Team', sorted(['Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders', 'Royal Challengers Bengaluru', 'Rajasthan Royals', 'Delhi Capitals', 'Sunrisers Hyderabad', 'Punjab Kings', 'Gujarat Titans', 'Lucknow Super Giants']), key='t1')
        city = st.selectbox('Host City', sorted(['Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Delhi', 'Hyderabad', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh']))

    with c2:
        st.markdown("<br><br><h1 style='text-align: center;'>VS</h1>", unsafe_allow_html=True)

    with c3:
        st.subheader("Team 2 (Chasing)")
        bowling_team = st.selectbox('Select Team', sorted(['Mumbai Indians', 'Chennai Super Kings', 'Kolkata Knight Riders', 'Royal Challengers Bengaluru', 'Rajasthan Royals', 'Delhi Capitals', 'Sunrisers Hyderabad', 'Punjab Kings', 'Gujarat Titans', 'Lucknow Super Giants']), key='t2')
        toss_dec = st.radio("Toss Winner Decided to:", ('bat', 'field'), horizontal=True)

st.divider()

# --- 4. THE H2H RIVALRY DASHBOARD ---
st.markdown("### 📊 Historical Rivalry (Head-to-Head)")
# Logic to filter H2H wins
pair = sorted([batting_team, bowling_team])
match_history = h2h_stats[((h2h_stats['team1'] == pair[0]) & (h2h_stats['team2'] == pair[1])) | 
                          ((h2h_stats['team1'] == pair[1]) & (h2h_stats['team2'] == pair[0]))]

t1_wins = match_history[match_history['winner'] == batting_team]['count'].sum()
t2_wins = match_history[match_history['winner'] == bowling_team]['count'].sum()

h1, h2, h3 = st.columns(3)
with h1: st.markdown(f"<div class='metric-box'><b>{batting_team} Wins</b><br><h2>{t1_wins}</h2></div>", unsafe_allow_html=True)
with h2: st.markdown(f"<div class='metric-box'><b>Total Encounters</b><br><h2>{t1_wins + t2_wins}</h2></div>", unsafe_allow_html=True)
with h3: st.markdown(f"<div class='metric-box'><b>{bowling_team} Wins</b><br><h2>{t2_wins}</h2></div>", unsafe_allow_html=True)

st.divider()

# --- 5. GAME STATE ---
col_s1, col_s2 = st.columns(2)
with col_s1:
    target = st.number_input('Target Score set by Team 1', 0, 300, 185)
with col_s2:
    wickets = st.select_slider('Wickets Lost by Team 1', options=list(range(11)), value=3)

# --- 6. PREDICTION ---
if st.button('🎯 CALCULATE WIN PROBABILITY'):
    # Prepare data
    input_df = pd.DataFrame(columns=model_columns).fillna(0)
    input_df.loc[0] = 0
    
    if f'city_{city}' in input_df.columns: input_df[f'city_{city}'] = 1
    if f'team1_{batting_team}' in input_df.columns: input_df[f'team1_{batting_team}'] = 1
    if f'team2_{bowling_team}' in input_df.columns: input_df[f'team2_{bowling_team}'] = 1
    
    input_df['target_score'] = target
    input_df['wickets_lost'] = wickets
    input_df['h2h_ratio'] = t1_wins / (t1_wins + t2_wins) if (t1_wins + t2_wins) > 0 else 0.5
    input_df['team1_win_ratio'] = 0.5 # Simplified for UI
    input_df['team2_win_ratio'] = 0.5
    input_df['avg_venue_score'] = 175

    # Scale & Predict
    num_cols = ['target_score', 'avg_venue_score', 'team1_win_ratio', 'team2_win_ratio', 'h2h_ratio', 'wickets_lost']
    input_df[num_cols] = scaler.transform(input_df[num_cols])
    prob = model.predict_proba(input_df[model_columns])[0]

    # Display Results with Animation-style progress bar
    st.markdown(f"## {bowling_team} needs {target} to win!")
    
    r1, r2 = st.columns(2)
    r1.metric(label=f"🏆 {batting_team} Win Chance", value=f"{prob[1]*100:.1f}%")
    r2.metric(label=f"🏆 {bowling_team} Win Chance", value=f"{prob[0]*100:.1f}%")
    
    st.progress(int(prob[1] * 100))
    st.write("---")
    st.info("Analysis based on venue history, current target pressure, and historical head-to-head dominance.")
