import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
from PIL import Image, ImageDraw
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🔭", layout="wide") # خليناها wide عشان الخريطة تاخذ راحتها

# --- 2. ستايل وتنسيق ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #000000; }
    
    /* تنسيق الحاويات لتشبه لوحة تحكم مركبة فضائية */
    .control-panel {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
    }
    .metric-box {
        background-color: #0e1117;
        border: 1px solid #F4E4BC;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        color: #F4E4BC;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. إدارة حالة اللعبة ---
if 'level' not in st.session_state: st.session_state.level = 1
# نولد نجوم خلفية مرة واحدة فقط عشان ما تتغير كل شوي
if 'bg_stars_x' not in st.session_state: 
    st.session_state.bg_stars_x = np.random.randint(0, 100, 200)
    st.session_state.bg_stars_y = np.random.randint(0, 100, 200)

if 'target_x' not in st.session_state: st.session_state.target_x = random.randint(10, 90)
if 'target_y' not in st.session_state: st.session_state.target_y = random.randint(10, 90)
if 'game_over' not in st.session_state: st.session_state.game_over = False
if 'game_won' not in st.session_state: st.session_state.game_won = False
if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

# --- 4. النصوص واللغات ---
lang = st.radio("", ["العربية", "English"], horizontal=True)
is_ar = lang == "العربية"

texts = {
    "title": "🔭 لغز النجم الضائع" if is_ar else "🔭 The Lost Signal",
    "instr": "استخدم أدوات التحكم لتحريك السكوب 🔴 والبحث عن إشارة النجم المخفي" if is_ar else "Use controls to move the scope 🔴 and find the hidden star signal",
    "zoom": "🔍 مستوى التقريب (Zoom)" if is_ar else "🔍 Zoom Level",
    "x_move": "↔️ تحريك أفقي" if is_ar else "↔️ Horizontal Move",
    "y_move": "↕️ تحريك عمودي" if is_ar else "↕️ Vertical Move",
    "signal": "قوة الإشارة" if is_ar else "Signal Strength",
    "scan": "📸 التقاط (SCAN)" if is_ar else "📸 SCAN",
    "time": "الزمن" if is_ar else "Time",
    "level": "المستوى" if is_ar else "Level",
    "found": "✅ تم رصد الهدف!" if is_ar else "✅ Target Locked!",
    "miss": "❌ لا يوجد شيء هنا" if is_ar else "❌ Nothing here",
    "win_title": "🎉 اكتملت المهمة!" if is_ar else "🎉 Mission Accomplished!",
    "cert_btn": "تحميل الشهادة" if is_ar else "Download Certificate",
    "sentence": ["أخلاقياتك", "هي", "بوصلة", "الذكاء", "الاصطناعي"] if is_ar else ["Ethics", "is", "the", "Compass", "of AI"]
}

# --- 5. دالة رسم الخريطة (القلب النابض للعبة) ---
def draw_scope_view(user_x, user_y, zoom, signal_strength):
    fig = go.Figure()

    # 1. رسم نجوم الخلفية (المجرة)
    fig.add_trace(go.Scatter(
        x=st.session_state.bg_stars_x,
        y=st.session_state.bg_stars_y,
        mode='markers',
        marker=dict(size=3, color='white', opacity=0.5),
        hoverinfo='none'
    ))

    # 2. رسم "السكوب" (دائرة النظر)
    # لون الدائرة يتغير حسب قربك من الهدف (أحمر = بعيد، أخضر = قريب)
    scope_color = "#00ff00" if signal_strength > 80 else "#ff0000"
    
    # نستخدم شكل دائرة لتحديد منطقة النظر
    # حجم الدائرة يصغر كل ما سويت زوم عشان الدقة
    circle_size = 15 / zoom 
    
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=user_x - circle_size, y0=user_y - circle_size,
        x1=user_x + circle_size, y1=user_y + circle_size,
        line_color=scope_color,
        line_width=3,
    )

    # 3. إعدادات المحاور (الزوم)
    # نحسب النطاق الظاهر بناءً على الزوم
    range_span = 100 / zoom
    x_min = max(0, user_x - range_span/2)
    x_max = min(100, user_x + range_span/2)
    y_min = max(0, user_y - range_span/2)
    y_max = min(100, user_y + range_span/2)

    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(range=[x_min, x_max], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[y_min, y_max], showgrid=False, zeroline=False, visible=False),
        paper_bgcolor='black',
        plot_bgcolor='black',
        dragmode=False # منع التحريك بالماوس ليكون اللعب بالسلايدر حصراً
    )
    return fig

