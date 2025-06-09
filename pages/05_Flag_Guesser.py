import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client, Client
from utils.database import FlagGameDatabase

# Initialize database
db = FlagGameDatabase()

# Page configuration
st.set_page_config(page_title="🌍 Flag Guesser", page_icon="🌍", layout="wide")

# Country data with flag emojis
COUNTRIES_DATA = {
    # Easy countries
    "easy": {
        "🇺🇸": "United States", "🇬🇧": "United Kingdom", "🇫🇷": "France", 
        "🇩🇪": "Germany", "🇮🇹": "Italy", "🇪🇸": "Spain", "🇨🇦": "Canada",
        "🇦🇺": "Australia", "🇯🇵": "Japan", "🇨🇳": "China", "🇧🇷": "Brazil",
        "🇮🇳": "India", "🇷🇺": "Russia", "🇲🇽": "Mexico", "🇰🇷": "South Korea",
        "🇳🇱": "Netherlands", "🇸🇪": "Sweden", "🇳🇴": "Norway", "🇨🇭": "Switzerland",
        "🇦🇹": "Austria"
    },
    
    # Medium countries
    "medium": {
        "🇵🇱": "Poland", "🇺🇦": "Ukraine", "🇹🇷": "Turkey", "🇬🇷": "Greece",
        "🇵🇹": "Portugal", "🇧🇪": "Belgium", "🇩🇰": "Denmark", "🇫🇮": "Finland",
        "🇮🇪": "Ireland", "🇮🇸": "Iceland", "🇨🇿": "Czech Republic", "🇭🇺": "Hungary",
        "🇷🇴": "Romania", "🇧🇬": "Bulgaria", "🇭🇷": "Croatia", "🇸🇰": "Slovakia",
        "🇸🇮": "Slovenia", "🇪🇪": "Estonia", "🇱🇻": "Latvia", "🇱🇹": "Lithuania",
        "🇲🇹": "Malta", "🇨🇾": "Cyprus", "🇱🇺": "Luxembourg", "🇦🇩": "Andorra",
        "🇲🇨": "Monaco"
    },
    
    # Hard countries
    "hard": {
        "🇦🇫": "Afghanistan", "🇦🇱": "Albania", "🇩🇿": "Algeria", "🇦🇴": "Angola",
        "🇦🇷": "Argentina", "🇦🇲": "Armenia", "🇦🇿": "Azerbaijan", "🇧🇭": "Bahrain",
        "🇧🇩": "Bangladesh", "🇧🇾": "Belarus", "🇧🇿": "Belize", "🇧🇯": "Benin",
        "🇧🇹": "Bhutan", "🇧🇴": "Bolivia", "🇧🇦": "Bosnia and Herzegovina", "🇧🇼": "Botswana",
        "🇧🇳": "Brunei", "🇧🇫": "Burkina Faso", "🇧🇮": "Burundi", "🇰🇭": "Cambodia",
        "🇨🇲": "Cameroon", "🇨🇻": "Cape Verde", "🇨🇫": "Central African Republic", "🇹🇩": "Chad",
        "🇨🇱": "Chile", "🇨🇴": "Colombia", "🇰🇲": "Comoros", "🇨🇬": "Congo"
    }
}

# Initialize session state
def init_session_state():
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'current_flag' not in st.session_state:
        st.session_state.current_flag = None
    if 'current_country' not in st.session_state:
        st.session_state.current_country = None
    if 'options' not in st.session_state:
        st.session_state.options = []
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'question_count' not in st.session_state:
        st.session_state.question_count = 0
    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    if 'difficulty' not in st.session_state:
        st.session_state.difficulty = 'easy'
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 10
    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False
    if 'countries_pool' not in st.session_state:
        st.session_state.countries_pool = {}

init_session_state()

def start_new_game(difficulty, num_questions):
    st.session_state.game_active = True
    st.session_state.game_finished = False
    st.session_state.score = 0
    st.session_state.question_count = 0
    st.session_state.correct_answers = 0
    st.session_state.difficulty = difficulty
    st.session_state.total_questions = num_questions
    st.session_state.start_time = time.time()
    st.session_state.countries_pool = COUNTRIES_DATA[difficulty].copy()
    generate_question()

