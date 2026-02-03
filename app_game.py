import streamlit as st
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

# --- تنسيق CSS شامل ---
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
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    body { 
        margin: 0; overflow: hidden; 
        background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
        font-family: 'Montserrat', sans-serif; 
        user-select: none;
        touch-action: none; /* مهم جداً للجوال: يمنع السكرول */
    }
    #gameCanvas { display: block; width: 100vw; height: 100vh; cursor: none; touch-action: none; }
    
    /* واجهة المستخدم - متجاوبة */
    #ui-layer { 
        position: absolute; top: 20px; left: 20px; right: 20px;
        color: #F4E4BC; pointer-events: none; 
        text-shadow: 0 0 10px rgba(244, 228, 188, 0.3);
        display: flex; flex-direction: column; align-items: flex-start;
    }
    
    h1 { margin: 0; font-size: clamp(14px, 4vw, 18px); letter-spacing: 2px; color: #8892b0; }
    
    .bar-container {
        width: clamp(150px, 50vw, 300px); height: 12px; 
        background: rgba(255,255,255,0.1); 
        border: 1px solid #5867dd; 
        border-radius: 6px; margin-top: 8px;
        box-shadow: 0 0 10px rgba(88, 103, 221, 0.2);
    }
    #signal-bar {
        width: 0%; height: 100%; 
        background: linear-gradient(90deg, #5867dd, #00f0ff);
        border-radius: 5px; box-shadow: 0 0 10px #00f0ff;
        transition: width 0.1s;
    }

    #word-container { 
        position: absolute; bottom: 10%; width: 100%; 
        display: flex; justify-content: center; pointer-events: none; 
    }
    #word-box { 
        font-size: clamp(16px, 5vw, 26px); font-weight: bold; color: #fff; 
        background: rgba(14, 17, 23, 0.9); 
        padding: 15px 30px; 
        border: 1px solid #F4E4BC; border-radius: 30px;
        box-shadow: 0 0 20px rgba(244, 228, 188, 0.2);
        letter-spacing: 1px; text-align: center;
        max-width: 90%;
    }

    /* الشاشات */
    .screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 10;
        padding: 20px; box-sizing: border-box; text-align: center;
    }
    
    #start-screen { background: radial-gradient(circle, rgba(20,20,30,0.98) 0%, rgba(0,0,0,1) 100%); }
    #timeout-screen { background: rgba(20, 0, 0, 0.95); display: none; z-index: 30; }
    #cert-screen { background: #090a0f; display: none; z-index: 20; }
    
    .title-glow {
        font-size: clamp(30px, 8vw, 60px); color: #F4E4BC; margin-bottom: 10px; font-weight: bold;
        text-shadow: 0 0 30px rgba(244, 228, 188, 0.6); letter-spacing: 2px;
    }
    .fail-title {
        font-size: clamp(30px, 8vw, 60px); color: #ff4444; margin-bottom: 20px; font-weight: bold;
        text-shadow: 0 0 30px red; letter-spacing: 2px;
    }
    .subtitle { color: #a0a0a0; font-size: clamp(14px, 4vw, 20px); letter-spacing: 1px; margin-bottom: 30px; }

    .credits {
        position: absolute; bottom: 30px; width: 100%; text-align: center;
        color: #555; font-size: 12px; letter-spacing: 1px;
    }
    .credits span { color: #888; font-weight: bold; }

    .btn {
        padding: 15px 40px; font-size: clamp(16px, 4vw, 22px); font-weight: bold;
        background: linear-gradient(45deg, #F4E4BC, #d4af37);
        color: #000; border: none; border-radius: 50px;
        cursor: pointer; margin-top: 20px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        font-family: 'Montserrat', sans-serif;
        touch-action: manipulation; /* تحسين استجابة الزر */
    }
    
    #timer-display {
        position: absolute; top: 20px; right: 20px;
        font-size: clamp(24px, 6vw, 36px); color: #F4E4BC; font-weight: bold;
        text-shadow: 0 0 10px #d4af37;
    }
    .warning { color: #ff4444 !important; text-shadow: 0 0 20px red !important; animation: pulse 1s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    .hidden { display: none !important; }

</style>
</head>
<body>

<div id="start-screen" class="screen">
    <div class="title-glow">ATHAR EVENT</div>
    <p class="subtitle">THE LOST SIGNAL MISSION</p>
    <button class="btn" onclick="startGame()">START MISSION</button>
    <div class="credits">POWERED BY <span>ATHAR CLUB</span> | DEV BY <span>ENG. ALYAA</span></div>
</div>

<div id="timeout-screen" class="screen">
    <div class="fail-title">SIGNAL LOST</div>
    <p class="subtitle" style="color: #ffaaaa;">TIME CONNECTION EXPIRED</p>
    <button class="btn" style="background: linear-gradient(45deg, #ff4444, #cc0000); color: white;" onclick="location.reload()">TRY AGAIN ↻</button>
</div>

<div id="ui-layer">
    <h1 id="level-label">SIGNAL STRENGTH</h1>
    <div class="bar-container"><div id="signal-bar"></div></div>
    <p id="level-counter" style="margin-top: 10px; color: #ccc; font-size: 12px;">TARGET 1 / 5</p>
</div>

<div id="timer-display">60</div>

<div id="word-container"><div id="word-box">LOCKED</div></div>

<canvas id="gameCanvas"></canvas>

<div id="cert-screen" class="screen">
    <canvas id="cert-canvas" width="800" height="600" style="max-width: 90%; height: auto; border: 2px solid #F4E4BC; box-shadow: 0 0 50px rgba(244,228,188,0.2); margin-bottom: 20px; border-radius: 10px;"></canvas>
    <div>
        <button class="btn" onclick="downloadCert()">DOWNLOAD</button>
        <button class="btn" onclick="location.reload()" style="margin-left: 10px; background: #333; color: white; box-shadow: none;">RESTART</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // ضبط الحجم بدقة للأجهزة المختلفة
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // 5 كلمات فقط
    const sentence = ["ETHICS", "IS", "THE", "COMPASS", "OF AI"];
    let level = 1;
    const maxLevels = sentence.length;
    let foundWords = [];
    
    let target = { x: 0, y: 0 };
    let mouse = { x: canvas.width/2, y: canvas.height/2 };
    let gameRunning = false;
    let timeLeft = 60;
    let timerInterval;

    const stars = [];
    for(let i=0; i<300; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2,
            baseSize: Math.random() * 2,
            alpha: Math.random(),
        });
    }

    function spawnTarget() {
        const margin = Math.min(canvas.width, canvas.height) * 0.15;
        target.x = margin + Math.random() * (canvas.width - margin*2);
        target.y = margin + Math.random() * (canvas.height - margin*2);
    }

    function startTimer() {
        timeLeft = 60;
        document.getElementById('timer-display').innerText = timeLeft;
        document.getElementById('timer-display').classList.remove('warning');
        
        timerInterval = setInterval(() => {
            if(!gameRunning) return;
            timeLeft--;
            document.getElementById('timer-display').innerText = timeLeft;
            if(timeLeft <= 10) document.getElementById('timer-display').classList.add('warning');
            if(timeLeft <= 0) gameOver();
        }, 1000);
    }

    function gameOver() {
        gameRunning = false;
        clearInterval(timerInterval);
        document.getElementById('ui-layer').classList.add('hidden');
        document.getElementById('word-container').classList.add('hidden');
        document.getElementById('timer-display').classList.add('hidden');
        document.getElementById('timeout-screen').style.display = 'flex';
    }

    function startGame() {
        document.getElementById('start-screen').classList.add('hidden');
        spawnTarget();
        gameRunning = true;
        startTimer();
        loop();
    }

    // --- دعم الماوس ---
    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // --- دعم اللمس (للجوال) ---
    canvas.addEventListener('touchmove', e => {
        e.preventDefault(); // منع السكرول
        const touch = e.touches[0];
        mouse.x = touch.clientX;
        mouse.y = touch.clientY;
    }, { passive: false });
    
    // التقاط اللمسة الأولى للتوجيه السريع
    canvas.addEventListener('touchstart', e => {
        e.preventDefault();
        const touch = e.touches[0];
        mouse.x = touch.clientX;
        mouse.y = touch.clientY;
        checkWin(); // فحص إذا ضغط مباشرة على الهدف
    }, { passive: false });

    // النقر للالتقاط
    window.addEventListener('mousedown', () => {
        if (!gameRunning) return;
        checkWin();
    });

    function checkWin() {
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        // زيادة مساحة الفوز في الجوال لتسهيل اللعب
        let winRadius = (window.innerWidth < 600) ? 70 : 50; 
        
        if (dist < winRadius) {
            winLevel();
        }
    }

    function winLevel() {
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
        
        let gradient = ctx.createRadialGradient(canvas.width/2, canvas.height/2, 0, canvas.width/2, canvas.height/2, canvas.width);
        gradient.addColorStop(0, "#1b2735");
        gradient.addColorStop(1, "#090a0f");
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        let signalStrength = Math.max(0, 1 - (dist / (Math.min(canvas.width, canvas.height)*0.8)));
        document.getElementById('signal-bar').style.width = (signalStrength * 100) + "%";

        let proximity = Math.max(0, 1 - (dist / 400));
        stars.forEach(star => {
            star.alpha += (Math.random() - 0.5) * 0.1;
            if (star.alpha < 0.2) star.alpha = 0.2; if (star.alpha > 1) star.alpha = 1;
            let size = star.baseSize + (proximity * 3);
            ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
            ctx.beginPath(); ctx.arc(star.x, star.y, size, 0, Math.PI * 2); ctx.fill();
        });

        let scopeColor = dist < 50 ? '#00ff00' : '#00f0ff';
        let scopeSize = (window.innerWidth < 600) ? 30 : 40; // تصغير السكوب في الجوال
        
        ctx.shadowBlur = 15; ctx.shadowColor = scopeColor;
        ctx.strokeStyle = scopeColor; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(mouse.x, mouse.y, scopeSize, 0, Math.PI * 2); ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(mouse.x - scopeSize - 10, mouse.y); ctx.lineTo(mouse.x + scopeSize + 10, mouse.y);
        ctx.moveTo(mouse.x, mouse.y - scopeSize - 10); ctx.lineTo(mouse.x, mouse.y + scopeSize + 10);
        ctx.stroke(); ctx.shadowBlur = 0;

        // رسم الهدف
        if (dist < 120) {
            let opacity = 1 - (dist / 120);
            ctx.shadowBlur = 20; ctx.shadowColor = "#F4E4BC";
            ctx.fillStyle = `rgba(244, 228, 188, ${opacity})`;
            ctx.beginPath(); ctx.arc(target.x, target.y, 8, 0, Math.PI*2); ctx.fill();
            ctx.shadowBlur = 0;
        }
    }

    function drawCertificate() {
        const c = document.getElementById('cert-canvas');
        const cx = c.getContext('2d');
        cx.fillStyle = '#0e0e0e'; cx.fillRect(0,0,800,600);
        cx.strokeStyle = '#F4E4BC'; cx.lineWidth = 5; cx.strokeRect(20,20,760,560);
        cx.lineWidth = 2; cx.strokeRect(30,30,740,540);
        
        cx.textAlign = 'center';
        cx.fillStyle = '#F4E4BC'; cx.font = 'bold 40px Montserrat, sans-serif';
        cx.fillText('CERTIFICATE OF COMPLETION', 400, 120);
        
        cx.fillStyle = 'white'; cx.font = '30px Montserrat, sans-serif';
        cx.fillText('ATHAR EVENT 2026', 400, 180);
        
        cx.fillStyle = '#ccc'; cx.font = '18px Montserrat, sans-serif';
        cx.fillText('HAS SUCCESSFULLY DECODED THE SIGNAL', 400, 300);
        
        cx.fillStyle = '#F4E4BC'; cx.shadowBlur = 10; cx.shadowColor = "#d4af37";
        cx.font = 'bold 26px Montserrat, sans-serif';
        cx.fillText('"ETHICS IS THE COMPASS', 400, 400);
        cx.fillText('OF AI"', 400, 450);
        cx.shadowBlur = 0;
        
        cx.fillStyle = '#555'; cx.font = '14px Montserrat, sans-serif';
        cx.fillText('Athar Club | Eng. Alyaa', 400, 550);
    }

    window.downloadCert = function() {
        const link = document.createElement('a');
        link.download = 'Athar_Event_Cert.png';
        link.href = document.getElementById('cert-canvas').toDataURL();
        link.click();
    }
</script>
</body>
</html>
"""

components.html(game_html, height=1000, scrolling=False)