# --- 6. دالة الشهادة ---
def create_certificate():
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='#0e1117')
    draw = ImageDraw.Draw(img)
    draw.rectangle([20, 20, width-20, height-20], outline="#F4E4BC", width=5)
    draw.text((width//2, 100), "CERTIFICATE OF COMPLETION", fill="#F4E4BC", anchor="mm", font_size=40)
    draw.text((width//2, 180), "ATHAR EXHIBITION 2026", fill="white", anchor="mm", font_size=30)
    draw.text((width//2, 300), "The player has successfully found", fill="#cccccc", anchor="mm", font_size=20)
    draw.text((width//2, 350), "ALL HIDDEN SIGNALS", fill="#cccccc", anchor="mm", font_size=25)
    draw.text((width//2, 450), "Ethics is the Compass of AI", fill="#F4E4BC", anchor="mm", font_size=25)
    return img

# --- 7. الواجهة الرئيسية ---

st.title(texts["title"])

# شاشة الفوز
if st.session_state.game_won:
    st.balloons()
    st.markdown(f"""
        <div style="text-align: center; border: 2px solid #00ff00; padding: 20px; border-radius: 15px;">
            <h1 style="color: #00ff00;">{texts['win_title']}</h1>
            <h3>"Ethics is the Compass of AI"</h3>
        </div>
        """, unsafe_allow_html=True)
    
    buf = io.BytesIO()
    create_certificate().save(buf, format="PNG")
    st.download_button(texts["cert_btn"], data=buf.getvalue(), file_name="Certificate.png", mime="image/png")
    
    if st.button("🔄 Reset"):
        for k in st.session_state.keys(): del st.session_state[k]
        st.rerun()

# شاشة الخسارة
elif st.session_state.game_over:
    st.error("Time is up! Signal Lost.")
    if st.button("🔄 Retry"):
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.rerun()

# اللعبة مستمرة
else:
    # المؤقت
    elapsed = time.time() - st.session_state.start_time
    left = 60 - elapsed
    if left <= 0:
        st.session_state.game_over = True
        st.rerun()
    
    # تقسيم الشاشة: يسار (تحكم) - يمين (الخريطة)
    col_ctrl, col_map = st.columns([1, 2])
    
    # حساب الإشارة
    # نستخدم قيم افتراضية للمتغيرات (default values) عشان الـ sliders ما تعلق
    if 'u_x' not in st.session_state: st.session_state.u_x = 50
    if 'u_y' not in st.session_state: st.session_state.u_y = 50
    if 'u_z' not in st.session_state: st.session_state.u_z = 1.0

    with col_ctrl:
        st.markdown(f"<div class='control-panel'>", unsafe_allow_html=True)
        
        # معلومات
        st.metric(texts["time"], f"{int(left)}s")
        st.caption(f"{texts['level']}: {st.session_state.level} / 5")
        
        # الجملة السرية
        words_found = texts["sentence"][:st.session_state.level-1]
        st.info("🧩 " + " ".join(words_found) if words_found else "🧩 ...")

        st.write("---")
        
        # أدوات التحكم
        zoom = st.slider(texts["zoom"], 1.0, 5.0, 1.0, 0.5)
        user_x = st.slider(texts["x_move"], 0, 100, 50)
        user_y = st.slider(texts["y_move"], 0, 100, 50)
        
        # حساب المسافة وقوة الإشارة
        dist = np.sqrt((user_x - st.session_state.target_x)**2 + (user_y - st.session_state.target_y)**2)
        signal = max(0, 100 - (dist * 3)) # معادلة الحساسية
        
        # عرض قوة الإشارة
        st.write(texts["signal"])
        st.progress(int(signal) / 100)
        
        if signal > 85:
            st.success("TARGET LOCKED! 🎯")
        
        # زر الالتقاط
        if st.button(texts["scan"], use_container_width=True):
            if signal > 85: # لازم تكون دقيق
                if st.session_state.level == 5:
                    st.session_state.game_won = True
                else:
                    st.toast(texts["found"])
                    st.session_state.level += 1
                    st.session_state.target_x = random.randint(10, 90)
                    st.session_state.target_y = random.randint(10, 90)
                    st.session_state.start_time = time.time() # تمديد وقت
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(texts["miss"])
                
        st.markdown("</div>", unsafe_allow_html=True)

    with col_map:
        # رسم الخريطة مع السكوب
        fig = draw_scope_view(user_x, user_y, zoom, signal)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: grey;'>Athar Exhibition 2026</div>", unsafe_allow_html=True)