def generate_question():
    if st.session_state.question_count >= st.session_state.total_questions:
        end_game()
        return
    
    if not st.session_state.countries_pool:
        # If we run out of countries, refill the pool
        st.session_state.countries_pool = COUNTRIES_DATA[st.session_state.difficulty].copy()
    
    # Select random flag and country
    flag, country = random.choice(list(st.session_state.countries_pool.items()))
    st.session_state.current_flag = flag
    st.session_state.current_country = country
    
    # Remove from pool to avoid duplicates
    del st.session_state.countries_pool[flag]
    
    # Generate wrong options
    all_countries = list(COUNTRIES_DATA[st.session_state.difficulty].values())
    wrong_options = random.sample([c for c in all_countries if c != country], 3)
    
    # Create options list and shuffle
    options = [country] + wrong_options
    random.shuffle(options)
    st.session_state.options = options
    
    st.session_state.question_count += 1

def check_answer(selected_answer):
    if selected_answer == st.session_state.current_country:
        st.session_state.correct_answers += 1
        points = {"easy": 10, "medium": 20, "hard": 30}[st.session_state.difficulty]
        st.session_state.score += points
        st.success(f"✅ Correct! +{points} points")
    else:
        st.error(f"❌ Wrong! The correct answer was {st.session_state.current_country}")
    
    time.sleep(1)
    generate_question()

def end_game():
    st.session_state.game_active = False
    st.session_state.game_finished = True
    
    time_taken = int(time.time() - st.session_state.start_time)
    accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
    
    # Bonus points for speed and accuracy
    time_bonus = max(0, 300 - time_taken) // 10  # Bonus for completing quickly
    accuracy_bonus = int(accuracy * 2)  # 2 points per percent accuracy
    
    final_score = st.session_state.score + time_bonus + accuracy_bonus
    st.session_state.final_score = final_score

def save_game_score(player_name, score, correct_answers, total_questions, accuracy, time_taken, difficulty):
    try:
        if db and db.supabase:
            result = db.supabase.table('flag_leaderboard').insert({
                'player_name': player_name,
                'score': score,
                'correct_answers': correct_answers,
                'total_questions': total_questions,
                'accuracy': accuracy,
                'time_taken': time_taken,
                'difficulty': difficulty
                # game_date will be set automatically by DEFAULT NOW()
            }).execute()
            
            # Check if the insert was successful
            if result.data:
                return True
            else:
                st.error(f"Failed to save score: {result}")
                return False
                
    except Exception as e:
        st.error(f"Error saving score: {str(e)}")
        return False
    
def get_leaderboard(limit=10, difficulty_filter=None):
    try:
        if db and db.supabase:
            query = db.supabase.table('flag_leaderboard')\
                .select('player_name, score, accuracy, difficulty, game_date')\
                .order('score', desc=True)\
                .limit(limit)
            
            if difficulty_filter:
                query = query.eq('difficulty', difficulty_filter)
                
            response = query.execute()
            return response.data
    except Exception as e:
        st.error(f"Error fetching leaderboard: {str(e)}")
    return []

def get_leaderboard_stats():
    """Get comprehensive statistics for the statistics tab"""
    try:
        if db and db.supabase:
            response = db.supabase.table('flag_leaderboard')\
                .select('*')\
                .execute()
            return response.data
    except Exception as e:
        st.error(f"Error fetching statistics: {str(e)}")
    return []

# Main UI
st.title("🌍 Flag Guesser Game")

# Check if database is available
if not db or not db.supabase:
    st.error("⚠️ Database connection unavailable. Leaderboard features will be disabled.")
    st.info("💡 The game will still work, but scores won't be saved.")

# Sidebar for navigation
with st.sidebar:
    st.header("📊 Game Stats")
    if st.session_state.game_active:
        st.metric("Current Score", st.session_state.score)
        st.metric("Question", f"{st.session_state.question_count}/{st.session_state.total_questions}")
        st.metric("Correct Answers", st.session_state.correct_answers)
        if st.session_state.question_count > 0:
            current_accuracy = (st.session_state.correct_answers / st.session_state.question_count) * 100
            st.metric("Accuracy", f"{current_accuracy:.1f}%")
    
    st.header("🎮 Quick Actions")
    if st.button("🔄 Refresh Leaderboard"):
        st.rerun()

