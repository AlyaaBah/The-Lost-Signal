import streamlit as st
import random
import time
from PIL import Image, ImageDraw
import io
import plotly.graph_objects as go
import numpy as np
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🌌", layout="wide")

# --- 2. تنسيق CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background-color: #000000;
        color: white;
    }
    /* تنسيق حاوية اللوقو ليكون في المنتصف */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }
    .logo-img {
        width: 150px; /* تحكمي في حجم اللوقو من هنا */
        border-radius: 50%; /* يجعله دائرياً إذا كانت الصورة مربعة */
        box-shadow: 0 0 20px rgba(88, 103, 221, 0.6); /* توهج أزرق */
    }
    /* تنسيق الأزرار */
    .stButton>button {
        width: 100%;
        background-color: #5867dd; /* لون أزرق فضائي */
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 50px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3f4cbea1;
    }
    /* صندوق الجملة السرية */
    .clue-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        border: 1px solid #5867dd;
        font-size: 18px;
        color: #F4E4BC;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة الحالة (Session State) ---
if 'level' not in st.session_state: st.session_state.level = 1
if 'target_x' not in st.session_state: st.session_state.target_x = random.randint(10, 90)
if 'target_y' not in st.session_state: st.session_state.target_y = random.randint(10, 90)
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'game_won' not in st.session_state: st.session_state.game_won = False
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()
if 'hint_used' not in st.session_state: st.session_state.hint_used = False
# توليد نجوم الخلفية مرة واحدة
if 'bg_stars_x' not in st.session_state:
    st.session_state.bg_stars_x = np.random.randint(0, 100, 250)
    st.session_state.bg_stars_y = np.random.randint(0, 100, 250)

# --- 4. إعدادات اللغة ---
lang = st.radio("", ["العربية", "English"], horizontal=True)
is_ar = lang == "العربية"

texts = {
    "title": "🌌 لغز الإشارة المفقودة" if is_ar else "🌌 The Lost Signal",
    "desc": "استخدم أدوات التحكم لتحريك السكوب ⭕ على الخريطة والعثور على النجم المخفي." if is_ar else "Use controls to move the scope ⭕ on the map and find the hidden star.",
    "level": "المستوى" if is_ar else "Level",
    "secret": "الشفرة" if is_ar else "Code",
    "time": "⏳" if is_ar else "⏳",
    "x_label": "↔️ تحريك أفقي (X)" if is_ar else "↔️ Horizontal (X)",
    "y_label": "↕️ تحريك عمودي (Y)" if is_ar else "↕️ Vertical (Y)",
    "scan_btn": "📸 مسح المنطقة (SCAN)" if is_ar else "📸 SCAN AREA",
    "hint_btn": "💡 تلميح" if is_ar else "💡 HINT",
    "sig_strong": "إشارة قوية! الهدف في الموقع" if is_ar else "Strong Signal! Target locked",
    "sig_weak": "لا توجد إشارة في هذا الموقع" if is_ar else "No signal in this area",
    "win_msg": "✅ تم العثور على النجم!" if is_ar else "✅ Star Found!",
    "fail_msg": "❌ لا يوجد شيء هنا.." if is_ar else "❌ Nothing here..",
    "hint_l": "⬅️ الهدف لليسار" if is_ar else "⬅️ Target is Left",
    "hint_r": "➡️ الهدف لليمين" if is_ar else "➡️ Target is Right",
    "hint_u": "⬆️ الهدف للأعلى" if is_ar else "⬆️ Target is Up",
    "hint_d": "⬇️ الهدف للأسفل" if is_ar else "⬇️ Target is Down",
    "final_title": "🎉 اكتملت المهمة!" if is_ar else "🎉 Mission Complete!",
    "download": "📄 تحميل الشهادة" if is_ar else "📄 Download Certificate",
    "play_again": "🔄 العب مجدداً" if is_ar else "🔄 Play Again"
}

sentence_ar = ["أخلاقياتك", "هي", "بوصلة", "الذكاء", "الاصطناعي"]
sentence_en = ["Ethics", "is", "the", "Compass", "of AI"]
current_sentence = sentence_ar if is_ar else sentence_en

# --- 5. دالة رسم الخريطة ---
def draw_map(user_x, user_y, signal_strength):
    fig = go.Figure()
    # رسم نجوم الخلفية
    fig.add_trace(go.Scatter(
        x=st.session_state.bg_stars_x, y=st.session_state.bg_stars_y,
        mode='markers', marker=dict(color='white', size=2, opacity=0.5), hoverinfo='none'
    ))
    
    # لون وحجم السكوب حسب الإشارة
    scope_color = "#00ff00" if signal_strength > 85 else "#ff0000"
    scope_size = 25 if signal_strength > 85 else 20
    
    # رسم السكوب (مكان اللاعب)
    fig.add_trace(go.Scatter(
        x=[user_x], y=[user_y],
        mode='markers',
        marker=dict(color=scope_color, size=scope_size, symbol='circle-open', line=dict(width=3)),
        hoverinfo='none'
    ))

    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(range=[0, 100], showgrid=False, zeroline=False, visible=False, fixedrange=True),
        yaxis=dict(range=[0, 100], showgrid=False, zeroline=False, visible=False, fixedrange=True),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='black', plot_bgcolor='black',
        height=500, dragmode=False
    )
    return fig

