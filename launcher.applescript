tell application "Terminal"
    activate
    -- Start Backend in a new window
    do script "echo 'Starting CaliForge AI Backend...'; cd \"/Users/yusufamjherawala/CaliForge AI/backend\" && source venv/bin/activate && uvicorn app.main:app --host 0.0.0.0 --port 8000"
    
    -- Start Frontend in a new window
    do script "echo 'Starting CaliForge AI Frontend...'; cd \"/Users/yusufamjherawala/CaliForge AI/frontend\" && npm run dev"
    
    -- Optional: Give the servers a second to start, then open the browser
    delay 3
    do script "open http://localhost:5173"
end tell
