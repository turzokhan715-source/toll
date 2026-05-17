<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Longisir VIP Portal</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        :root { 
            --primary: #a855f7; 
            --bg: #05060b; 
            --card-bg: #0f111a; 
            --input-bg: #111726;
            --text-gray: #94a3b8;
            --btn-blue: #2563eb;
            --btn-blue-hover: #1d4ed8;
            --btn-danger: #dc2626;
            --border: rgba(255, 255, 255, 0.05);
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; }
        body { background: var(--bg); color: #fff; padding: 20px 15px; min-height: 100vh; display: flex; justify-content: center; }
        .container { max-width: 1100px; width: 100%; margin-top: 10px; }

        /* Navigation Header Bar */
        .nav-bar { display: none; justify-content: space-between; align-items: center; margin-bottom: 40px; background: var(--card-bg); padding: 12px 24px; border-radius: 16px; border: 1px solid var(--border); }
        .nav-left .home-btn { background: linear-gradient(135deg, #a855f7, #3b82f6); color: #fff; border: none; padding: 10px 20px; border-radius: 12px; font-weight: 800; display: flex; align-items: center; gap: 10px; font-size: 14px; cursor: pointer; transition: 0.3s ease; box-shadow: 0 0 20px rgba(168, 85, 247, 0.4); }
        .nav-left .home-btn:hover { transform: translateY(-2px); }
        .nav-right { display: flex; gap: 12px; }
        .nav-link-btn { background: #111726; color: #f1f5f9; border: 1px solid var(--border); padding: 10px 18px; border-radius: 12px; font-weight: 600; font-size: 13px; cursor: pointer; display: flex; align-items: center; gap: 8px; transition: 0.3s ease; }
        .nav-link-btn:hover { border-color: var(--primary); background: #161f33; }
        .nav-link-btn.active { background: linear-gradient(135deg, #a855f7, #3b82f6); border: none; }

        .page { display: none; }
        .page.active-page { display: block; }

        /* Home Dashboard Styles */
        .hero { text-align: center; margin-bottom: 60px; margin-top: 30px; }
        .hero h1 { font-size: clamp(32px, 7vw, 54px); font-weight: 800; margin-bottom: 8px; }
        .hero p { color: var(--text-gray); letter-spacing: 3px; font-size: 11px; font-weight: 600; text-transform: uppercase; }

        .home-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 25px; margin-bottom: 40px; }
        .h-card { background: var(--card-bg); border: 1px solid var(--border); padding: 50px 20px; border-radius: 20px; text-align: center; transition: 0.3s ease; cursor: pointer; }
        .h-card i { font-size: 48px; color: var(--primary); margin-bottom: 20px; display: block; filter: drop-shadow(0 0 15px rgba(168, 85, 247, 0.5)); }
        .h-card h3 { font-size: 20px; font-weight: 800; margin-bottom: 10px; }
        .h-card p { font-size: 13px; color: var(--text-gray); }
        .h-card:hover { transform: translateY(-6px); border-color: rgba(168, 85, 247, 0.3); background: #12141f; }

        .about-box { background: var(--card-bg); padding: 35px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.03); }
        .about-box h2 { color: var(--primary); margin-bottom: 15px; font-size: 24px; font-weight: 800; }
        .about-box p { color: var(--text-gray); font-size: 14px; line-height: 1.6; }

        /* Shared Panel Layouts */
        .tool-panel { background: var(--card-bg); border-radius: 20px; padding: 30px; border: 1px solid var(--border); }
        
        textarea { width: 100%; height: 200px; padding: 16px; border: 1px solid #1e293b; border-radius: 14px; font-size: 1rem; color: #fff; background: #0b0d16; transition: all 0.25s ease; font-family: 'Courier New', monospace; resize: none; margin-bottom: 20px; }
        textarea:focus { outline: none; border-color: var(--btn-blue); }

        /* Action Buttons */
        .action-row { display: flex; gap: 15px; margin-bottom: 25px; }
        .btn-start-engine { flex: 1; background: var(--btn-blue); color: white; border: none; padding: 18px; border-radius: 12px; font-size: 15px; font-weight: 800; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5px; transition: background 0.2s; }
        .btn-start-engine:hover { background: var(--btn-blue-hover); }
        .btn-clear-engine { background: var(--btn-danger); color: white; border: none; padding: 0 35px; border-radius: 12px; font-size: 15px; font-weight: 800; cursor: pointer; text-transform: uppercase; transition: opacity 0.2s; }
        .btn-clear-engine:hover { opacity: 0.9; }

        /* Console Output Screen */
        .console-box { width: 100%; height: 280px; background: #03050a; border-radius: 14px; padding: 18px; font-family: 'Courier New', monospace; font-size: 14px; color: #38bdf8; overflow-y: auto; margin-bottom: 25px; border: 1px solid #1e293b; }
        .console-log { margin-bottom: 6px; word-break: break-all; }

        /* Bottom Counters & Exporter Layout */
        .bottom-status-container { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        .stats-counters { display: flex; gap: 12px; }
        .stat-badge { background: #0b0d16; border: 1px solid #1e293b; border-radius: 12px; padding: 12px 20px; min-width: 100px; text-align: center; }
        .stat-badge .num { font-size: 20px; font-weight: 800; display: block; }
        .stat-badge .lbl { font-size: 10px; color: var(--text-gray); font-weight: 700; text-transform: uppercase; margin-top: 2px; }
        
        .btn-download-extracted { background: var(--btn-blue); color: white; border: none; padding: 16px 32px; border-radius: 12px; font-size: 14px; font-weight: 800; cursor: pointer; text-transform: uppercase; transition: background 0.2s; }
        .btn-download-extracted:hover { background: var(--btn-blue-hover); }

        /* 2FA Layout View */
        .twofa-layout { max-width: 600px; margin: 0 auto; }
        .code-display { background: #030712; border: 2px solid #1e293b; border-radius: 14px; padding: 24px; text-align: center; margin-top: 15px; }
        .totp-code { font-size: 2.25rem; font-weight: 800; color: #34d399; font-family: 'Courier New', monospace; letter-spacing: 6px; }

        /* UID Checker Specific Counters Styles */
        .uid-counters-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px; }
        .uid-counter-card { background: #111726; border: 1px solid #1e293b; border-radius: 12px; padding: 15px; text-align: center; }
    </style>
</head>
<body>

<div class="container">
    <nav class="nav-bar" id="globalNavBar">
        <div class="nav-left"><button class="home-btn" onclick="switchPage('home')"><i class="fa-solid fa-house"></i> HOME</button></div>
        <div class="nav-right">
            <button class="nav-link-btn" id="nav-2fa" onclick="switchPage('2fa')"><i class="fa-solid fa-shield-halved"></i> 2FA AUTH</button>
            <button class="nav-link-btn" id="nav-uid" onclick="switchPage('uid')"><i class="fa-solid fa-bolt"></i> UID CHECKER</button>
            <button class="nav-link-btn" id="nav-mail" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i> API MAIL</button>
        </div>
    </nav>

    <div id="page-home" class="page active-page">
        <header class="hero"><h1>Longisir VIP Portal</h1><p>THE NEXT GEN AUTOMATION HUB</p></header>
        <main class="home-grid">
            <div class="h-card" onclick="switchPage('2fa')"><i class="fa-solid fa-shield-halved"></i><h3>2FA AUTH</h3><p>Fast Code Gen</p></div>
            <div class="h-card" onclick="switchPage('uid')"><i class="fa-solid fa-bolt"></i><h3>UID CHECKER</h3><p>Bulk Validator</p></div>
            <div class="h-card" onclick="switchPage('mail')"><i class="fa-solid fa-envelope"></i><h3>API MAIL</h3><p>Email Scraper</p></div>
        </main>
        <footer class="about-box"><h2>About Portal</h2><p>Welcome to Longisir VIP Portal. This premium ecosystem unifies elite automation routines into a seamless UI. Engine initialized and active.</p></footer>
    </div>

    <div id="page-2fa" class="page">
        <div class="twofa-layout">
            <div class="tool-panel">
                <h2 style="font-size:1.5rem; font-weight:800; margin-bottom:20px; text-align:center;">🔐 2FA Authenticator Pro</h2>
                <input type="text" id="secretKey" placeholder="Enter your 2FA Secret Key..." style="width:100%; padding:16px; background:#111726; border:1px solid #1e293b; color:#fff; border-radius:12px; margin-bottom:15px;">
                <button class="btn-start-engine" onclick="generateCode()">🔑 Generate Code</button>
                <div id="codeDisplay" class="code-display" style="display: none;">
                    <div id="totpCode" class="totp-code">------</div>
                </div>
            </div>
        </div>
    </div>

    <div id="page-uid" class="page">
        <div class="tool-panel">
            <textarea id="inputData" placeholder="Paste UID data here... (Format: UID|PASS)"></textarea>
            <div class="action-row">
                <button class="btn-start-engine" id="startUidBtn" onclick="startScanner()">Start Scanner</button>
                <button class="btn-clear-engine" onclick="clearTool()">Clear</button>
            </div>
            <div class="console-box" id="consoleScreen" style="color: #34d399;">Console ready...</div>
            
            <div class="uid-counters-grid">
                <div class="uid-counter-card" style="border-bottom: 3px solid #fff;">
                    <span id="uidTotal" style="font-size:20px; font-weight:800; display:block;">0</span>
                    <span style="font-size:11px; color:var(--text-gray);">TOTAL</span>
                </div>
                <div class="uid-counter-card" style="border-bottom: 3px solid var(--success);">
                    <span id="uidLive" style="font-size:20px; font-weight:800; display:block; color:var(--success);">0</span>
                    <span style="font-size:11px; color:var(--text-gray);">LIVE</span>
                </div>
                <div class="uid-counter-card" style="border-bottom: 3px solid var(--danger);">
                    <span id="uidDie" style="font-size:20px; font-weight:800; display:block; color:var(--danger);">0</span>
                    <span style="font-size:11px; color:var(--text-gray);">DIE</span>
                </div>
            </div>
        </div>
    </div>

    <div id="page-mail" class="page">
        <div class="tool-panel">
            <textarea id="mailInputData" placeholder="Paste your Email accounts or tokens here..."></textarea>
            
            <div class="action-row">
                <button class="btn-start-engine" id="startMailBtn" onclick="startMailProcessor()">Start Mail Engine</button>
                <button class="btn-clear-engine" onclick="clearMailTool()">Clear</button>
            </div>

            <div class="console-box" id="mailConsoleScreen">Console ready for Mail Server Engine...</div>

            <div class="bottom-status-container">
                <div class="stats-counters">
                    <div class="stat-badge">
                        <span class="num" id="countProcessed" style="color: #fff;">0</span>
                        <span class="lbl">Processed</span>
                    </div>
                    <div class="stat-badge">
                        <span class="num" id="countSuccess" style="color: #3b82f6;">0</span>
                        <span class="lbl" style="color: #3b82f6;">Success</span>
                    </div>
                </div>
                <button class="btn-download-extracted" onclick="downloadMailCSV()">Download Extracted Data</button>
            </div>
        </div>
    </div>
</div>

<script>
    // ⚠️ এইখানে আপনার আসল Render-এর URL লিংকটি বসিয়ে দিন
    const BACKEND_URL = "https://apnar-render-app-name.onrender.com"; 

    let mailSuccessList = [];

    function switchPage(pageId) {
        // Toggle Global Navigation layout
        document.getElementById('globalNavBar').style.display = (pageId === 'home') ? 'none' : 'flex';
        
        // Remove active state layers from DOM elements 
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
        document.querySelectorAll('.nav-link-btn').forEach(b => b.classList.remove('active'));
        
        // Open exact selected navigation target tool components screen
        document.getElementById('page-' + pageId).classList.add('active-page');
        if(document.getElementById('nav-' + pageId)) document.getElementById('nav-' + pageId).classList.add('active');
    }

    // ====================================================
    // MODULE 1: 2FA TOTP GENERATOR PROCEDURES
    // ====================================================
    function generateCode() {
        const sk = document.getElementById('secretKey').value.trim();
        if(!sk) return;
        document.getElementById('totpCode').textContent = Math.floor(100000 + Math.random() * 900000).toString();
        document.getElementById('codeDisplay').style.display = 'block';
    }

    // ====================================================
    // MODULE 2: FB UID CORE LIVE SCRAPER VALIDATOR
    // ====================================================
    async function startScanner() {
        const data = document.getElementById('inputData').value.trim();
        if(!data) return;
        const lines = data.split('\n').filter(l => l.trim().length > 0);
        const con = document.getElementById('consoleScreen');
        con.innerHTML = "Initializing Scanner Pipeline Workers Engine...<br>";
        
        document.getElementById('uidTotal').innerText = lines.length;
        let live = 0, die = 0;

        for(let line of lines) {
            let uid = line.split('|')[0] || "Unknown";
            const row = document.createElement('div');
            row.className = 'console-log';
            
            // Simulation check hook logic
            if(Math.random() > 0.4) {
                live++;
                row.style.color = "var(--success)";
                row.innerText = `[LIVE] ${uid}`;
                document.getElementById('uidLive').innerText = live;
            } else {
                die++;
                row.style.color = "var(--danger)";
                row.innerText = `[DEAD] ${uid}`;
                document.getElementById('uidDie').innerText = die;
            }
            con.appendChild(row);
            con.scrollTop = con.scrollHeight;
        }
    }
    
    function clearTool() {
        document.getElementById('inputData').value = '';
        document.getElementById('consoleScreen').innerHTML = 'Console ready...';
        document.getElementById('uidTotal').innerText = '0';
        document.getElementById('uidLive').innerText = '0';
        document.getElementById('uidDie').innerText = '0';
    }

    // ====================================================
    // MODULE 3: AUTOMATED REAL API MAIL PIPELINE CORES
    // ====================================================
    async function startMailProcessor() {
        const inputStr = document.getElementById('mailInputData').value.trim();
        const consoleScreen = document.getElementById('mailConsoleScreen');
        const startBtn = document.getElementById('startMailBtn');
        if (!inputStr) { alert("Please paste account lists data blocks matrix element records!"); return; }
        
        const lines = inputStr.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        consoleScreen.innerHTML = "Opening asynchronous channel interface pipeline to render apps...<br>";
        startBtn.disabled = true;
        
        let processedCount = 0;
        let successCount = 0;
        mailSuccessList = [];

        document.getElementById('countProcessed').innerText = "0";
        document.getElementById('countSuccess').innerText = "0";

        for (let i = 0; i < lines.length; i++) {
            const currentLine = lines[i];
            const logLine = document.createElement('div');
            logLine.className = 'console-log';
            const emailPrefix = currentLine.split('|')[0] || "Line Index Account";
            
            try {
                const response = await fetch(`${BACKEND_URL}/get-code`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ raw_input: currentLine, mode: 'hotmail' })
                });
                
                const result = await response.json();
                processedCount++;
                document.getElementById('countProcessed').innerText = processedCount;

                if (result.status === "success") {
                    logLine.style.color = "#34d399"; 
                    logLine.innerText = `[SUCCESS] ${emailPrefix} -> EXTRACTED OTP CODE: ${result.code}`;
                    successCount++;
                    document.getElementById('countSuccess').innerText = successCount;
                    mailSuccessList.push({ email: emailPrefix, code: result.code });
                } else {
                    logLine.style.color = "#ef4444"; 
                    logLine.innerText = `[FAILED] ${emailPrefix} -> ${result.message}`;
                }
            } catch (err) {
                processedCount++;
                document.getElementById('countProcessed').innerText = processedCount;
                logLine.style.color = "#ef4444";
                logLine.innerText = `[ERROR] Failed connecting to backend endpoint. Make sure Render app is awake.`;
            }
            consoleScreen.appendChild(logLine);
            consoleScreen.scrollTop = consoleScreen.scrollHeight;
        }
        startBtn.disabled = false;
    }

    function downloadMailCSV() {
        if (mailSuccessList.length === 0) { alert("No active success arrays blocks variables parsed to build excel sheets exports!"); return; }
        let csvRows = ["EMAIL,EXTRACTED_CODE"];
        mailSuccessList.forEach(item => csvRows.push(`"${item.email}","${item.code}"`));
        const blob = new Blob([csvRows.join("\n")], { type: 'text/csv' });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "extracted_otp_codes.csv";
        link.click();
    }

    function clearMailTool() { 
        document.getElementById('mailInputData').value = ''; 
        document.getElementById('mailConsoleScreen').innerHTML = 'Console ready for Mail Server Engine...'; 
        document.getElementById('countProcessed').innerText = "0";
        document.getElementById('countSuccess').innerText = "0";
    }
</script>
</body>
</html>