# --- 6. دالة الشهادة ---
def create_certificate():
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#0a0a2a')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width-20, height-20], outline="#5867dd", width=5)
    draw.text((width//2, 100), "CERTIFICATE OF COMPLETION", fill="#5867dd", anchor="mm", font_size=40)
    draw.text((width//2, 180), "ATHAR EXHIBITION 2026", fill="white", anchor="mm", font_size=30)
    draw.text((width//2, 300), "Player successfully located all hidden stars in", fill="#cccccc", anchor="mm", font_size=20)
    draw.text((width//2, 350), "THE LOST SIGNAL MISSION", fill="#cccccc", anchor="mm", font_size=25)
    draw.text((width//2, 450), "Ethics is the Compass of AI", fill="#5867dd", anchor="mm", font_size=25)
    return img

# --- 7. الواجهة الرئيسية ---

# عرض اللوقو في الأعلى
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
# ⚠️ تأكدي من رفع ملف الصورة باسم galaxy_logo.png
if os.path.exists("galaxy_logo.png"):
    st.image("galaxy_logo.png", width=150)
else:
    # شكل مؤقت في حال عدم وجود الصورة
    st.markdown('<div style="width:100px; height:100px; border-radius:50%; background:radial-gradient(circle, #5867dd, #000);"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.title(texts["title"])

if not st.session_state.game_over and not st.session_state.game_won:
    elapsed = time.time() - st.session_state.start_time
    left = 60 - elapsed
    if left <= 0:
        st.session_state.game_over = True
        st.rerun()

    # تقسيم الشاشة: تحكم (يسار) - خريطة (يمين)
    col_controls, col_map = st.columns([2, 3])

    with col_controls:
        c1, c2 = st.columns(2)
        with c1: st.metric(texts["level"], f"{st.session_state.level}/5")
        with c2: st.metric(texts["time"], f"{int(left)}")
        
        found_words = current_sentence[:st.session_state.level - 1]
        clue_display = " ... ".join(found_words) if found_words else "🔒..."
        st.markdown(f'<div class="clue-box">{clue_display}</div>', unsafe_allow_html=True)
        
        st.write(texts["desc"])
        
        user_x = st.slider(texts["x_label"], 0, 100, 50)
        user_y = st.slider(texts["y_label"], 0, 100, 50)
        
        diff_x = user_x - st.session_state.target_x
        diff_y = user_y - st.session_state.target_y
        dist = np.sqrt(diff_x**2 + diff_y**2)
        signal = max(0, 100 - (dist * 4))

        if signal > 85:
            st.success(texts["sig_strong"])
        
        b1, b2 = st.columns([2,1])
        with b1:
            if st.button(texts["scan_btn"]):
                if signal > 85:
                    st.balloons()
                    if st.session_state.level == 5:
                        st.session_state.game_won = True
                    else:
                        st.toast(texts["win_msg"])
                        st.session_state.level += 1
                        st.session_state.target_x = random.randint(10, 90)
                        st.session_state.target_y = random.randint(10, 90)
                        st.session_state.start_time = time.time()
                        st.session_state.hint_used = False
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error(texts["fail_msg"])
        with b2:
            if not st.session_state.hint_used:
                if st.button(texts["hint_btn"]):
                    st.session_state.hint_used = True
                    st.rerun()
            else:
                if abs(diff_x) > abs(diff_y): h = texts["hint_l"] if diff_x > 0 else texts["hint_r"]
                else: h = texts["hint_u"] if diff_y > 0 else texts["hint_d"]
                st.info(h)

    with col_map:
        # عرض الخريطة البصرية
        fig = draw_map(user_x, user_y, signal)
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.game_won:
    st.markdown(f"""
    <div style="text-align: center; border: 2px solid #5867dd; padding: 30px; border-radius: 20px; background: rgba(0,0,0,0.7);">
        <h1 style="color: #5867dd;">{texts['final_title']}</h1>
        <h3 style="color: white;">"Ethics is the Compass of AI"</h3>
    </div>""", unsafe_allow_html=True)
    buf = io.BytesIO()
    create_certificate().save(buf, format="PNG")
    st.download_button(texts["download"], data=buf.getvalue(), file_name="Athar_Certificate.png", mime="image/png")
    if st.button(texts["play_again"]):
        for k in st.session_state.keys(): del st.session_state[k]
        st.rerun()

elif st.session_state.game_over:
    st.error("Game Over.. Time's up!")
    if st.button("Retry"):
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align: center; color: #555; font-size: 12px;'>Athar Exhibition © 2026</div>", unsafe_allow_html=True)
