import streamlit as st
import random
import time
from PIL import Image, ImageDraw
import io

st.set_page_config(page_title="The Lost Signal", page_icon="📡", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        transition: background-color 1s ease;
    }
    .stButton>button {
        width: 100%;
        background-color: #F4E4BC;
        color: black;
        font-weight: bold;
        border-radius: 12px;
        height: 55px;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 15px rgba(244, 228, 188, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(244, 228, 188, 0.5);
    }
    .clue-box {
        background: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #F4E4BC;
        font-size: 22px;
        color: #F4E4BC;
        text-shadow: 0 0 10px rgba(244, 228, 188, 0.5);
    }
    .signal-box {
        background-color: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
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

bg_colors = ["#000000", "#0e153a", "#220a2e", "#2e0b16", "#04291c"]
current_bg = bg_colors[(st.session_state.level - 1) % len(bg_colors)]

st.markdown(f"""
    <style>
    .stApp {{background-color: {current_bg}; color: white;}}
    </style>
    """, unsafe_allow_html=True)

lang = st.radio("", ["العربية", "English"], horizontal=True)
is_ar = lang == "العربية"

texts = {
    "title": "📡 لغز الإشارة المفقودة" if is_ar else "📡 The Lost Signal",
    "desc": "حرك أجهزة التتبع لالتقاط إشارة النجم" if is_ar else "Adjust trackers to intercept the star signal",
    "level": "المستوى" if is_ar else "Level",
    "stars": "النجوم" if is_ar else "Stars",
    "secret": "الشفرة السرية" if is_ar else "Secret Code",
    "time": "⏳ الوقت" if is_ar else "⏳ Time",
    "x_label": "↔️ تردد أفقي (X)" if is_ar else "↔️ Horizontal Freq (X)",
    "y_label": "↕️ تردد عمودي (Y)" if is_ar else "↕️ Vertical Freq (Y)",
    "scan_btn": "📡 مسح الإشارة (SCAN)" if is_ar else "📡 SCAN SIGNAL",
    "hint_btn": "💡 طلب مساعدة" if is_ar else "💡 REQUEST ASSIST",
    "sig_strong": "⚠️ إشارة قصوى! الهدف تحتك تماماً" if is_ar else "⚠️ MAX SIGNAL! Target Locked",
    "sig_med": "📡 إشارة متوسطة.. أنت قريب" if is_ar else "📡 Medium Signal.. Getting close",
    "sig_weak": "❌ لا توجد إشارة.. ابحث في مكان آخر" if is_ar else "❌ No Signal.. Search elsewhere",
    "win_msg": "✅ تم فك الشفرة: " if is_ar else "✅ Decoded: ",
    "fail_msg": "❌ الإشارة ضعيفة جداً للالتقاط!" if is_ar else "❌ Signal too weak to capture!",
    "hint_l": "⬅️ حرك المؤشر لليسار" if is_ar else "⬅️ Move Left",
    "hint_r": "➡️ حرك المؤشر لليمين" if is_ar else "➡️ Move Right",
    "hint_u": "⬆️ حرك المؤشر للأعلى" if is_ar else "⬆️ Move Up",
    "hint_d": "⬇️ حرك المؤشر للأسفل" if is_ar else "⬇️ Move Down",
    "game_over": "🔴 انقطع الاتصال! انتهى الوقت" if is_ar else "🔴 Connection Lost! Time up",
    "retry": "🔄 إعادة ضبط النظام" if is_ar else "🔄 System Reset",
    "final_title": "🎉 تمت المهمة بنجاح! 🎉" if is_ar else "🎉 Mission Accomplished! 🎉",
    "download": "📄 استلام وثيقة المهمة" if is_ar else "📄 Retrieve Mission Doc",
    "play_again": "🔄 مهمة جديدة" if is_ar else "🔄 New Mission"
}

sentence_ar = ["أخلاقياتك", "هي", "بوصلة", "الذكاء", "الاصطناعي"]
sentence_en = ["Ethics", "is", "the", "Compass", "of AI"]
current_sentence = sentence_ar if is_ar else sentence_en

def create_certificate():
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#0e1117')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width-20, height-20], outline="#F4E4BC", width=5)
    draw.text((width//2, 100), "CERTIFICATE OF ACHIEVEMENT", fill="#F4E4BC", anchor="mm", font_size=40)
    draw.text((width//2, 180), "ATHAR EXHIBITION 2026", fill="white", anchor="mm", font_size=30)
    draw.text((width//2, 300), "The player has successfully decoded", fill="#cccccc", anchor="mm", font_size=20)
    draw.text((width//2, 340), "THE LOST SIGNAL", fill="#cccccc", anchor="mm", font_size=25)
    draw.text((width//2, 450), "Ethics is the Compass of AI", fill="#F4E4BC", anchor="mm", font_size=25)
    return img

st.title(texts["title"])

if not st.session_state.game_over and not st.session_state.game_won:
    elapsed_time = time.time() - st.session_state.start_time
    time_left = 60 - elapsed_time
    
    if time_left > 0:
        st.progress(max(0.0, time_left / 60), text=f"{texts['time']}: {int(time_left)}")
    else:
        st.session_state.game_over = True
        st.rerun()

    c1, c2 = st.columns(2)
    with c1: st.metric(texts["level"], f"{st.session_state.level}/5")
    with c2: st.metric(texts["stars"], "⭐" * (st.session_state.level - 1))
    
    found_words = current_sentence[:st.session_state.level - 1]
    clue_display = " ... ".join(found_words) if found_words else "🔒🔒🔒"
    st.markdown(f'<div class="clue-box">{clue_display}</div>', unsafe_allow_html=True)
    
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
    
    st.markdown('<div class="signal-box">', unsafe_allow_html=True)
    if signal > 90: st.success(f"{texts['sig_strong']} ({int(signal)}%)")
    elif signal > 50: st.warning(f"{texts['sig_med']} ({int(signal)}%)")
    else: st.error(f"{texts['sig_weak']} ({int(signal)}%)")
    st.markdown('</div>', unsafe_allow_html=True)

    b1, b2 = st.columns([3, 1])
    with b1:
        if st.button(texts["scan_btn"]):
            if dist < 6:
                st.balloons()
                word_found = current_sentence[st.session_state.level - 1]
                if st.session_state.level == 5:
                    st.session_state.game_won = True
                    st.rerun()
                else:
                    st.toast(f"{texts['win_msg']} {word_found}")
                    time.sleep(1.5)
                    st.session_state.level += 1
                    st.session_state.target_x = random.randint(10, 90)
                    st.session_state.target_y = random.randint(10, 90)
                    st.session_state.start_time = time.time()
                    st.session_state.hint_used = False
                    st.rerun()
            else:
                st.error(texts["fail_msg"])
    
    with b2:
        if not st.session_state.hint_used:
            if st.button(texts["hint_btn"]):
                st.session_state.hint_used = True
                st.rerun()
        else:
            if abs(diff_x) > abs(diff_y): 
                h_msg = texts["hint_l"] if diff_x > 0 else texts["hint_r"]
            else:
                h_msg = texts["hint_u"] if diff_y > 0 else texts["hint_d"]
            st.info(h_msg)

elif st.session_state.game_won:
    st.markdown(f"""
    <div style="text-align: center; border: 2px solid #F4E4BC; padding: 30px; border-radius: 20px; background: rgba(0,0,0,0.6);">
        <h1 style="color: #F4E4BC; margin-bottom: 20px;">{texts['final_title']}</h1>
        <h3 style="color: white; font-style: italic;">"Ethics is the Compass of AI"</h3>
        <p style="color: #cccccc;">{texts['win_msg']} Completed</p>
    </div>
    """, unsafe_allow_html=True)
    
    cert = create_certificate()
    buf = io.BytesIO()
    cert.save(buf, format="PNG")
    st.download_button(label=texts["download"], data=buf.getvalue(), file_name="Athar_Mission_Doc.png", mime="image/png")
    
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
st.markdown("<div style='text-align: center; color: #555; font-size: 12px;'>Athar Exhibition © 2026</div>", unsafe_allow_html=True)
