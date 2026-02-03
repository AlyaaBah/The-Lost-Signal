import streamlit as st
import streamlit.components.v1 as components

# --- إعدادات الصفحة ---
st.set_page_config(page_title="The Lost Signal", page_icon="🌌", layout="wide")

# --- إخفاء القوائم ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    body {margin: 0; padding: 0; overflow: hidden; background-color: black;}
    .stApp {background-color: black;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    </style>
""", unsafe_allow_html=True)

# --- كود اللعبة (HTML + JavaScript) ---
# هذا الكود يعمل داخل المتصفح مباشرة لضمان سرعة الصوت والحركة
game_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    body { margin: 0; overflow: hidden; background: #000; font-family: 'Segoe UI', sans-serif; user-select: none; }
    #gameCanvas { display: block; width: 100vw; height: 100vh; cursor: none; }
    #ui-layer { position: absolute; top: 20px; left: 20px; color: #F4E4BC; pointer-events: none; }
    h1 { margin: 0; font-size: 24px; text-shadow: 0 0 10px #5867dd; }
    p { font-size: 18px; color: #ccc; }
    #word-box { 
        position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%);
        font-size: 28px; color: #fff; background: rgba(0,0,0,0.5); padding: 10px 20px; 
        border: 1px solid #5867dd; border-radius: 10px; pointer-events: none;
    }
    #start-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.9); display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white; z-index: 10;
    }
    button {
        padding: 15px 40px; font-size: 24px; background: #5867dd; color: white;
        border: none; border-radius: 30px; cursor: pointer; margin-top: 20px;
        box-shadow: 0 0 20px #5867dd; transition: transform 0.2s;
    }
    button:hover { transform: scale(1.1); }
    .hidden { display: none !important; }
    
    /* شهادة النهاية */
    #cert-screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: #0e0e0e; display: none; flex-direction: column;
        justify-content: center; align-items: center; z-index: 20;
    }
    #cert-canvas { border: 5px solid #F4E4BC; box-shadow: 0 0 30px rgba(244, 228, 188, 0.2); }
</style>
</head>
<body>

<div id="start-screen">
    <h1 style="font-size: 50px; color: #F4E4BC;">🌌 THE LOST SIGNAL</h1>
    <p>Move your mouse to find the hidden stars.</p>
    <p>Listen to the signal sound 🔊</p>
    <button onclick="startGame()">START MISSION</button>
</div>

<div id="ui-layer">
    <h1 id="level-txt">LEVEL 1/5</h1>
    <p id="status-txt">Searching for signal...</p>
</div>

<div id="word-box">🔒 LOCKED</div>

<canvas id="gameCanvas"></canvas>

<div id="cert-screen">
    <canvas id="cert-canvas" width="800" height="600"></canvas>
    <button onclick="downloadCert()">📥 Download Certificate</button>
    <button onclick="location.reload()" style="background: #333; margin-top:10px; font-size:18px;">↻ New Game</button>
</div>

<script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    
    // إعدادات الشاشة
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // متغيرات اللعبة
    let level = 1;
    const maxLevels = 5;
    const sentence = ["Ethics", "is", "the", "Compass", "of AI"];
    let foundWords = [];
    let target = { x: 0, y: 0 };
    let mouse = { x: canvas.width/2, y: canvas.height/2 };
    let gameRunning = false;
    let audioCtx, osc, gainNode;

    // النجوم الخلفية
    const stars = [];
    for(let i=0; i<300; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2,
            baseSize: Math.random() * 2
        });
    }

    function spawnTarget() {
        // مكان عشوائي للهدف مع هامش
        target.x = Math.random() * (canvas.width - 200) + 100;
        target.y = Math.random() * (canvas.height - 200) + 100;
    }

    // --- نظام الصوت (الرادار) ---
    function initAudio() {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        osc = audioCtx.createOscillator();
        gainNode = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.value = 200; // تردد البداية
        gainNode.gain.value = 0;   // صامت في البداية
        
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        osc.start();
    }

    function updateAudio(dist, maxDist) {
        if (!gameRunning) return;
        
        // كل ما قربت المسافة (dist) يقل، الصوت يزيد
        let proximity = 1 - (dist / (maxDist * 0.6)); // حساسية الرادار
        proximity = Math.max(0, proximity); // لا يقل عن صفر

        // رفع الصوت
        gainNode.gain.setTargetAtTime(proximity * 0.5, audioCtx.currentTime, 0.1);
        
        // تغيير النغمة (Pitch)
        // كل ما قربت تصير النغمة أحدّ وأعلى
        osc.frequency.setTargetAtTime(200 + (proximity * 800), audioCtx.currentTime, 0.1);
    }

    // --- تشغيل اللعبة ---
    function startGame() {
        document.getElementById('start-screen').classList.add('hidden');
        initAudio();
        spawnTarget();
        gameRunning = true;
        loop();
    }

    // --- حركة الماوس ---
    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    // --- النقر (Scan) ---
    window.addEventListener('mousedown', () => {
        if (!gameRunning) return;
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        
        // إذا كان قريب جداً (أقل من 50 بكسل)
        if (dist < 50) {
            winLevel();
        }
    });

    function winLevel() {
        // فلاش أخضر
        ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        foundWords.push(sentence[level-1]);
        document.getElementById('word-box').innerText = "✅ " + foundWords.join(" ... ");
        
        if (level >= maxLevels) {
            gameWin();
        } else {
            level++;
            document.getElementById('level-txt').innerText = `LEVEL ${level}/${maxLevels}`;
            spawnTarget();
        }
    }

    function gameWin() {
        gameRunning = false;
        gainNode.gain.value = 0; // إيقاف الصوت
        document.getElementById('ui-layer').classList.add('hidden');
        document.getElementById('word-box').classList.add('hidden');
        document.getElementById('cert-screen').style.display = 'flex';
        drawCertificate();
    }

    // --- حلقة الرسم (Game Loop) ---
    function loop() {
        if (!gameRunning) return;
        requestAnimationFrame(loop);
        
        // مسح الشاشة
        ctx.fillStyle = 'black';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        let dist = Math.hypot(mouse.x - target.x, mouse.y - target.y);
        let maxDist = Math.hypot(canvas.width, canvas.height);
        
        updateAudio(dist, maxDist);

        // 1. رسم النجوم (تأثير الزوم)
        // كل ما قربت من الهدف، النجوم تكبر وتبتعد عن المركز (تأثير السرعة)
        let proximity = Math.max(0, 1 - (dist / 500));
        
        stars.forEach(star => {
            let size = star.baseSize + (proximity * 3); // النجوم تكبر
            ctx.fillStyle = `rgba(255, 255, 255, ${0.5 + proximity})`;
            ctx.beginPath();
            ctx.arc(star.x, star.y, size, 0, Math.PI * 2);
            ctx.fill();
        });

        // 2. رسم الهدف (يظهر فقط لما تكون قريب جداً)
        if (dist < 150) {
            let opacity = 1 - (dist / 150);
            ctx.fillStyle = `rgba(255, 255, 0, ${opacity})`; // نجم أصفر
            ctx.beginPath();
            ctx.arc(target.x, target.y, 10, 0, Math.PI * 2);
            ctx.fill();
            
            // هالة حول النجم
            ctx.strokeStyle = `rgba(255, 255, 0, ${opacity * 0.5})`;
            ctx.beginPath();
            ctx.arc(target.x, target.y, 20 + Math.sin(Date.now()/100)*5, 0, Math.PI * 2);
            ctx.stroke();
        }

        // 3. رسم السكوب (الدائرة الحمراء/الخضراء)
        let scopeColor = dist < 50 ? '#00ff00' : '#ff0000';
        let scopeSize = 40;
        
        ctx.strokeStyle = scopeColor;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(mouse.x, mouse.y, scopeSize, 0, Math.PI * 2);
        ctx.stroke();
        
        // خطوط التصويب
        ctx.beginPath();
        ctx.moveTo(mouse.x - scopeSize - 10, mouse.y);
        ctx.lineTo(mouse.x + scopeSize + 10, mouse.y);
        ctx.moveTo(mouse.x, mouse.y - scopeSize - 10);
        ctx.lineTo(mouse.x, mouse.y + scopeSize + 10);
        ctx.stroke();

        // 4. تحديث النصوص
        let signalPercent = Math.floor(Math.max(0, 1 - (dist / 800)) * 100);
        document.getElementById('status-txt').innerText = `SIGNAL STRENGTH: ${signalPercent}%`;
        document.getElementById('status-txt').style.color = scopeColor;
    }

    // --- رسم الشهادة ---
    function drawCertificate() {
        const c = document.getElementById('cert-canvas');
        const cx = c.getContext('2d');
        
        // خلفية
        cx.fillStyle = '#0e0e0e';
        cx.fillRect(0,0,800,600);
        
        // إطار
        cx.strokeStyle = '#F4E4BC';
        cx.lineWidth = 10;
        cx.strokeRect(20,20,760,560);
        
        // نصوص
        cx.textAlign = 'center';
        cx.fillStyle = '#F4E4BC';
        cx.font = '40px Arial';
        cx.fillText('CERTIFICATE OF COMPLETION', 400, 100);
        
        cx.fillStyle = 'white';
        cx.font = '30px Arial';
        cx.fillText('ATHAR EXHIBITION 2026', 400, 180);
        
        cx.fillStyle = '#ccc';
        cx.font = '20px Arial';
        cx.fillText('The player has successfully found', 400, 300);
        cx.fillText('ALL HIDDEN SIGNALS', 400, 340);
        
        cx.fillStyle = '#F4E4BC';
        cx.font = 'bold 30px Arial';
        cx.fillText('"Ethics is the Compass of AI"', 400, 450);
        
        cx.fillStyle = '#555';
        cx.font = '15px Arial';
        cx.fillText('Created by Eng. Alyaa', 400, 550);
    }

    // تحميل الشهادة
    window.downloadCert = function() {
        const link = document.createElement('a');
        link.download = 'Athar_Certificate.png';
        link.href = document.getElementById('cert-canvas').toDataURL();
        link.click();
    }

    // تعديل حجم الكانفاس عند تغيير حجم النافذة
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });

</script>
</body>
</html>
"""

# عرض اللعبة داخل Streamlit
components.html(game_html, height=800, scrolling=False)
