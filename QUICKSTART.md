# Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Launch the Web UI

The Streamlit UI is already running! Open your browser to:

```
http://localhost:8501
```

If it's not running, start it with:
```bash
streamlit run app.py
```

### Step 2: Configure LLM Provider

**Option A: Use Ollama (Local, Free)**
- Default configuration ✅
- Already set to use `llama3` model
- No API key needed
- Works immediately

**Option B: Use Anthropic Claude (Higher Quality)**
- In the sidebar, select "anthropic"
- Enter your API key from https://console.anthropic.com/
- Better output quality (~$0.10-0.30 per run)

### Step 3: Upload PDF

1. Click "Browse files" or drag-and-drop your PDF
2. System will show total page count
3. Example: Try the included "Vestas Annual Report 2024.pdf"

### Step 4: Configure Sections

Define which sections to extract:

**Example Configuration:**
```
Section Name         Start Page    End Page
Executive Summary    1             2
Key Findings         10            12
Conclusion           45            46
```

Click "➕ Add Section" to add more sections.

### Step 5: Generate Podcast

1. Adjust "Target Word Count" slider (default: 2,000 words)
2. Click **"🎙️ Generate Podcast"** button
3. Wait for generation (~30-90 seconds)
4. View results in the "Results" tab

### Step 6: Review & Download

In the **Results** tab you'll see:
- ✅ Generated podcast script
- ✅ Word count and duration estimate
- ✅ Verification report with claim traceability
- ✅ Hallucination detection results
- ✅ Coverage analysis

Download buttons available for:
- 📥 Podcast script (Markdown)
- 📥 Verification report (Markdown)

---

## 🎯 Example Workflow

### Try This First

1. **Launch UI**: `streamlit run app.py`
2. **Upload**: Use the included Vestas Annual Report 2024.pdf
3. **Configure Sections**:
   - Letter from the Chair & CEO: Pages 3-4
   - Market outlook: Pages 17-18
   - Corporate strategy: Pages 19-21
4. **Generate**: Click the button
5. **Review**: Check Results tab

Expected output:
- ~2,000 word script (with Claude) or ~400 words (with Llama3)
- Two-host dialogue format
- Verification with 0 hallucinations

---

## 💡 Tips for Best Results

### Section Selection
- Choose 2-5 sections for best results
- Keep each section 2-10 pages
- Select content-rich sections (avoid covers, TOCs)

### Word Count
- **500-1000 words**: Quick 5-minute podcast
- **2000 words**: Standard 10-minute episode
- **3000-4000 words**: Deep dive 15-20 minutes

### LLM Provider Comparison

| Feature | Ollama (Llama3) | Anthropic Claude |
|---------|-----------------|------------------|
| **Cost** | Free ✅ | ~$0.20/run |
| **Speed** | Fast ✅ | Moderate |
| **Quality** | Good | Excellent ✅ |
| **Word Count** | ~400-500 | ~2000 ✅ |
| **Dialogue** | Radio show | True two-host ✅ |
| **Setup** | None ✅ | API key required |

**Recommendation:**
- **Development/Testing**: Use Ollama
- **Production/Demo**: Use Claude

---

## 🔧 Troubleshooting

### UI Won't Start

```bash
# Check if Streamlit is installed
pip install streamlit

# Start manually
streamlit run app.py --server.port 8501
```

### Ollama Not Working

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start Ollama
ollama serve

# Pull llama3 model if needed
ollama pull llama3
```

### Generation Takes Too Long

- Llama3: Should complete in 30-60 seconds
- Claude: May take 60-90 seconds
- If > 2 minutes, check your internet/LLM connection

### Script Too Short

This is expected with Llama3 (~400 words vs 2000 target).

**Solutions:**
1. Switch to Claude (best option)
2. Use larger Ollama model: `ollama pull llama3:70b`
3. Accept shorter output for testing

### Verification Errors

If you see "Failed to parse verification output":
- This is non-fatal - script is still generated
- Llama3 sometimes doesn't format JSON correctly
- Switch to Claude for reliable verification

---

## 📝 Command Line Alternative

If you prefer CLI over UI:

```bash
# Edit config.json
{
  "pdf_path": "your_document.pdf",
  "sections": {
    "Introduction": [1, 2],
    "Analysis": [10, 15]
  },
  "target_word_count": 2000
}

# Run
python3 src/main.py config.json

# Outputs saved to example_output/
```

---

## 🎉 You're Ready!

The UI should now be running at **http://localhost:8501**

Try generating your first podcast script! 🎙️

For more details, see:
- [README.md](README.md) - Full documentation
- [process.md](process.md) - Technical details
- [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) - Architecture info
