# Complete Setup and Run Guide

## 📍 Project Location
```
/Users/rishabhporwal/Desktop/podcast
```

---

## 🚀 Quick Start (2 Commands)

### Option 1: Run Web UI (Recommended)
```bash
cd /Users/rishabhporwal/Desktop/podcast
streamlit run app.py
```
**Access at**: http://localhost:8501

### Option 2: Run CLI
```bash
cd /Users/rishabhporwal/Desktop/podcast
python3 src/main.py config.json
```

---

## 📋 Step-by-Step Setup (First Time Only)

### Step 1: Navigate to Project
```bash
cd /Users/rishabhporwal/Desktop/podcast
```

### Step 2: Verify Python Installation
```bash
python3 --version
```
**Required**: Python 3.8 or higher

### Step 3: Install Dependencies (If Not Already Done)
```bash
python3 -m pip install -r requirements.txt
```

This installs:
- `streamlit` - Web UI framework
- `langgraph` - Workflow orchestration
- `anthropic` - Claude API support
- `ollama` - Local LLM support
- `pymupdf` - PDF processing
- `python-dotenv` - Environment configuration

### Step 4: Verify Ollama is Running
```bash
curl http://localhost:11434/api/tags
```

**If not running:**
```bash
ollama serve
```

### Step 5: Check Configuration
```bash
cat .env
```

Should show:
```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

---

## 🖥️ Running the Web UI

### Start the UI
```bash
cd /Users/rishabhporwal/Desktop/podcast
streamlit run app.py
```

**Output you'll see:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Access the UI
Open your browser to: **http://localhost:8501**

### Stop the UI
Press `Ctrl + C` in the terminal

---

## 💻 Running the CLI

### Method 1: Using Default Config
```bash
cd /Users/rishabhporwal/Desktop/podcast
python3 src/main.py config.json
```

### Method 2: Custom Config
```bash
cd /Users/rishabhporwal/Desktop/podcast
python3 src/main.py path/to/your/config.json
```

### What Happens:
1. Logs appear in terminal
2. Progress updates shown
3. Files saved to `example_output/`
   - `podcast_script.md`
   - `verification_report.md`
   - `verification_report.json`

### Where Logs Are Saved:
```
/Users/rishabhporwal/Desktop/podcast/logs/
podcast_generation_YYYYMMDD_HHMMSS.log
```

---

## 📁 Important Files and Locations

### Configuration
```
/Users/rishabhporwal/Desktop/podcast/.env           # LLM settings
/Users/rishabhporwal/Desktop/podcast/config.json    # Section configuration
```

### Source Code
```
/Users/rishabhporwal/Desktop/podcast/src/
├── main.py                      # CLI entry point
├── workflow.py                  # LangGraph workflow
├── agents/
│   ├── pdf_extractor.py         # PDF extraction
│   ├── podcast_generator.py     # Script generation
│   └── verifier.py              # Verification
└── utils/
    ├── llm_provider.py          # Multi-provider support
    ├── logger.py                # Logging configuration
    └── helpers.py               # Utility functions
