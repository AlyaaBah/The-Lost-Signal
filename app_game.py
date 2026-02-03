import streamlit as st
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

# --- تنسيق CSS لملء الشاشة وإزالة الحواف ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    body {margin: 0; padding: 0; overflow: hidden; background-color: #090a0f;}
    .stApp {background-color: #090a0f; margin: 0;}
    .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
    iframe { width: 100vw !important; height: 100vh !important; border: none; display: block; }
    </style>
""", unsafe_allow_html=True)

# --- كود اللعبة (HTML + JavaScript) ---
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    /* الخطوط والألوان */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    body { 
        margin: 0; overflow: hidden; 
        background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%); /* خلفية المجرة */
        font-family: 'Montserrat', sans-serif; 
        user-select: none; 
    }
    #gameCanvas { display: block; width: 100vw; height: 100vh; cursor: none; }
    
    /* واجهة المستخدم */
    #ui-layer { 
        position: absolute; top: 30px; left: 30px; 
        color: #F4E4BC; pointer-events: none; 
        text-shadow: 0 0 10px rgba(244, 228, 188, 0.3);
    }
    h1 { margin: 0; font-size: 18px; letter-spacing: 2px; color: #8892b0; }
    h2 { margin: 5px 0 0 0; font-size: 24px; color: white; }
    
    /* شريط الإشارة */
    .bar-container {
        width: 250px; height: 12px; 
        background: rgba(255,255,255,0.1); 
        border: 1px solid #5867dd; 
        border-radius: 6px; margin-top: 8px;
        box-shadow: 0 0 10px rgba(88, 103, 221, 0.2);
    }
    #signal-bar {
        width: 0%; height: 100%; 
        background: linear-gradient(90deg, #5867dd, #00f0ff); /* تدرج أزرق سماوي */
        border-radius: 5px;
        box-shadow: 0 0 10px #00f0ff;
        transition: width 0.1s;
    }

    /* الكلمات في الأسفل */
    #word-container { 
        position: absolute; bottom: 50px; width: 100%; text-align: center; pointer-events: none; 
    }
    #word-box { 
        display: inline-block;
        font-size: 26px; font-weight: bold; color: #fff; 
        background: rgba(14, 17, 23, 0.8); 
        padding: 15px 40px; 
        border: 1px solid #F4E4BC; border-radius: 30px;
        box-shadow: 0 0 20px rgba(244, 228, 188, 0.2);
        letter-spacing: 2px;
    }

    /* شاشة البداية */
    #start-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle, rgba(20,20,30,0.95) 0%, rgba(0,0,0,1) 100%);
        display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 10;
    }
    .title-glow {
        font-size: 50px; color: #F4E4BC; margin-bottom: 20px; font-weight: bold;
        text-shadow: 0 0 20px rgba(244, 228, 188, 0.6);
        letter-spacing: 5px;
    }
    .btn {
        padding: 18px 60px; font-size: 22px; font-weight: bold;
        background: linear-gradient(45deg, #F4E4BC, #d4af37);
        color: #000; border: none; border-radius: 50px;
        cursor: pointer; margin-top: 40px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
        font-family: 'Montserrat', sans-serif;
    }
    .btn:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(212, 175, 55, 0.7); }
    
    /* المؤقت */
    #timer-display {
        position: absolute; top: 30px; right: 40px;
        font-size: 36px; color: #F4E4BC; font-weight: bold;
        text-shadow: 0 0 10px #d4af37;
    }
    .warning { color: #ff4444 !important; text-shadow: 0 0 20px red !important; animation: pulse 1s infinite; }
    
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }

    /* الشهادة */
    #cert-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: #090a0f; display: none; flex-direction: column;
        justify-content: center; align-items: center; z-index: 20;
    }
    .hidden { display: none !important; }

</style>
</head>
<body>

<div id="start-screen">
    <div class="title-glow">ATHAR EVENT</div>
    <p style="color: #a0a0a0; font-size: 18px; letter-spacing: 1px;">THE LOST SIGNAL MISSION</p>
    <button class="btn" onclick="startGame()">START MISSION</button>
</div>

<div id="ui-layer">
    <h1 id="level-label">SIGNAL STRENGTH</h1>
    <div class="bar-container">
        <div id="signal-bar"></div>
    </div>
    <p id="level-counter" style="margin-top: 10px; color: #ccc;">TARGET 1 / 7</p>
</div>

<div id="timer-display">60</div>

<div id="word-container">
    <div id="word-box">LOCKED</div>
</div>

<canvas id="gameCanvas"></canvas>

<div id="cert-screen">
    <canvas id="cert-canvas" width="800" height="600" style="border: 2px solid #F4E4BC; box-shadow: 0 0 50px rgba(244,228,188,0.2); margin-bottom: 30px; border-radius: 10px;"></canvas>
    <div>
        <button class="btn" onclick="downloadCert()">DOWNLOAD</button>
        <button class="btn" onclick="location.reload()" style="margin-left: 20px; background: #333; color: white; box-shadow: none;">RESTART</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // إعدادات اللعبة
    const sentence = ["ETHICS", "IS", "THE", "COMPASS", "OF", "ARTIFICIAL", "INTELLIGENCE"];
    let level = 1;
    const maxLevels = sentence.length;
    let foundWords = [];
    
    let target = { x: 0, y: 0 };
    let mouse = { x: canvas.width/2, y: canvas.height/2 };
    let gameRunning = false;
    let timeLeft = 60;
    let timerInterval;

    // توليد نجوم (أكثر جمالية)
    const stars = [];
    for(let i=0; i<350; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2,
            baseSize: Math.random() * 2,
            alpha: Math.random(),
            speed: Math.random() * 0.5
        });
    }

    function spawnTarget() {
        target.x = Math.random() * (canvas.width - 200) + 100;
        target.y = Math.random() * (canvas.height - 200) + 100;
    }

    function startTimer() {
        timeLeft = 60;
        document.getElementById('timer-display').innerText = timeLeft;
        document.getElementById('timer-display').classList.remove('warning');
        
        timerInterval = setInterval(() => {
            if(!gameRunning) return;
            timeLeft--;
            document.getElementById('timer-display').innerText = timeLeft;
            
            if(timeLeft <= 10) {
                document.getElementById('timer-display').classList.add('warning');
            }
            if(timeLeft <= 0) {
                gameOver();
            }
        }, 1000);
    }

    function gameOver() {
        gameRunning = false;
        clearInterval(timerInterval);
        alert("SIGNAL LOST. TIME EXPIRED.");
        location.reload();
    }

    function startGame() {
        document.getElementById('start-screen').classList.add('hidden');
        spawnTarget();
        gameRunning = true;
        startTimer();
        loop();
    }

    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // النقر للالتقاط
    window.addEventListener('mousedown', () => {
        if (!gameRunning) return;
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        if (dist < 50) winLevel();
    });

    function winLevel() {
        // فلاش ذهبي ناعم
        ctx.fillStyle = 'rgba(244, 228, 188, 0.4)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        foundWords.push(sentence[level-1]);
        document.getElementById('word-box').innerText = foundWords.join(" ");
        
        if (level >= maxLevels) {
            gameWin();
        } else {
            level++;
            document.getElementById('level-counter').innerText = `TARGET ${level} / ${maxLevels}`;
            spawnTarget();
        }
    }

    function gameWin() {
        gameRunning = false;
        clearInterval(timerInterval);
        document.getElementById('ui-layer').classList.add('hidden');
        document.getElementById('word-container').classList.add('hidden');
        document.getElementById('timer-display').classList.add('hidden');
        document.getElementById('cert-screen').style.display = 'flex';
        drawCertificate();
    }

    function loop() {
        if (!gameRunning) return;
        requestAnimationFrame(loop);
        
        // رسم الخلفية (تدرج مع شفافية لإعطاء تأثير ذيل للحركة)
        let gradient = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 0, canvas.width/2, canvas.height/2, canvas.width);
        gradient.addColorStop(0, "#1b2735");
        gradient.addColorStop(1, "#090a0f");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        
        // تحديث شريط الإشارة
        let signalStrength = Math.max(0, 1 - (dist / 600));
        document.getElementById('signal-bar').style.width = (signalStrength * 100) + "%";

        // رسم النجوم
        let proximity = Math.max(0, 1 - (dist / 400));
        
        stars.forEach(star => {
            // تأثير وميض النجوم
            star.alpha += (Math.random() - 0.5) * 0.1;
            if (star.alpha < 0.2) star.alpha = 0.2;
            if (star.alpha > 1) star.alpha = 1;
            
            let size = star.baseSize + (proximity * 3); // زوم عند القرب
            
            ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, size, 0, Math.PI * 2);
            ctx.fill();
        });

        // رسم السكوب (متوهج)
        // أزرق سماوي عادي، وأخضر عند القرب
        let scopeColor = dist < 50 ? '#00ff00' : '#00f0ff';
        let scopeSize = 40;
        
        ctx.shadowBlur = 15;
        ctx.shadowColor = scopeColor;
        ctx.strokeStyle = scopeColor;
        ctx.lineWidth = 3;
        
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, scopeSize, 0, Math.PI * 2);
        ctx.stroke();
        
        // Crosshair
        ctx.beginPath();
        ctx.moveTo(mouse.x - scopeSize - 10, mouse.y);
        ctx.lineTo(mouse.x + scopeSize + 10, mouse.y);
        ctx.moveTo(mouse.x, mouse.y - scopeSize - 10);
        ctx.lineTo(mouse.x, mouse.y + scopeSize + 10);
        ctx.stroke();
        
        ctx.shadowBlur = 0; // إعادة ضبط الظل

        // رسم الهدف (نجمة ذهبية تظهر عند القرب)
        if (dist < 120) {
            let opacity = 1 - (dist / 120);
            ctx.shadowBlur = 20;
            ctx.shadowColor = "#F4E4BC";
            ctx.fillStyle = `rgba(244, 228, 188, ${opacity})`;
            
            // رسم شكل نجمة
            drawStar(ctx, target.x, target.y, 5, 10, 5);
            ctx.shadowBlur = 0;
        }
    }
    
    // دالة مساعدة لرسم نجمة
    function drawStar(cx, cy, spikes, outerRadius, innerRadius) {
        let rot = Math.PI / 2 * 3;
        let x = cx;
        let y = cy;
        let step = Math.PI / spikes;

        ctx.beginPath();
        ctx.moveTo(cx, cy - outerRadius);
        for (let i = 0; i < spikes; i++) {
            x = cx + Math.cos(rot) * outerRadius;
            y = cy + Math.sin(rot) * outerRadius;
            ctx.lineTo(x, y);
            rot += step;

            x = cx + Math.cos(rot) * innerRadius;
            y = cy + Math.sin(rot) * innerRadius;
            ctx.lineTo(x, y);
            rot += step;
        }
        ctx.lineTo(cx, cy - outerRadius);
        ctx.closePath();
        ctx.fill();
    }

    // --- الشهادة ---
    function drawCertificate() {
        const c = document.getElementById('cert-canvas');
        const cx = c.getContext('2d');
        
        // خلفية سوداء
        cx.fillStyle = '#0e0e0e';
        cx.fillRect(0,0,800,600);
        
        // إطار ذهبي مزدوج
        cx.strokeStyle = '#F4E4BC';
        cx.lineWidth = 5;
        cx.strokeRect(20,20,760,560);
        cx.lineWidth = 2;
        cx.strokeRect(30,30,740,540);
        
        cx.textAlign = 'center';
        
        // العنوان
        cx.fillStyle = '#F4E4BC';
        cx.font = 'bold 40px Montserrat, sans-serif';
        cx.fillText('CERTIFICATE OF COMPLETION', 400, 120);
        
        cx.fillStyle = 'white';
        cx.font = '30px Montserrat, sans-serif';
        cx.fillText('ATHAR EVENT 2026', 400, 180);
        
        cx.fillStyle = '#ccc';
        cx.font = '18px Montserrat, sans-serif';
        cx.fillText('HAS SUCCESSFULLY DECODED THE SIGNAL', 400, 300);
        
        // الجملة النهائية
        cx.fillStyle = '#F4E4BC';
        cx.shadowBlur = 10;
        cx.shadowColor = "#d4af37";
        cx.font = 'bold 26px Montserrat, sans-serif';
        cx.fillText('"ETHICS IS THE COMPASS', 400, 400);
        cx.fillText('OF ARTIFICIAL INTELLIGENCE"', 400, 440);
        cx.shadowBlur = 0;
        
        cx.fillStyle = '#555';
        cx.font = '14px Montserrat, sans-serif';
        cx.fillText('Eng. Alyaa', 400, 550);
    }

    window.downloadCert = function() {
        const link = document.createElement('a');
        link.download = 'Athar_Event_Cert.png';
        link.href = document.getElementById('cert-canvas').toDataURL();
        link.click();
    }

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

</script>
</body>
</html>
"""

components.html(game_html, height=1000, scrolling=False)
