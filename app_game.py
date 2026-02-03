import streamlit as st
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")

# --- تنسيق CSS لملء الشاشة ---
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
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    
    body { 
        margin: 0; overflow: hidden; 
        background: radial-gradient(ellipse at center, #1b2735 0%, #090a0f 100%);
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
    
    .bar-container {
        width: 250px; height: 12px; 
        background: rgba(255,255,255,0.1); 
        border: 1px solid #5867dd; 
        border-radius: 6px; margin-top: 8px;
        box-shadow: 0 0 10px rgba(88, 103, 221, 0.2);
    }
    #signal-bar {
        width: 0%; height: 100%; 
        background: linear-gradient(90deg, #5867dd, #00f0ff);
        border-radius: 5px;
        box-shadow: 0 0 10px #00f0ff;
        transition: width 0.1s;
    }

    #word-container { 
        position: absolute; bottom: 80px; width: 100%; text-align: center; pointer-events: none; 
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

    /* شاشات (البداية / الخسارة / الفوز) */
    .screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 10;
    }
    
    #start-screen { background: radial-gradient(circle, rgba(20,20,30,0.98) 0%, rgba(0,0,0,1) 100%); }
    
    /* شاشة الخسارة (Time Out) */
    #timeout-screen { 
        background: rgba(20, 0, 0, 0.95); 
        display: none; 
        z-index: 30;
    }
    
    #cert-screen { background: #090a0f; display: none; z-index: 20; }
    
    .title-glow {
        font-size: 60px; color: #F4E4BC; margin-bottom: 10px; font-weight: bold;
        text-shadow: 0 0 30px rgba(244, 228, 188, 0.6);
        letter-spacing: 5px;
    }
    
    .fail-title {
        font-size: 60px; color: #ff4444; margin-bottom: 20px; font-weight: bold;
        text-shadow: 0 0 30px red; letter-spacing: 5px;
    }

    .subtitle {
        color: #a0a0a0; font-size: 20px; letter-spacing: 2px; margin-bottom: 40px;
    }

    /* الحقوق */
    .credits {
        margin-top: 60px; color: #555; font-size: 14px; letter-spacing: 1px;
        border-top: 1px solid #333; padding-top: 20px;
    }
    .credits span { color: #888; font-weight: bold; }

    .btn {
        padding: 18px 60px; font-size: 22px; font-weight: bold;
        background: linear-gradient(45deg, #F4E4BC, #d4af37);
        color: #000; border: none; border-radius: 50px;
        cursor: pointer; margin-top: 20px;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.4);
        transition: transform 0.2s, box-shadow 0.2s;
        font-family: 'Montserrat', sans-serif;
    }
    .btn:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(212, 175, 55, 0.7); }
    
    .btn-retry {
        background: linear-gradient(45deg, #ff4444, #cc0000);
        color: white; box-shadow: 0 0 20px rgba(255, 0, 0, 0.4);
    }
    .btn-retry:hover { box-shadow: 0 0 30px rgba(255, 0, 0, 0.7); }

    /* المؤقت */
    #timer-display {
        position: absolute; top: 30px; right: 40px;
        font-size: 36px; color: #F4E4BC; font-weight: bold;
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
    
    <div class="credits">
        POWERED BY <span>ATHAR CLUB</span> | DEVELOPED BY <span>ENG. ALYAA</span>
    </div>
</div>

<div id="timeout-screen" class="screen">
    <div class="fail-title">SIGNAL LOST</div>
    <p class="subtitle" style="color: #ffaaaa;">TIME CONNECTION EXPIRED</p>
    <button class="btn btn-retry" onclick="location.reload()">TRY AGAIN ↻</button>
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

<div id="cert-screen" class="screen">
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

    const sentence = ["ETHICS", "IS", "THE", "COMPASS", "OF", "ARTIFICIAL", "INTELLIGENCE"];
    let level = 1;
    const maxLevels = sentence.length;
    let foundWords = [];
    
    let target = { x: 0, y: 0 };
    let mouse = { x: canvas.width/2, y: canvas.height/2 };
    let gameRunning = false;
    let timeLeft = 60;
    let timerInterval;

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
        // إخفاء الواجهة وإظهار شاشة الخسارة
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

    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    window.addEventListener('mousedown', () => {
        if (!gameRunning) return;
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        if (dist < 50) winLevel();
    });

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
        let signalStrength = Math.max(0, 1 - (dist / 600));
        document.getElementById('signal-bar').style.width = (signalStrength * 100) + "%";

        let proximity = Math.max(0, 1 - (dist / 400));
        stars.forEach(star => {
            star.alpha += (Math.random() - 0.5) * 0.1;
            if (star.alpha < 0.2) star.alpha = 0.2;
            if (star.alpha > 1) star.alpha = 1;
            let size = star.baseSize + (proximity * 3);
            ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, size, 0, Math.PI * 2);
            ctx.fill();
        });

        let scopeColor = dist < 50 ? '#00ff00' : '#00f0ff';
        let scopeSize = 40;
        ctx.shadowBlur = 15;
        ctx.shadowColor = scopeColor;
        ctx.strokeStyle = scopeColor;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, scopeSize, 0, Math.PI * 2);
        ctx.stroke();
        
        ctx.beginPath();
        ctx.moveTo(mouse.x - scopeSize - 10, mouse.y);
        ctx.lineTo(mouse.x + scopeSize + 10, mouse.y);
        ctx.moveTo(mouse.x, mouse.y - scopeSize - 10);
        ctx.lineTo(mouse.x, mouse.y + scopeSize + 10);
        ctx.stroke();
        ctx.shadowBlur = 0;

        if (dist < 120) {
            let opacity = 1 - (dist / 120);
            ctx.shadowBlur = 20;
            ctx.shadowColor = "#F4E4BC";
            ctx.fillStyle = `rgba(244, 228, 188, ${opacity})`;
            drawStar(ctx, target.x, target.y, 5, 10, 5);
            ctx.shadowBlur = 0;
        }
    }
    
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

    function drawCertificate() {
        const c = document.getElementById('cert-canvas');
        const cx = c.getContext('2d');
        cx.fillStyle = '#0e0e0e';
        cx.fillRect(0,0,800,600);
        cx.strokeStyle = '#F4E4BC';
        cx.lineWidth = 5;
        cx.strokeRect(20,20,760,560);
        cx.lineWidth = 2;
        cx.strokeRect(30,30,740,540);
        cx.textAlign = 'center';
        cx.fillStyle = '#F4E4BC';
        cx.font = 'bold 40px Montserrat, sans-serif';
        cx.fillText('CERTIFICATE OF COMPLETION', 400, 120);
        cx.fillStyle = 'white';
        cx.font = '30px Montserrat, sans-serif';
        cx.fillText('ATHAR EVENT 2026', 400, 180);
        cx.fillStyle = '#ccc';
        cx.font = '18px Montserrat, sans-serif';
        cx.fillText('HAS SUCCESSFULLY DECODED THE SIGNAL', 400, 300);
        cx.fillStyle = '#F4E4BC';
        cx.shadowBlur = 10;
        cx.shadowColor = "#d4af37";
        cx.font = 'bold 26px Montserrat, sans-serif';
        cx.fillText('"ETHICS IS THE COMPASS', 400, 400);
        cx.fillText('OF ARTIFICIAL INTELLIGENCE"', 400, 440);
        cx.shadowBlur = 0;
        cx.fillStyle = '#555';
        cx.font = '14px Montserrat, sans-serif';
        cx.fillText('Athar Club | Eng. Alyaa', 400, 550);
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
