import streamlit as st
import streamlit.components.v1 as components

# --- إعدادات الصفحة (ملء الشاشة) ---
st.set_page_config(page_title="The Lost Signal", page_icon="🔭", layout="wide", initial_sidebar_state="collapsed")

# --- تنسيق CSS لإزالة الحواف وجعل اللعبة ملء الشاشة ---
st.markdown("""
    <style>
    /* إخفاء كل عناصر ستريم ليت الزائدة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* إزالة الهوامش والحواف تماماً */
    body {margin: 0; padding: 0; overflow: hidden; background-color: black;}
    .stApp {background-color: black; margin: 0;}
    .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
    
    /* جعل الإطار يملأ الشاشة */
    iframe {
        width: 100vw !important;
        height: 100vh !important;
        border: none;
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# --- كود اللعبة (HTML + JavaScript) ---
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body { margin: 0; overflow: hidden; background: #000; font-family: 'Courier New', Courier, monospace; user-select: none; }
    #gameCanvas { display: block; width: 100vw; height: 100vh; cursor: none; }
    
    /* واجهة المستخدم العلوية */
    #ui-layer { 
        position: absolute; top: 30px; left: 30px; 
        color: white; pointer-events: none; letter-spacing: 2px;
    }
    h1 { margin: 0; font-size: 20px; font-weight: normal; color: #888; }
    h2 { margin: 5px 0 0 0; font-size: 24px; color: white; }
    
    /* شريط الكلمات في الأسفل */
    #word-container { 
        position: absolute; bottom: 40px; width: 100%; text-align: center; pointer-events: none; 
    }
    #word-box { 
        display: inline-block;
        font-size: 24px; color: #fff; background: rgba(0,0,0,0.7); 
        padding: 15px 30px; border: 1px solid white; border-radius: 0;
        text-transform: uppercase; letter-spacing: 3px;
    }

    /* شاشة البداية */
    #start-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: black; display: flex; flex-direction: column;
        justify-content: center; align-items: center; z-index: 10;
    }
    .btn {
        padding: 15px 50px; font-size: 20px; background: transparent; color: white;
        border: 2px solid white; cursor: pointer; margin-top: 30px;
        font-family: 'Courier New', monospace; letter-spacing: 2px;
        transition: all 0.3s;
    }
    .btn:hover { background: white; color: black; }
    
    /* شاشة النهاية (الشهادة) */
    #cert-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: #0e0e0e; display: none; flex-direction: column;
        justify-content: center; align-items: center; z-index: 20;
    }
    
    .hidden { display: none !important; }
    
    /* المؤقت */
    #timer-display {
        position: absolute; top: 30px; right: 30px;
        font-size: 30px; color: white; font-weight: bold;
    }
    .warning { color: red !important; }

</style>
</head>
<body>

<div id="start-screen">
    <h1 style="font-size: 40px; color: white; margin-bottom: 20px;">ATHAR EVENT</h1>
    <p style="color: #aaa; font-size: 16px;">MOVE MOUSE TO LOCATE SIGNALS</p>
    <button class="btn" onclick="startGame()">INITIATE MISSION</button>
</div>

<div id="ui-layer">
    <h1 id="level-label">SIGNAL STRENGTH</h1>
    <div style="width: 200px; height: 10px; border: 1px solid #555; margin-top: 5px;">
        <div id="signal-bar" style="width: 0%; height: 100%; background: white;"></div>
    </div>
    <p id="level-counter" style="margin-top: 10px; color: #aaa;">TARGET 1 / 7</p>
</div>

<div id="timer-display">60</div>

<div id="word-container">
    <div id="word-box">LOCKED</div>
</div>

<canvas id="gameCanvas"></canvas>

<div id="cert-screen">
    <canvas id="cert-canvas" width="800" height="600" style="border: 2px solid white; margin-bottom: 20px;"></canvas>
    <div>
        <button class="btn" onclick="downloadCert()">DOWNLOAD</button>
        <button class="btn" onclick="location.reload()" style="margin-left: 20px;">RESTART</button>
    </div>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // إعدادات اللعبة
    // الجملة الجديدة الأطول
    const sentence = ["ETHICS", "IS", "THE", "COMPASS", "OF", "ARTIFICIAL", "INTELLIGENCE"];
    let level = 1;
    const maxLevels = sentence.length;
    let foundWords = [];
    
    let target = { x: 0, y: 0 };
    let mouse = { x: canvas.width/2, y: canvas.height/2 };
    let gameRunning = false;
    
    // المؤقت
    let timeLeft = 60;
    let timerInterval;

    // النجوم
    const stars = [];
    for(let i=0; i<400; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 1.5,
            baseSize: Math.random() * 1.5
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
        alert("TIME EXPIRED. SIGNAL LOST.");
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

    window.addEventListener('mousedown', () => {
        if (!gameRunning) return;
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        
        // إذا كان الهدف في النطاق
        if (dist < 50) {
            winLevel();
        }
    });

    function winLevel() {
        // فلاش أبيض بسيط
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
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
        
        // مسح الخلفية
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        
        // تحديث شريط الإشارة
        let signalStrength = Math.max(0, 1 - (dist / 600));
        document.getElementById('signal-bar').style.width = (signalStrength * 100) + "%";

        // رسم النجوم
        let proximity = Math.max(0, 1 - (dist / 400));
        
        stars.forEach(star => {
            // تأثير الحركة البسيط عند الاقتراب
            let size = star.baseSize + (proximity * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${0.4 + proximity})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, size, 0, Math.PI * 2);
            ctx.fill();
        });

        // رسم الهدف (مخفي، يظهر فقط عند الاقتراب جداً)
        if (dist < 100) {
            let opacity = 1 - (dist / 100);
            ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
            ctx.beginPath();
            ctx.arc(target.x, target.y, 5, 0, Math.PI * 2);
            ctx.fill();
        }

        // رسم السكوب (الدائرة)
        // اللون أبيض، يتحول للأخضر عند القرب الشديد
        let scopeColor = dist < 50 ? '#00ff00' : '#ffffff';
        let scopeSize = 40;
        
        ctx.strokeStyle = scopeColor;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, scopeSize, 0, Math.PI * 2);
        ctx.stroke();
        
        // خطوط التصويب (Crosshair)
        ctx.beginPath();
        ctx.moveTo(mouse.x - scopeSize - 5, mouse.y);
        ctx.lineTo(mouse.x + scopeSize + 5, mouse.y);
        ctx.moveTo(mouse.x, mouse.y - scopeSize - 5);
        ctx.lineTo(mouse.x, mouse.y + scopeSize + 5);
        ctx.stroke();
    }

    // --- الشهادة ---
    function drawCertificate() {
        const c = document.getElementById('cert-canvas');
        const cx = c.getContext('2d');
        
        // خلفية سوداء
        cx.fillStyle = '#0e0e0e';
        cx.fillRect(0,0,800,600);
        
        // إطار أبيض
        cx.strokeStyle = 'white';
        cx.lineWidth = 8;
        cx.strokeRect(20,20,760,560);
        
        cx.textAlign = 'center';
        
        // العنوان
        cx.fillStyle = 'white';
        cx.font = 'bold 40px Courier New';
        cx.fillText('CERTIFICATE OF COMPLETION', 400, 120);
        
        cx.fillStyle = '#aaa';
        cx.font = '30px Courier New';
        cx.fillText('ATHAR EVENT 2026', 400, 180);
        
        cx.fillStyle = '#ccc';
        cx.font = '18px Courier New';
        cx.fillText('MISSION SUCCESSFUL', 400, 300);
        
        // الجملة النهائية
        cx.fillStyle = 'white';
        cx.font = 'bold 24px Courier New';
        cx.fillText('"ETHICS IS THE COMPASS', 400, 400);
        cx.fillText('OF ARTIFICIAL INTELLIGENCE"', 400, 440);
        
        cx.fillStyle = '#555';
        cx.font = '14px Courier New';
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

# عرض اللعبة بملء الشاشة
components.html(game_html, height=1000, scrolling=False)
