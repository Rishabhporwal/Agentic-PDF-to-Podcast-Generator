# 🎉 Complete Setup Guide - PDF to Podcast Generator

## ✅ System Status

**Project Location**: `/Users/rishabhporwal/Desktop/podcast`

**Features Implemented**:
- ✅ Web UI (Streamlit) - Running
- ✅ CLI Interface - Ready
- ✅ LangGraph Workflow - Implemented
- ✅ Multi-LLM Support (Ollama + Claude) - Configured
- ✅ **Comprehensive Logging** - Active
- ✅ Example Outputs - Generated

---

## 🚀 How to Run (Choose One)

### Option A: Web UI (Easiest)

**Single Command:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && streamlit run app.py
```

**Then open browser to**: http://localhost:8501

**What you get:**
- 📤 Drag-and-drop PDF upload
- ⚙️ Interactive configuration
- 📊 Real-time progress
- 📥 Download buttons
- 🔍 Inline verification results

---

### Option B: Command Line

**Single Command:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && python3 src/main.py config.json
```

**What you get:**
- Console output with progress
- Files saved to `example_output/`
- **Detailed logs in `logs/` directory**

---

## 📊 NEW: Comprehensive Logging System

### Where Logs Are Saved

**Location**: `/Users/rishabhporwal/Desktop/podcast/logs/`

**Format**: `podcast_generation_YYYYMMDD_HHMMSS.log`

**Example**: `podcast_generation_20260127_020555.log`

### What's Logged

**INFO Level** (Console + File):
- Major steps (PDF opened, script generated, etc.)
- Progress indicators
- Success/failure messages
- Word counts and metrics

**DEBUG Level** (File only):
- Detailed agent actions
- Page-by-page extraction details
- Prompt lengths
- LLM call details
- Character counts

**Example Log Output**:
```
2026-01-27 02:05:55 - pdf_extractor - INFO - Opening PDF: Vestas Annual Report 2024.pdf
2026-01-27 02:05:55 - pdf_extractor - DEBUG - PDF opened successfully. Pages: 221
2026-01-27 02:05:56 - pdf_extractor - INFO - Extracting 4 sections from PDF
2026-01-27 02:05:56 - pdf_extractor - DEBUG - Extracting section 'Letter from the Chair & CEO' (pages 3-4)
2026-01-27 02:05:57 - pdf_extractor - INFO - ✓ Section 'Letter from the Chair & CEO': 1362 words extracted
2026-01-27 02:06:10 - podcast_generator - INFO - Generating podcast script from 4 sections
2026-01-27 02:06:10 - podcast_generator - INFO - Target word count: 2000
2026-01-27 02:06:45 - podcast_generator - INFO - ✓ Script generated: 411 words
2026-01-27 02:07:00 - verifier - INFO - Verifying script against 4 source sections
2026-01-27 02:07:30 - verifier - INFO - ✓ Verification complete: 9 claims, 0 hallucinations
```

### How to View Logs

**View latest logs:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
ls -lt logs/ | head -5
```

**View specific log file:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
cat logs/podcast_generation_20260127_020555.log
```

**Monitor live during generation:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
tail -f logs/podcast_generation_*.log
```

**Search for errors:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
grep -i "error" logs/*.log
```

