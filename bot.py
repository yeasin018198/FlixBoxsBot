# bot.py

import asyncio
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import random
import re
from string import Template

try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyrogram import Client
import config

# ১. সাধারণ (Free) ইউজারদের জন্য মিনি অ্যাপ ডাউনলোড টেমপ্লেট (নতুন নিওন-গ্লোয়িং ড্যাশবোর্ড সহ)
HTML_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download Movie</title>
    <!-- টেলিগ্রামের অফিশিয়াল ওয়েব অ্যাপ স্ক্রিপ্ট -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            background-color: #0b0c10;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            text-align: center;
            padding: 15px;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 95vh;
        }
        
        /* আরজিবি পালসিং বর্ডার অ্যানিমেশন */
        @keyframes borderGlow {
            0% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 15px rgba(255, 0, 85, 0.2); }
            50% { border-color: rgba(0, 240, 255, 0.4); box-shadow: 0 0 15px rgba(0, 240, 255, 0.2); }
            100% { border-color: rgba(255, 0, 85, 0.4); box-shadow: 0 0 15px rgba(255, 0, 85, 0.2); }
        }
        
        .container {
            width: 100%;
            max-width: 400px;
            background: rgba(30, 30, 38, 0.65);
            padding: 30px 20px;
            border-radius: 24px;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 0, 85, 0.4);
            animation: borderGlow 6s infinite ease-in-out;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        }
        
        h2 { 
            color: #ff0055; 
            margin: 0 0 15px 0; 
            font-size: 26px; 
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 0 0 12px rgba(255, 0, 85, 0.4);
        }
        
        /* সম্পূর্ণ রি-ডিজাইনকৃত প্রিমিয়াম ড্যাশবোর্ড কার্ড */
        .info-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.01));
            border: 1px solid rgba(0, 240, 255, 0.15);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 20px;
            text-align: left;
            box-shadow: inset 0 0 15px rgba(0, 240, 255, 0.05);
        }
        .info-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-size: 13px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            padding-bottom: 8px;
        }
        .info-row:last-child { 
            margin-bottom: 0; 
            border-bottom: none;
            padding-bottom: 0;
        }
        .info-label { 
            color: #9ca3af; 
            display: flex;
            align-items: center;
        }
        
        /* লাইভ স্ট্যাটাস ব্লিংকিং ডট */
        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-dot.blue { background-color: #00f0ff; box-shadow: 0 0 8px #00f0ff; }
        .status-dot.green { background-color: #00ff88; box-shadow: 0 0 8px #00ff88; }
        .status-dot.purple { background-color: #bd00ff; box-shadow: 0 0 8px #bd00ff; }
        .status-dot.safe { background-color: #00ffaa; box-shadow: 0 0 8px #00ffaa; }
        
        .info-value { color: #ffffff; font-weight: 700; font-family: monospace; font-size: 14px; }
        .neon-green { color: #00ff88; text-shadow: 0 0 8px rgba(0, 255, 136, 0.3); }
        .neon-blue { color: #00f0ff; text-shadow: 0 0 8px rgba(0, 240, 255, 0.3); }
        .neon-purple { color: #bd00ff; text-shadow: 0 0 8px rgba(189, 0, 255, 0.3); }
        
        .step-card {
            background: rgba(255, 255, 255, 0.04);
            padding: 14px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 13px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #d1d5db;
            line-height: 1.4;
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 16px 0;
            margin: 15px 0;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .btn-ad {
            background: linear-gradient(135deg, #ff0055, #b3003b);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 0, 85, 0.4);
        }
        .btn-ad:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 0, 85, 0.6);
        }
        .btn-download {
            background-color: #1f2937;
            color: #4b5563;
            border: 1px solid #374151;
            pointer-events: none;
        }
        .btn-download.active {
            background: linear-gradient(135deg, #00ff88, #009951);
            color: #000000;
            font-weight: 800;
            pointer-events: auto;
            box-shadow: 0 0 25px rgba(0, 255, 136, 0.7);
            border: none;
        }
        
        .success-badge {
            display: none;
            background: rgba(0, 255, 136, 0.08);
            color: #00ff88;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 14px;
            border: 1px solid rgba(0, 255, 136, 0.2);
            margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.1);
        }
        
        .support-note {
            font-size: 11px;
            color: #6b7280;
            margin-top: 20px;
            line-height: 1.4;
            text-align: center;
        }
        
        #loader {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 70vh;
        }
        .loader-title {
            font-size: 18px;
            font-weight: bold;
            color: #00f0ff;
            text-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
            margin-bottom: 15px;
        }
        .progress-container {
            width: 80%;
            height: 8px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .progress-bar {
            width: 0%;
            height: 100%;
            background: linear-gradient(90deg, #ff0055, #00f0ff);
            box-shadow: 0 0 10px #00f0ff;
            transition: width 0.05s ease-out;
        }
        .loader-percent {
            font-size: 14px;
            margin-top: 10px;
            color: #9ca3af;
        }
    </style>
    <script>
        let tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();

        window.addEventListener("DOMContentLoaded", () => {
            let percent = 0;
            let bar = document.getElementById("bar");
            let pText = document.getElementById("percent-text");
            
            let interval = setInterval(() => {
                percent += 5;
                if (percent <= 100) {
                    bar.style.width = percent + "%";
                    pText.innerText = percent + "% Completed";
                } else {
                    clearInterval(interval);
                    document.getElementById("loader").style.display = "none";
                    document.getElementById("app-content").style.display = "block";
                }
            }, 70);
        });

        function unlockDownload() {
            window.open("$ad_link", "_blank");
            
            document.getElementById("btn-ad").style.display = "none";
            document.getElementById("success-badge").style.display = "block";
            
            var downloadBtn = document.getElementById("download-btn");
            downloadBtn.classList.add("active");
            downloadBtn.innerText = "⚡️ Get Movie File";
            document.getElementById("step-text").innerText = "লিংকটি সচল হয়েছে! নিচের বাটনে চাপ দিন।";
        }

        function getMovie() {
            tg.openTelegramLink("https://t.me/$bot_username?start=get_$file_db_id");
            setTimeout(function() {
                tg.close();
            }, 500);
        }
    </script>
</head>
<body>
    <div id="loader">
        <div class="loader-title">🔍 Generating Secure CDN Link...</div>
        <div class="progress-container">
            <div id="bar" class="progress-bar"></div>
        </div>
        <div id="percent-text" class="loader-percent">0% Completed</div>
    </div>

    <div id="app-content" class="container" style="display: none;">
        <h2>CTG PREMIUM SEARCH</h2>
        
        <div class="info-card">
            <div class="info-row">
                <span class="info-label"><span class="status-dot blue"></span> 📊 Database Inventory:</span>
                <span class="info-value neon-blue">$total_files+ Movies</span>
            </div>
            <div class="info-row">
                <span class="info-label"><span class="status-dot green"></span> 👥 Connected Users:</span>
                <span class="info-value neon-green">$total_users+ Online</span>
            </div>
            <div class="info-row">
                <span class="info-label"><span class="status-dot purple"></span> 💾 Storage Used:</span>
                <span class="info-value neon-purple">$used_storage</span>
            </div>
            <div class="info-row">
                <span class="info-label"><span class="status-dot safe"></span> 📉 Free Buffer Space:</span>
                <span class="info-value neon-green">$free_storage</span>
            </div>
        </div>
        
        <div id="step-text" class="step-card">
            ধাপ ১: প্রথমে নিচের লাল বাটনে ক্লিক করে বিজ্ঞাপন পেজটি লোড করুন এবং ডাউনলোড লিংকটি আনলক করুন।
        </div>
        
        <div id="success-badge" class="success-badge">✅ Link Unlocked successfully!</div>
        
        <button id="btn-ad" class="btn btn-ad" onclick="unlockDownload()">🔓 Unlock Download Link</button>
        <button id="download-btn" class="btn btn-download" onclick="getMovie()">🔒 Locked</button>
        
        <div class="support-note">
            বটের হাই-স্পিড সার্ভার খরচ চালাতে এবং আপনাকে সম্পূর্ণ ফ্রিতে সেবা দিতে আমাদের একটি ছোট্ট বিজ্ঞাপন দেখতে হয়। সহযোগিতার জন্য ধন্যবাদ!
        </div>
    </div>
</body>
</html>
""")

# ২. প্রিমিয়াম (VIP) ইউজারদের জন্য ড্যাশবোর্ড
HTML_VIP_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP Access Control Panel</title>
    <!-- টেলিগ্রামের অফিশিয়াল ওয়েব অ্যাপ স্ক্রিপ্ট -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            background-color: #0b0c10;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            text-align: center;
            padding: 15px;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 95vh;
        }
        
        @keyframes vipGlow {
            0% { border-color: rgba(0, 255, 136, 0.4); box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); }
            50% { border-color: rgba(0, 240, 255, 0.4); box-shadow: 0 0 15px rgba(0, 240, 255, 0.2); }
            100% { border-color: rgba(0, 255, 136, 0.4); box-shadow: 0 0 15px rgba(0, 255, 136, 0.2); }
        }
        
        .container {
            width: 100%;
            max-width: 400px;
            background: rgba(30, 30, 38, 0.7);
            padding: 30px 20px;
            border-radius: 24px;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(0, 255, 136, 0.5);
            animation: vipGlow 6s infinite ease-in-out;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
        }
        
        .vip-badge {
            display: inline-block;
            background: rgba(0, 255, 136, 0.1);
            color: #00ff88;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 800;
            border: 1px solid rgba(0, 255, 136, 0.3);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 20px;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
        }
        
        h2 { 
            color: #00ff88; 
            margin: 0 0 15px 0; 
            font-size: 24px; 
            font-weight: 800;
            text-transform: uppercase;
            text-shadow: 0 0 12px rgba(0, 255, 136, 0.3);
        }
        
        .info-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 25px;
            text-align: left;
        }
        .info-title {
            font-weight: bold;
            color: #00f0ff;
            word-break: break-all;
            margin-bottom: 8px;
            font-size: 14px;
            line-height: 1.4;
        }
        .info-size {
            font-size: 12px;
            color: #9ca3af;
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 16px 0;
            margin: 15px 0;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
        }
        .btn-stream {
            background: linear-gradient(135deg, #00f0ff, #0072ff);
            box-shadow: 0 4px 15px rgba(0, 240, 255, 0.4);
        }
        .btn-stream:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 240, 255, 0.6);
        }
        .btn-download {
            background: linear-gradient(135deg, #00ff88, #009951);
            color: #000000;
            font-weight: 800;
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.4);
        }
        .btn-download:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 255, 136, 0.6);
        }
        .btn-close {
            background: #1f2937;
            border: 1px solid #374151;
            color: #9ca3af;
        }
        .btn-close:hover {
            background: #374151;
            color: white;
        }
    </style>
    <script>
        let tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();

        function playOnline() {
            window.location.href = "/play?id=$file_db_id";
        }

        function getMovie() {
            tg.openTelegramLink("https://t.me/$bot_username?start=get_$file_db_id");
            setTimeout(function() {
                tg.close();
            }, 500);
        }
        
        function closeApp() {
            tg.close();
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="vip-badge">👑 VIP Premium Active</div>
        <h2>CTG VIP MOVIE PANEL</h2>
        
        <div class="info-card">
            <div class="info-title">🎬 $file_name</div>
            <div class="info-size">💾 Size: <b>$file_size MB</b></div>
        </div>
        
        <button class="btn btn-stream" onclick="playOnline()">🍿 Watch Online / Stream</button>
        <button class="btn btn-download" onclick="getMovie()">⚡️ Get File in Telegram</button>
        <button class="btn btn-close" onclick="closeApp()">🛑 Close Panel</button>
    </div>
</body>
</html>
""")

# ৩. প্রিমিয়াম স্ট্রিমিং প্লেয়ার ওয়েব পেজ টেমপ্লেট (সংশোধিত এরর-ফ্রি ডিজাইন)
HTML_STREAM_TEMPLATE = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIP SEARCH BOT - Player</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { background-color: #0b0f19; color: #ffffff; font-family: sans-serif; padding: 10px; margin: 0; }
        .container { width: 100%; max-width: 500px; margin: auto; }
        
        .header-info { display: flex; justify-content: space-between; padding: 10px 5px; font-weight: bold; font-size: 13px; text-transform: uppercase; }
        .size-green { color: #4ade80; }
        .time-white { color: #fff; }

        .player-box { position: relative; width: 100%; background: #000; border-radius: 12px; overflow: hidden; margin-bottom: 15px; aspect-ratio: 16/9; border: 1px solid #1e293b; }
        video { width: 100%; height: 100%; }
        #brightness-layer { position: absolute; top:0; left:0; width:100%; height:100%; background:black; opacity:0; pointer-events:none; }

        .title-display { font-weight: bold; font-size: 14px; color: #00f0ff; padding: 8px; margin-bottom: 15px; border-left: 4px solid #e91e63; word-break: break-all; background: rgba(255,255,255,0.03); }
        
        .custom-controls { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 15px; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; }
        .ctrl-box { display: flex; flex-direction: column; align-items: center; font-size: 10px; color: #94a3b8; }
        .ctrl-box select, .ctrl-box input { background: #1e293b; color: #fff; border: 1px solid #334155; border-radius: 5px; width: 100%; padding: 4px; margin-top: 5px; font-size: 11px; }

        .action-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
        .btn-act { padding: 16px; border-radius: 50px; text-decoration: none; color: white; font-weight: bold; font-size: 13px; text-align: center; }
        .btn-red { background: #e11d48; }
        .btn-blue { background: #2563eb; }

        .grid-apps { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
        .btn-app { background: #1c2230; color: #fff; padding: 14px; border-radius: 35px; text-decoration: none; font-size: 12px; font-weight: bold; display: flex; align-items: center; justify-content: center; gap: 8px; border: 1px solid #2a3245; cursor: pointer; }
        
        .small-apps { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 15px; }
        .btn-mini { padding: 12px; font-size: 10px; border-radius: 12px; }

        .btn-get-file { background: #00ff88; color: #000; width: 100%; padding: 15px; border-radius: 12px; font-weight: 900; border: none; margin-bottom: 10px; cursor: pointer; text-transform: uppercase; }
        .btn-close-p { background: #1e293b; width: 100%; padding: 13px; border-radius: 12px; color: #ef4444; border: none; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header-info">
            <span class="size-green">SIZE: $file_size MB</span>
            <span class="time-white" id="live-timer">TIME: 00:00:00 PM</span>
        </div>

        <div class="player-box">
            <div id="brightness-layer"></div>
            <video id="p-main" controls poster="https://github.com/NBBotz/Images/blob/main/Lucia-Filter-Bot.jpeg?raw=true">
                <source src="$stream_url" type="video/mp4">
            </video>
        </div>

        <div class="title-display">🎬 $file_name</div>

        <div class="custom-controls">
            <div class="ctrl-box">
                <span>QUALITY</span>
                <select id="q-switch">
                    <option>Auto (High)</option>
                    <option>1080p</option>
                    <option>720p</option>
                </select>
            </div>
            <div class="ctrl-box">
                <span>BRIGHTNESS</span>
                <input type="range" min="0" max="0.7" step="0.1" value="0" oninput="document.getElementById('brightness-layer').style.opacity = this.value">
            </div>
            <div class="ctrl-box">
                <span>SPEED</span>
                <select onchange="document.getElementById('p-main').playbackRate = this.value">
                    <option value="1">1.0x</option>
                    <option value="1.5">1.5x</option>
                    <option value="2">2.0x</option>
                </select>
            </div>
        </div>

        <div class="action-btns">
            <!-- সরাসরি ডাউনলোডের জন্য dl=1 প্যারামিটার ফিক্সড -->
            <a href="$stream_url&dl=1" download class="btn-act btn-red">⚡ DOWNLOAD</a>
            <a href="$stream_url" class="btn-act btn-blue">📂 WATCH ONLINE</a>
        </div>

        <div class="grid-apps">
            <div onclick="openApp('intent:$stream_url#Intent;package=org.videolan.vlc;type=video/*;end')" class="btn-app"><span style="color:orange">🧡</span> VLC PLAYER</div>
            <div onclick="openApp('intent:$stream_url#Intent;package=com.mxtech.videoplayer.ad;S.title=$file_name;end')" class="btn-app"><span style="color:#3b82f6">💙</span> MX PLAYER</div>
            <div onclick="openApp('intent:$stream_url#Intent;package=com.player.videoplayer;S.title=$file_name;end')" class="btn-app"><span style="color:#22c55e">💚</span> PLAYIT</div>
            <div onclick="openApp('intent:$stream_url#Intent;action=android.intent.action.VIEW;type=video/*;end')" class="btn-app"><span style="color:#facc15">📺</span> SYSTEM</div>
        </div>

        <div class="small-apps">
            <div onclick="openApp('intent:$stream_url#Intent;package=com.kmplayer;end')" class="btn-app btn-mini">🎬 KM PLAYER</div>
            <div onclick="openApp('intent:$stream_url#Intent;package=org.xbmc.kodi;end')" class="btn-app btn-mini">🏢 KODI</div>
            <div onclick="openApp('nplayer-$stream_url')" class="btn-app btn-mini">📱 NPLAYER</div>
        </div>

        <button class="btn-get-file" onclick="tg.openTelegramLink('https://t.me/$bot_username?start=get_$file_db_id')">⚡️ GET FILE IN TELEGRAM</button>
        <button class="btn-close-p" onclick="tg.close()">🛑 CLOSE PLAYER</button>
    </div>

    <script>
        let tg = window.Telegram.WebApp;
        tg.ready(); tg.expand();

        // এরর মুক্ত উপায়ে এক্সটার্নাল প্লেয়ার ওপেন করার ফাংশন
        function openApp(url) {
            tg.openLink(url);
        }

        // রিয়েল টাইম ক্লক
        function clock() {
            const now = new Date();
            document.getElementById('live-timer').innerText = "TIME: " + now.toLocaleTimeString();
        }
        setInterval(clock, 1000); clock();

        // ভিডিও ফুল স্ক্রিন হ্যান্ডলার
        document.getElementById('p-main').addEventListener('dblclick', function() {
            if (this.requestFullscreen) this.requestFullscreen();
            else if (this.webkitRequestFullscreen) this.webkitRequestFullscreen();
        });
    </script>
</body>
</html>
""")

class DummyWebServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        # ১. মিনি অ্যাপ ডাউনলোড বাটন পেইজ (প্রিমিয়াম/ফ্রি কন্ডিশনাল লজিক সহ)
        if parsed_url.path == "/download":
            query_params = parse_qs(parsed_url.query)
            file_db_id = query_params.get("id", [""])[0]
            user_id_str = query_params.get("user_id", [""])[0]
            
            user_id = 0
            if user_id_str.isdigit():
                user_id = int(user_id_str)
                
            # প্রিমিয়াম ভেরিফিকেশন চেক
            is_vip = False
            if app.loop and app.loop.is_running() and user_id > 0:
                try:
                    from database import is_premium_user
                    future = asyncio.run_coroutine_threadsafe(is_premium_user(user_id), app.loop)
                    is_vip = future.result(timeout=2)
                except Exception as e:
                    print(f"Failed to verify VIP status in server: {e}")
            
            # ডাটাবেজ থেকে মুভির রিয়েল মেটাডেটা সংগ্রহ
            file_data = None
            if app.loop and app.loop.is_running():
                try:
                    from database import get_file_by_db_id
                    future = asyncio.run_coroutine_threadsafe(get_file_by_db_id(file_db_id), app.loop)
                    file_data = future.result(timeout=2)
                except Exception as e:
                    print(f"Failed to fetch file details: {e}")
            
            if not file_data:
                self.send_error(404, "File Not Found")
                return
                
            file_name = file_data.get("file_name", "Movie File")
            file_size = round(file_data["file_size"] / (1024 * 1024), 2)
            
            # ইউজার প্রিমিয়াম হলে সরাসরি অ্যাড ছাড়া ২-বাটন প্যানেল দেখাবে
            if is_vip:
                response_html = HTML_VIP_TEMPLATE.safe_substitute(
                    file_db_id=file_db_id,
                    bot_username=config.BOT_USERNAME,
                    file_name=file_name,
                    file_size=file_size
                )
            # ইউজার সাধারণ বা ফ্রি হলে পূর্বের নিয়মে লোডার + অ্যাড স্ক্রিন দেখাবে
            else:
                base_ad = random.choice(config.DIRECT_AD_LINKS)
                rand_id = random.randint(100000, 999999)
                rand_click = random.randint(1000000, 9999999)
                
                if "?" in base_ad:
                    ad_link = f"{base_ad}&click_id={rand_click}&sub_id={rand_id}"
                else:
                    ad_link = f"{base_ad}?click_id={rand_click}&sub_id={rand_id}"
                
                # [সংশোধিত ও অপ্টিমাইজড লাইভ স্ট্যাটাস মেকানিজম]
                total_files, total_users, used_storage, free_storage = 0, 0, "0.0 MB", "2.0 GB"
                if app.loop and app.loop.is_running():
                    try:
                        from database import get_detailed_stats
                        future = asyncio.run_coroutine_threadsafe(get_detailed_stats(), app.loop)
                        stats_dict = future.result(timeout=2)
                        
                        total_files = stats_dict.get("total_files", 0)
                        total_users = stats_dict.get("total_users", 0)
                        used_storage = stats_dict.get("used_storage", "0.0 MB")
                        free_storage = stats_dict.get("free_storage", "2.0 GB")
                    except Exception as e:
                        print(f"Failed to fetch live stats: {e}")
                
                response_html = HTML_TEMPLATE.safe_substitute(
                    file_db_id=file_db_id,
                    bot_username=config.BOT_USERNAME,
                    ad_link=ad_link,
                    total_files=f"{total_files:,}",
                    total_users=f"{total_users:,}",
                    used_storage=used_storage,
                    free_storage=free_storage
                )
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_html.encode("utf-8"))

        # ২. প্রিমিয়াম স্ট্রিমিং প্লেয়ার পেইজ
        elif parsed_url.path == "/play":
            query_params = parse_qs(parsed_url.query)
            file_db_id = query_params.get("id", [""])[0]
            
            file_data = None
            if app.loop and app.loop.is_running():
                try:
                    from database import get_file_by_db_id
                    future = asyncio.run_coroutine_threadsafe(get_file_by_db_id(file_db_id), app.loop)
                    file_data = future.result(timeout=2)
                except Exception as e:
                    print(f"Failed to fetch file for streaming: {e}")
            
            if not file_data:
                self.send_error(404, "File Not Found")
                return
            
            raw_url = config.WEB_URL.strip().replace("https://", "").replace("http://", "").rstrip("/")
            stream_url = f"https://{raw_url}/stream?id={file_db_id}"
            file_name = file_data.get("file_name", "Movie File")
            
            # অ্যানড্রয়েড ইন্টেন্ট এবং প্লেয়ারের জটিলতা এড়াতে ফালতু স্পেশাল ক্যারেক্টার ক্লিন করা হলো
            safe_file_name = re.sub(r'[^a-zA-Z0-9\s\.\-_]', '', file_name)
            file_size = round(file_data["file_size"] / (1024 * 1024), 2)
            
            response_html = HTML_STREAM_TEMPLATE.safe_substitute(
                stream_url=stream_url,
                file_db_id=file_db_id,
                bot_username=config.BOT_USERNAME,
                file_name=safe_file_name,
                file_size=file_size
            )
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_html.encode("utf-8"))

        # ৩. প্রিমিয়াম ডাইরেক্ট লাইভ ভিডিও স্ট্রিমিং এন্ডপয়েন্ট (HTTP 206 Partial Content সহ)
        elif parsed_url.path == "/stream":
            query_params = parse_qs(parsed_url.query)
            file_db_id = query_params.get("id", [""])[0]
            is_download = "dl" in query_params # ডাউনলোড ডিটেকশন
            
            file_data = None
            if app.loop and app.loop.is_running():
                try:
                    from database import get_file_by_db_id
                    future = asyncio.run_coroutine_threadsafe(get_file_by_db_id(file_db_id), app.loop)
                    file_data = future.result(timeout=2)
                except Exception as e:
                    print(f"Failed to fetch file metadata for stream: {e}")
            
            if not file_data:
                self.send_error(404, "File Not Found")
                return
            
            file_id = file_data["file_id"]
            file_size = file_data["file_size"]
            
            # HTTP Range রিকোয়েস্ট হ্যান্ডেল করা হচ্ছে (ভিডিওর যেকোনো সেকেন্ডে টেনে টেনে দেখার জন্য)
            range_header = self.headers.get("Range")
            start = 0
            end = file_size - 1
            
            if range_header:
                match = re.match(r"bytes=(\d+)-(\d*)", range_header)
                if match:
                    start = int(match.group(1))
                    if match.group(2):
                        end = int(match.group(2))
            
            if start > end or start >= file_size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{file_size}")
                self.end_headers()
                return
            
            content_len = end - start + 1
            
            self.send_response(206)
            self.send_header("Content-Type", "video/mp4")
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(content_len))
            
            # যদি ডাউনলোড রিকোয়েস্ট হয় তবে attachment হেডার দেওয়া হবে
            disp = "attachment" if is_download else "inline"
            self.send_header("Content-Disposition", f'{disp}; filename="{file_data["file_name"]}"')
            self.end_headers()
            
            # ব্যাকগ্রাউন্ডে পাইরোগ্রাম দিয়ে ফাইল চ্যাঙ্ক রিমোটলি রিড করে স্ট্রিম করা হচ্ছে
            if app.loop and app.loop.is_running():
                async def stream_helper():
                    try:
                        # স্ট্রিম স্পিড বাড়ানোর জন্য ২ এমবি করে চ্যাঙ্ক সাইজ বাড়ানো হলো
                        chunk_size = 2048 * 1024 
                        offset_parts = start // chunk_size
                        bytes_to_skip = start % chunk_size
                        bytes_sent = 0
                        
                        async for chunk in app.stream_media(file_id, offset=offset_parts):
                            if bytes_to_skip > 0:
                                if len(chunk) > bytes_to_skip:
                                    chunk = chunk[bytes_to_skip:]
                                    bytes_to_skip = 0
                                else:
                                    bytes_to_skip -= len(chunk)
                                    continue
                            
                            if bytes_sent + len(chunk) > content_len:
                                chunk = chunk[:content_len - bytes_sent]
                            
                            self.wfile.write(chunk)
                            bytes_sent += len(chunk)
                            
                            if bytes_sent >= content_len:
                                break
                    except Exception:
                        pass
                
                future = asyncio.run_coroutine_threadsafe(stream_helper(), app.loop)
                future.result() 
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"FlixBoxs Movie Bot is running alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), DummyWebServer)
    print(f"ওয়েব সার্ভার এবং মিনি অ্যাপ পোর্ট {port}-এ চালু হয়েছে।")
    server.serve_forever()

t = threading.Thread(target=run_web_server, daemon=True)
t.start()

plugins = dict(root="plugins")

app = Client(
    "movie_search_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=plugins
)

if __name__ == "__main__":
    print("অভিনন্দন! আপনার মুভি বটটি সফলভাবে চালু হয়েছে।")
    app.run()
