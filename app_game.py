import streamlit as st
import random
import time
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="The Lost Signal", page_icon="🔭", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%; background-color: #F4E4BC; color: black; font-weight: bold; border-radius: 10px; height: 50px;
    }
    .clue-box {
        background: rgba(255, 255, 255, 0.1); padding: 15px; border-radius: 10px;
        text-align: center; margin: 10px 0; border: 1px solid #F4E4BC; font-size: 20px; color: #F4E4BC;
    }
    </style>
    """, unsafe_allow_html=True)

if 'level' not in st.session_state: st.session_state.level = 1
if 'target_x' not in st.session_state: st.session_state.target_x = random.randint(10, 90)
if 'target_y' not in st.session_state: st.session_state.target_y = random.randint(10, 90)
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'game_won' not in st.session_state: st.session_state.game_won = False
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'hint_used' not in st.session_state: st.session_state.hint_used = False

bg_colors = ["#000000", "#0a0f24", "#1a0b2e", "#2e0b16", "#0b2e26"]
current_bg = bg_colors[(st.session_state.level - 1) % len(bg_colors)]

st.markdown(f"""
    <style>
    .stApp {{background-color: {current_bg}; color: white; transition: background-color 1s ease;}}
    </style>
    """, unsafe_allow_html=True)

lang = st.radio("", ["العربية", "English"], horizontal=True)
is_ar = lang == "العربية"

texts = {
    "title": "🔭 لغز النجم الضائع" if is_ar else "🔭 The Lost Signal",
    "desc": "حرك التلسكوب للبحث عن الإشارة" if is_ar else "Adjust telescope to find the signal",
    "level": "المستوى" if is_ar else "Level",
    "stars": "النجوم" if is_ar else "Stars",
    "secret": "الجملة السرية" if is_ar else "Secret Sentence",
    "time": "⏳ الوقت المتبقي" if is_ar else "⏳ Time Left",
    "sec": "ثانية" if is_ar else "sec",
    "x_label": "↔️ أفقي (X)" if is_ar else "↔️ Horizontal (X)",
    "y_label": "↕️ عمودي (Y)" if is_ar else "↕️ Vertical (Y)",
    "scan_btn": "📸 مسح (SCAN)" if is_ar else "📸 SCAN",
    "hint_btn": "💡 تلميح" if is_ar else "💡 HINT",
    "sig_strong": "📡 إشارة قوية جداً! أنت فوق النجم" if is_ar else "📡 Strong Signal! Target locked",
    "sig_med": "📡 إشارة متوسطة.. اقتربت" if is_ar else "📡 Medium Signal.. Getting closer",
    "sig_weak": "📡 لا توجد إشارة.. غير الموقع" if is_ar else "📡 No Signal.. Keep searching",
    "win_msg": "✅ أحسنت! الكلمة هي" if is_ar else "✅ Great! Found word",
    "fail_msg": "❌ لا يوجد نجم هنا.. واصل البحث!" if is_ar else "❌ Nothing here.. Keep looking!",
    "hint_left": "⬅️ لليسار" if is_ar else "⬅️ Go Left",
    "hint_right": "➡️ لليمين" if is_ar else "➡️ Go Right",
    "hint_up": "⬆️ للأعلى" if is_ar else "⬆️ Go Up",
    "hint_down": "⬇️ للأسفل" if is_ar else "⬇️ Go Down",
    "game_over": "⏰ انتهى الوقت! فقدت الإشارة..." if is_ar else "⏰ Time's up! Signal lost...",
    "retry": "🔄 إعادة المحاولة" if is_ar else "🔄 Retry",
    "final_title": "🎉 مبروك! اكتمل اللغز 🎉" if is_ar else "🎉 Congratulations! Puzzle Solved 🎉",
    "download": "📄 تحميل الشهادة" if is_ar else "📄 Download Certificate",
    "play_again": "🔄 العب مجدداً" if is_ar else "🔄 Play Again"
}

sentence_ar = ["أخلاقياتك", "هي", "بوصلة", "الذكاء", "الاصطناعي"]
sentence_en = ["Ethics", "is", "the", "Compass", "of AI"]
current_sentence = sentence_ar if is_ar else sentence_en

def create_certificate():
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#0e1117')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width-20, height-20], outline="#F4E4BC", width=5)
    draw.text((width//2, 100), "CERTIFICATE OF COMPLETION", fill="#F4E4BC", anchor="mm", font_size=40)
    draw.text((width//2, 180), "ATHAR EXHIBITION 2026", fill="white", anchor="mm", font_size=30)
    draw.text((width//2, 300), "This certifies that the player has found", fill="#cccccc", anchor="mm", font_size=20)
    draw.text((width//2, 340), "ALL THE HIDDEN STARS", fill="#cccccc", anchor="mm", font_size=20)
    draw.text((width//2, 450), "Ethics is the Compass of AI", fill="#F4E4BC", anchor="mm", font_size=25)
    return img

st.title(texts["title"])

if not st.session_state.game_over and not st.session_state.game_won:
    elapsed_time = time.time() - st.session_state.start_time
    time_left = 60 - elapsed_time
    
    if time_left > 0:
        st.progress(max(0.0, time_left / 60), text=f"{texts['time']}: {int(time_left)} {texts['sec']}")
    else:
        st.session_state.game_over = True
        st.rerun()

    c1, c2 = st.columns(2)
    with c1: st.caption(f"{texts['level']}: {st.session_state.level} / 5")
    with c2: st.caption(f"{texts['stars']}: {'⭐' * (st.session_state.level - 1)}")
    
    found_words = current_sentence[:st.session_state.level - 1]
    clue_display = " ... ".join(found_words) if found_words else "؟؟؟"
    st.markdown(f'<div class="clue-box">🧩 {texts["secret"]}: {clue_display}</div>', unsafe_allow_html=True)

    st.write("---")
    st.write(texts["desc"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(texts["x_label"])
        user_x = st.slider("X", 0, 100, 50, label_visibility="collapsed")
    with col2:
        st.write(texts["y_label"])
        user_y = st.slider("Y", 0, 100, 50, label_visibility="collapsed")

    diff_x = user_x - st.session_state.target_x
    diff_y = user_y - st.session_state.target_y
    dist = (abs(diff_x) + abs(diff_y)) / 2
    
    signal = max(0, 100 - (dist * 2.5))
    if signal > 90: st.success(f"{texts['sig_strong']} ({int(signal)}%)")
    elif signal > 50: st.warning(f"{texts['sig_med']} ({int(signal)}%)")
    else: st.error(f"{texts['sig_weak']} ({int(signal)}%)")

    bc1, bc2 = st.columns([3, 1])
    with bc1:
        if st.button(texts["scan_btn"]):
            if dist < 6:
                st.balloons()
                word_found = current_sentence[st.session_state.level - 1]
                if st.session_state.level == 5:
                    st.session_state.game_won = True
                    st.rerun()
                else:
                    st.toast(f"{texts['win_msg']}: {word_found}")
                    time.sleep(1.5)
                    st.session_state.level += 1
                    st.session_state.target_x = random.randint(10, 90)
                    st.session_state.target_y = random.randint(10, 90)
                    st.session_state.start_time = time.time()
                    st.session_state.hint_used = False
                    st.rerun()
            else:
                st.error(texts["fail_msg"])

    with bc2:
        if not st.session_state.hint_used:
            if st.button(texts["hint_btn"]):
                st.session_state.hint_used = True
                st.rerun()
        else:
            if abs(diff_x) > abs(diff_y): 
                hint = texts["hint_left"] if diff_x > 0 else texts["hint_right"]
            else:
                hint = texts["hint_up"] if diff_y > 0 else texts["hint_down"]
            st.info(hint)

elif st.session_state.game_won:
    st.markdown(f"""
    <div style="text-align: center; border: 2px solid #F4E4BC; padding: 20px; border-radius: 15px; background: rgba(0,0,0,0.5);">
        <h1 style="color: #F4E4BC;">{texts['final_title']}</h1>
        <h3 style="color: white;">"Ethics is the Compass of AI"</h3>
    </div>
    """, unsafe_allow_html=True)
    
    cert = create_certificate()
    buf = io.BytesIO()
    cert.save(buf, format="PNG")
    st.download_button(label=texts["download"], data=buf.getvalue(), file_name="Athar_Certificate.png", mime="image/png")
    
    if st.button(texts["play_again"]):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()

elif st.session_state.game_over:
    st.error(texts["game_over"])
    if st.button(texts["retry"]):
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: grey; font-size: 12px;'>Created with ⭐️ by Eng. Alyaa</div>", unsafe_allow_html=True)