**View last 50 lines:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
tail -50 logs/podcast_generation_*.log
```

---

## 🎯 Complete Workflow Example

### Step 1: Navigate to Project
```bash
cd /Users/rishabhporwal/Desktop/podcast
```

### Step 2: Choose Your Interface

**For Web UI:**
```bash
streamlit run app.py
```
Then open: http://localhost:8501

**For CLI:**
```bash
python3 src/main.py config.json
```

### Step 3: During Generation

**Monitor logs in real-time:**
```bash
# Open a second terminal
cd /Users/rishabhporwal/Desktop/podcast
tail -f logs/podcast_generation_*.log
```

### Step 4: After Generation

**View outputs:**
```bash
ls -lh example_output/
```

**Read script:**
```bash
cat example_output/podcast_script.md
```

**Read verification:**
```bash
cat example_output/verification_report.md
```

**Review logs:**
```bash
cat logs/podcast_generation_*.log
```
---

## 🔍 Traceability Features

### 1. Execution Logs

Every run creates a timestamped log file with:
- **Agent actions**: What each agent is doing
- **Timing**: When each step occurred
- **Word counts**: How much content extracted/generated
- **Errors**: Any issues encountered
- **LLM calls**: What prompts were sent

### 2. Verification Reports

For each generated script:
- **Claim traceability**: Every factual claim mapped to source
- **Hallucination detection**: Untraceable claims flagged
- **Coverage analysis**: What content was included/omitted
- **Confidence scores**: How reliable each claim is

### 3. Complete Audit Trail

For any podcast generation, you can trace:
1. **What PDF was used** (from config)
2. **What sections were extracted** (from logs)
3. **How many words extracted** (from logs)
4. **What LLM was used** (from logs)
5. **How long it took** (from log timestamps)
6. **What was generated** (saved scripts)
7. **What claims were made** (verification report)
8. **What sources support claims** (verification evidence)

---

## 🎓 Example Traceability Flow

### Generation Request
```json
{
  "pdf_path": "Vestas Annual Report 2024.pdf",
  "sections": {
    "Letter from CEO": [3, 4]
  }
}
```

### Log Trace
```
2026-01-27 02:05:55 - pdf_extractor - INFO - Opening PDF: Vestas Annual Report 2024.pdf
2026-01-27 02:05:56 - pdf_extractor - INFO - Extracting 1 sections from PDF
2026-01-27 02:05:56 - pdf_extractor - DEBUG - Extracting section 'Letter from CEO' (pages 3-4)
2026-01-27 02:05:56 - pdf_extractor - DEBUG -   Extracted page 3: 650 characters
2026-01-27 02:05:56 - pdf_extractor - DEBUG -   Extracted page 4: 712 characters
2026-01-27 02:05:56 - pdf_extractor - INFO - ✓ Section 'Letter from CEO': 1362 words extracted
2026-01-27 02:06:10 - podcast_generator - INFO - Generating podcast script from 1 sections
2026-01-27 02:06:45 - podcast_generator - INFO - ✓ Script generated: 411 words
```

### Verification Output
```markdown
### Claim 1
**Statement**: "Vestas continued its positive trajectory in 2024"
**Source Section**: Letter from CEO
**Source Evidence**: "Progress in a challenging year"
**Traceable**: YES
```

### Complete Chain
```
Input Config → Log Entry → Extracted Content → Generated Claim → Source Evidence → ✓ Verified
```

---

## 🆘 Quick Troubleshooting

### Issue: Can't find logs

**Solution:**
```bash
cd /Users/rishabhporwal/Desktop/podcast
ls -la logs/
```

Logs are created automatically on first run.

### Issue: Logs not updating

**Solution:** Check if you're looking at the right file:
```bash
ls -lt logs/*.log | head -1
```

Each run creates a new timestamped file.

### Issue: Want more detailed logs

**Current**: Already logging at DEBUG level to files!

**To see DEBUG in console too**, edit `src/utils/logger.py`:
```python
console_handler.setLevel(logging.DEBUG)  # Change from INFO to DEBUG
```

---

## 📚 Documentation Quick Links

**For Quick Start**: [QUICKSTART.md](QUICKSTART.md)

**For All Commands**: [COMMANDS_CHEATSHEET.md](COMMANDS_CHEATSHEET.md)

**For Complete Setup**: [SETUP_AND_RUN.md](SETUP_AND_RUN.md)

**For Technical Details**: [process.md](process.md)

**For Main Documentation**: [README.md](README.md)

---

## ✨ Key Improvements Added

### 1. Logging System
- ✅ Timestamped log files
- ✅ Console + file output
- ✅ DEBUG and INFO levels
- ✅ Structured formatting
- ✅ Automatic log rotation (by timestamp)

### 2. Traceability
- ✅ Every agent action logged
- ✅ Word counts tracked
- ✅ Timing information
- ✅ Error details captured
- ✅ LLM calls documented

### 3. Documentation
- ✅ Step-by-step guides
- ✅ Command cheat sheet
- ✅ Troubleshooting tips
- ✅ Complete examples
- ✅ File location reference

---

## 🎯 Your Next Steps

1. **Run the Web UI**:
   ```bash
   cd /Users/rishabhporwal/Desktop/podcast && streamlit run app.py
   ```
   Open: http://localhost:8501

2. **Or run CLI**:
   ```bash
   cd /Users/rishabhporwal/Desktop/podcast && python3 src/main.py config.json
   ```

3. **Monitor logs**:
   ```bash
   tail -f /Users/rishabhporwal/Desktop/podcast/logs/podcast_generation_*.log
   ```

4. **Review outputs**:
   ```bash
   ls -lh /Users/rishabhporwal/Desktop/podcast/example_output/
   ```

---

## 🎉 Summary

**Web UI Command:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && streamlit run app.py
```

**CLI Command:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && python3 src/main.py config.json
```

**View Logs:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && ls -lt logs/
```

**Monitor Live:**
```bash
cd /Users/rishabhporwal/Desktop/podcast && tail -f logs/podcast_generation_*.log
```

---

**Everything is ready to use!** 🚀

Logs are automatically saved to `/Users/rishabhporwal/Desktop/podcast/logs/` with complete traceability.