# Main content area
if db and db.supabase:
    tab1, tab2, tab3 = st.tabs(["🎯 Play Game", "🏆 Leaderboard", "📈 Statistics"])
else:
    tab1, = st.tabs(["🎯 Play Game"])

with tab1:
    if not st.session_state.game_active and not st.session_state.game_finished:
        st.header("🚀 Start New Game")
        
        col1, col2 = st.columns(2)
        
        with col1:
            difficulty = st.selectbox(
                "Choose Difficulty:",
                ["easy", "medium", "hard"],
                format_func=lambda x: f"{x.title()} ({len(COUNTRIES_DATA[x])} countries)"
            )
        
        with col2:
            num_questions = st.selectbox("Number of Questions:", [5, 10, 15, 20])
        
        st.info(f"**{difficulty.title()} Mode**: {len(COUNTRIES_DATA[difficulty])} countries available")
        
        if st.button("🎮 Start Game", type="primary"):
            start_new_game(difficulty, num_questions)
            st.rerun()
    
    elif st.session_state.game_active:
        # Game interface
        st.header(f"Question {st.session_state.question_count}/{st.session_state.total_questions}")
        
        # Progress bar
        progress = st.session_state.question_count / st.session_state.total_questions
        st.progress(progress)
        
        # Display flag
        st.markdown(f"<div style='text-align: center; font-size: 120px;'>{st.session_state.current_flag}</div>", 
                   unsafe_allow_html=True)
        
        st.markdown("### Which country does this flag represent?")
        
        # Answer options
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(st.session_state.options[0], key="opt1", use_container_width=True):
                check_answer(st.session_state.options[0])
                st.rerun()
            
            if st.button(st.session_state.options[2], key="opt3", use_container_width=True):
                check_answer(st.session_state.options[2])
                st.rerun()
        
        with col2:
            if st.button(st.session_state.options[1], key="opt2", use_container_width=True):
                check_answer(st.session_state.options[1])
                st.rerun()
            
            if st.button(st.session_state.options[3], key="opt4", use_container_width=True):
                check_answer(st.session_state.options[3])
                st.rerun()
        
        # Game controls
        if st.button("🛑 End Game Early"):
            end_game()
            st.rerun()
    
    elif st.session_state.game_finished:
        # Game over screen
        st.header("🎉 Game Complete!")
        
        time_taken = int(time.time() - st.session_state.start_time)
        accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Final Score", st.session_state.final_score)
        
        with col2:
            st.metric("Correct Answers", f"{st.session_state.correct_answers}/{st.session_state.total_questions}")
        
        with col3:
            st.metric("Accuracy", f"{accuracy:.1f}%")
        
        with col4:
            st.metric("Time Taken", f"{time_taken}s")
        
        # Performance message
        if accuracy >= 90:
            st.success("🌟 Excellent! You're a geography expert!")
        elif accuracy >= 70:
            st.info("👍 Good job! You know your flags well!")
        elif accuracy >= 50:
            st.warning("📚 Not bad! Keep practicing to improve!")
        else:
            st.error("🤔 Room for improvement! Try studying more flags!")
        
        # Save score
        if db and db.supabase:
            st.subheader("💾 Save Your Score")
            player_name = st.text_input("Enter your name:", max_chars=20)
            
            # Replace the save score section in the game over screen:
            if player_name and st.button("Save to Leaderboard", type="primary"):
                time_taken = int(time.time() - st.session_state.start_time)
                accuracy = (st.session_state.correct_answers / st.session_state.total_questions) * 100
                
                success = save_game_score(
                    player_name=player_name,
                    score=st.session_state.final_score,
                    correct_answers=st.session_state.correct_answers,
                    total_questions=st.session_state.total_questions,
                    accuracy=accuracy,
                    time_taken=time_taken,
                    difficulty=st.session_state.difficulty
                )
                
                if success:
                    st.success("🎊 Score saved successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Failed to save score. Please try again.")
        else:
            st.warning("💾 Score saving is currently unavailable due to database connection issues.")
        
        if st.button("🔄 Play Again"):
            st.session_state.game_finished = False
            st.rerun()