```

### UI
```
/Users/rishabhporwal/Desktop/podcast/app.py         # Streamlit web interface
```

### Outputs
```
/Users/rishabhporwal/Desktop/podcast/example_output/
├── podcast_script.md
├── verification_report.md
└── verification_report.json
```

### Logs
```
/Users/rishabhporwal/Desktop/podcast/logs/
└── podcast_generation_YYYYMMDD_HHMMSS.log
```

---

## 🎯 Usage Examples

### Example 1: Web UI with Ollama (Default)

1. **Start UI:**
   ```bash
   cd /Users/rishabhporwal/Desktop/podcast
   streamlit run app.py
   ```

2. **Open browser:** http://localhost:8501

3. **Upload PDF:** Click browse or drag-drop

4. **Configure Sections:**
   - Section 1: Pages 3-4
   - Section 2: Pages 17-18

5. **Click:** "🎙️ Generate Podcast"

6. **Wait:** ~30-60 seconds

7. **View Results:** Switch to "Results" tab

8. **Download:** Click download buttons

### Example 2: Web UI with Claude

1. **Start UI:**
   ```bash
   cd /Users/rishabhporwal/Desktop/podcast
   streamlit run app.py
   ```

2. **Open browser:** http://localhost:8501

3. **In Sidebar:**
   - Select "anthropic" from dropdown
   - Enter your API key

4. **Rest same as Example 1**

### Example 3: CLI with Custom Config

1. **Create config file:** `my_config.json`
   ```json
   {
     "pdf_path": "my_document.pdf",
     "sections": {
       "Introduction": [1, 3],
       "Conclusion": [50, 52]
     },
     "target_word_count": 1500
   }
   ```

2. **Run:**
   ```bash
   cd /Users/rishabhporwal/Desktop/podcast
   python3 src/main.py my_config.json
   ```

3. **Check outputs:**
   ```bash
   ls example_output/
   ```

4. **View logs:**
   ```bash
   ls logs/
   tail -100 logs/podcast_generation_*.log
   ```

---

## 📊 Viewing Logs

### Real-time Logs (During Execution)
Watch the terminal where you ran the command.

### Saved Log Files
```bash
cd /Users/rishabhporwal/Desktop/podcast
ls -lt logs/
```

### View Latest Log
```bash
cd /Users/rishabhporwal/Desktop/podcast
tail -100 logs/podcast_generation_*.log | less
```

### View Specific Log
```bash
cd /Users/rishabhporwal/Desktop/podcast
cat logs/podcast_generation_20260127_213045.log
```

### Search Logs for Errors
```bash
cd /Users/rishabhporwal/Desktop/podcast
grep -i "error" logs/*.log
```

### Monitor Live (During Generation)
```bash
cd /Users/rishabhporwal/Desktop/podcast
tail -f logs/podcast_generation_*.log
```

---

## 🔧 Switching Between LLM Providers

### Method 1: Via .env File (CLI)

Edit `.env`:
```bash
cd /Users/rishabhporwal/Desktop/podcast
nano .env
```

**For Ollama:**
```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

**For Claude:**
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Save and run:
```bash
python3 src/main.py config.json
```

### Method 2: Via UI Sidebar (Web UI)

No file editing needed - just use the dropdown in the sidebar!

---

## 🆘 Troubleshooting

### Issue: "streamlit: command not found"
```bash
python3 -m pip install streamlit
```

### Issue: "No module named 'langgraph'"
```bash
python3 -m pip install -r requirements.txt
```

### Issue: Ollama Not Responding
```bash
# Check if running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve

# Check llama3 model
ollama list
```

### Issue: Port 8501 Already in Use
```bash
# Find process
lsof -ti:8501

# Kill it
kill $(lsof -ti:8501)

# Or use different port
streamlit run app.py --server.port 8502
```

### Issue: PDF Not Found
```bash
# Check PDF location
ls -la *.pdf

# Use absolute path in config
{
  "pdf_path": "/Users/rishabhporwal/Desktop/podcast/Vestas Annual Report 2024.pdf",
  ...
}
```

### Issue: Generation Takes Too Long
**Normal Times:**
- Ollama/Llama3: 30-60 seconds
- Claude: 60-90 seconds

**If > 2 minutes:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Check logs
tail -f logs/podcast_generation_*.log
```

---

## 📝 Configuration Files Explained

### .env File
```bash
# Which LLM to use
LLM_PROVIDER=ollama          # or 'anthropic'

# Ollama settings (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3          # or 'llama3:70b', 'mixtral', etc.

# Anthropic settings (if using Claude)
ANTHROPIC_API_KEY=sk-ant-...  # Your API key from console.anthropic.com
```

### config.json File
```json
{
  "pdf_path": "your_document.pdf",        // Path to PDF (relative or absolute)
  "sections": {
    "Section Name": [start_page, end_page],  // 1-indexed page numbers
    "Introduction": [1, 2],
    "Analysis": [10, 15]
  },
  "target_word_count": 2000               // Desired script length
}
```

---

## 🎯 Complete Example Workflow

### Full CLI Workflow
```bash
# 1. Navigate to project
cd /Users/rishabhporwal/Desktop/podcast

# 2. Check everything is ready
python3 test_system.py

# 3. (Optional) Edit configuration
nano config.json

# 4. Run generation
python3 src/main.py config.json

# 5. Check outputs
ls -lh example_output/

# 6. View script
cat example_output/podcast_script.md

# 7. View logs
tail -50 logs/podcast_generation_*.log
```

### Full UI Workflow
```bash
# 1. Navigate to project
cd /Users/rishabhporwal/Desktop/podcast

# 2. Start UI
streamlit run app.py

# 3. Browser opens automatically to http://localhost:8501

# 4. Use the interface:
#    - Upload PDF
#    - Configure sections
#    - Generate
#    - Download results

# 5. Stop server when done
# Press Ctrl+C in terminal
```

---

## 🎉 Summary

### To Run Web UI:
```bash
cd /Users/rishabhporwal/Desktop/podcast && streamlit run app.py
```
**Then open**: http://localhost:8501

### To Run CLI:
```bash
cd /Users/rishabhporwal/Desktop/podcast && python3 src/main.py config.json
```
**Outputs in**: `example_output/`
**Logs in**: `logs/`

### To View Logs:
```bash
cd /Users/rishabhporwal/Desktop/podcast && ls -lt logs/
```

---

## 📚 Additional Resources

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: [README.md](README.md)
- **Technical Details**: [process.md](process.md)
- **UI Info**: [UI_LAUNCH_INFO.md](UI_LAUNCH_INFO.md)
- **Implementation Notes**: [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)

---

**Current Status**: ✅ All systems operational
**UI Running**: Check `lsof -ti:8501`
**Logs Location**: `/Users/rishabhporwal/Desktop/podcast/logs/`