# Only show leaderboard and statistics tabs if database is available
if db and db.supabase:
    # Replace the leaderboard tab content:
    with tab2:
        st.header("🏆 Leaderboard")
        
        # Leaderboard controls
        col1, col2 = st.columns(2)
        
        with col1:
            show_difficulty = st.selectbox("Filter by Difficulty:", ["All", "easy", "medium", "hard"])
        
        with col2:
            limit = st.selectbox("Show top:", [10, 20, 50], index=0)
        
        # Get leaderboard data
        difficulty_filter = show_difficulty if show_difficulty != "All" else None
        
        with st.spinner("Loading leaderboard..."):
            leaderboard = get_leaderboard(limit, difficulty_filter)
        
        if not leaderboard:
            st.info("🎮 No scores recorded yet! Be the first to play and make it to the leaderboard!")
        else:
            # Convert to DataFrame for better display
            df = pd.DataFrame(leaderboard)
            
            # Format the display
            display_df = df[['player_name', 'score', 'accuracy', 'difficulty']].copy()
            display_df['accuracy'] = display_df['accuracy'].round(1).astype(str) + '%'
            display_df['difficulty'] = display_df['difficulty'].str.title()
            
            # Display leaderboard
            st.dataframe(
                display_df,
                column_config={
                    "player_name": st.column_config.TextColumn("Player", width="medium"),
                    "score": st.column_config.NumberColumn("Score", width="medium"),
                    "accuracy": st.column_config.TextColumn("Accuracy", width="medium"),
                    "difficulty": st.column_config.TextColumn("Difficulty", width="medium")
                },
                use_container_width=True,
                hide_index=True
            )

    # Replace the statistics tab content:
with tab3:
    st.header("📈 Game Statistics")
    
    with st.spinner("Loading statistics..."):
        stats_data = get_leaderboard_stats()
    
    if not stats_data:
        st.info("📊 No data available yet. Play some games to see statistics!")
    else:
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(stats_data)
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Games", len(df))
        
        with col2:
            st.metric("Average Score", f"{df['score'].mean():.0f}")
        
        with col3:
            st.metric("Highest Score", f"{df['score'].max()}")
        
        with col4:
            st.metric("Average Accuracy", f"{df['accuracy'].mean():.1f}%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Score distribution
            fig_hist = px.histogram(
                df, 
                x='score', 
                nbins=20,
                title="Score Distribution",
                color_discrete_sequence=['#1f77b4']
            )
            fig_hist.update_layout(showlegend=False)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Difficulty distribution
            difficulty_counts = df['difficulty'].value_counts()
            fig_pie = px.pie(
                values=difficulty_counts.values, 
                names=difficulty_counts.index,
                title="Games by Difficulty"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Performance by difficulty
        st.subheader("📊 Performance by Difficulty")
        
        difficulty_stats = df.groupby('difficulty').agg({
            'score': ['mean', 'max'],
            'accuracy': 'mean',
            'time_taken': 'mean'
        }).round(1)
        
        difficulty_stats.columns = ['Avg Score', 'Max Score', 'Avg Accuracy (%)', 'Avg Time (s)']
        st.dataframe(difficulty_stats, use_container_width=True)
        
  # Recent activity
        st.subheader("🕒 Recent Activity")
        df['game_date'] = pd.to_datetime(df['game_date'], errors='coerce')
        recent_games = df.nlargest(5, 'game_date')

        
        for _, game in recent_games.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                
                with col1:
                    st.write(f"**{game['player_name']}**")
                
                with col2:
                    st.write(f"{game['score']} pts")
                
                with col3:
                    st.write(f"{game['accuracy']:.1f}%")
                
                with col4:
                    st.write(f"{game['difficulty'].title()} • {str(game['game_date'])[:16]}")
                
                st.divider()