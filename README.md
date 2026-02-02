# PDF-to-Podcast Generator with Verification

An AI-powered system that converts long-form PDF documents into engaging two-host podcast scripts with comprehensive factual verification.

## Overview

This system takes a PDF document, extracts specified sections, generates a natural conversational podcast script (~2,000 words / ~10 minutes), and produces a detailed verification report that checks for factual accuracy, claim traceability, and content coverage.

**Key Features:**
- 🎙️ Natural two-host conversational dialogue (not alternating monologues)
- 🔍 Comprehensive verification with claim traceability
- 🚨 Automatic hallucination detection
- 📊 Coverage analysis for source material
- ⚙️ Configurable section selection via page ranges
- 🤖 Agentic architecture with specialized agents
- 🖥️ **Web UI** - User-friendly Streamlit interface
- 💻 **CLI** - Command-line interface for automation
- 📊 **Comprehensive Logging** - Full traceability with timestamped logs in `logs/` directory

## 📚 Documentation

- **[FINAL_GUIDE.md](FINAL_GUIDE.md)** - ⭐ **START HERE** - Complete guide with logging details
- **[SETUP_AND_RUN.md](SETUP_AND_RUN.md)** - Step-by-step setup instructions
- **[QUICKSTART.md](QUICKSTART.md)** - 2-minute quick start
- **[process.md](process.md)** - Technical architecture and decisions
- **[IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)** - Ollama vs Claude comparison
- **[master_prompt.md](master_prompt.md)** - Master/Developer Prompt

## Architecture

The system uses three specialized agents coordinated by an orchestrator:

1. **PDF Extraction Agent**: Extracts text from configurable page ranges
2. **Podcast Script Generator Agent**: Creates natural two-host dialogue using Claude
3. **Verification Agent**: Validates accuracy and analyzes coverage
4. **Orchestrator**: Coordinates the pipeline and manages data flow

## Requirements

- Python 3.8+
- Anthropic API key (Claude)
- PDF documents (digital text, not scanned images)

## Installation

### 1. Clone or download this repository

```bash
cd podcast
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

Get your API key from: https://console.anthropic.com/

## Usage

### Option 1: Web UI (Recommended)

The easiest way to use the system is through the Streamlit web interface:

```bash
streamlit run app.py
```

Or use the provided script:

```bash
./run_ui.sh
```

Then open your browser to: **http://localhost:8501**

**Features:**
- 📤 Drag-and-drop PDF upload
- ⚙️ Interactive section configuration
- 🎛️ Real-time LLM provider selection
- 📊 Live progress tracking
- 📥 Download generated scripts and reports
- 🔍 View verification results inline

### Option 2: Command Line Interface

### Basic Usage

1. **Place your PDF** in the project directory (or note its path)

2. **Configure sections** in `config.json`:

```json
{
  "pdf_path": "your_document.pdf",
  "sections": {
    "Introduction": [1, 2],
    "Key Findings": [10, 15],
    "Conclusion": [45, 46]
  },
  "target_word_count": 2000
}
```

**Note**: Page numbers are 1-indexed (as they appear in PDF viewers).

3. **Run the system**:

```bash
python src/main.py
```

Or with a custom config:

```bash
python src/main.py path/to/config.json
```

### Output

The system generates three files in the `example_output/` directory:

1. **`podcast_script.md`**: The generated podcast script
2. **`verification_report.md`**: Human-readable verification report
3. **`verification_report.json`**: Machine-readable verification data

## Configuration

### Section Selection

The system uses **page ranges** for section selection. This approach is:
- **Deterministic**: Same pages = same content
- **Robust**: Works with any PDF structure
- **Simple**: Easy to configure and understand

Format: `"Section Name": [start_page, end_page]`

Example:
```json
{
  "sections": {
    "Executive Summary": [1, 3],
    "Market Analysis": [10, 15],
    "Strategy": [20, 25]
  }
}
```

### Target Word Count

Adjust the `target_word_count` parameter to control script length:
- ~2,000 words ≈ 10 minutes of spoken content
- ~1,500 words ≈ 7-8 minutes
- ~2,500 words ≈ 12-13 minutes

## Example Output

The repository includes example output generated from the **Vestas Annual Report 2024**:

- [`example_output/podcast_script.md`](example_output/podcast_script.md)
- [`example_output/verification_report.md`](example_output/verification_report.md)

These demonstrate the system's capabilities on a real-world 221-page corporate document.

## How It Works

### 1. PDF Extraction
- Uses PyMuPDF to extract text from specified page ranges
- Preserves document structure and context
- Handles multi-page sections seamlessly

### 2. Podcast Generation
- Uses Claude (Sonnet 4.5) with carefully crafted prompts
- Generates two distinct hosts: Alex (analytical) and Jordan (strategic)
- Ensures natural conversation with:
  - Back-and-forth dialogue
  - Friction and disagreement
  - Emotional cues (curiosity, skepticism, surprise)
  - Clear "so what" takeaway

### 3. Verification
- **Claim Extraction**: Identifies factual claims in the script
- **Traceability**: Maps each claim to source passages
- **Hallucination Detection**: Flags untraceable claims
- **Coverage Analysis**: Measures how well key information is covered

## Project Structure

```
podcast/
├── README.md                      # This file
├── process.md                     # Technical documentation and reflection
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── config.json                    # Configuration file
├── src/
│   ├── main.py                    # Main orchestrator
│   ├── agents/
│   │   ├── pdf_extractor.py       # PDF extraction agent
│   │   ├── podcast_generator.py   # Script generation agent
│   │   └── verifier.py            # Verification agent
│   └── utils/
│       └── helpers.py             # Utility functions
└── example_output/
    ├── podcast_script.md          # Example script
    ├── verification_report.md     # Example report (Markdown)
    └── verification_report.json   # Example report (JSON)
```

## Customization

### Using Different LLM Models

Edit the agent initialization in `src/main.py`:

```python
self.podcast_generator = PodcastGenerator(
    self.api_key,
    model="claude-opus-4-20250514"  # Use Opus for higher quality
)
```

### Adjusting Podcast Style

Modify the system prompt in [`src/agents/podcast_generator.py`](src/agents/podcast_generator.py) to customize:
- Host personalities
- Conversational style
- Level of friction
- Emotional tone

## Troubleshooting

### API Key Issues
- Ensure `.env` file exists and contains valid API key
- Verify key is active at https://console.anthropic.com/

### PDF Not Found
- Check PDF path in `config.json`
- Use absolute path if relative path fails

### Memory Issues with Large PDFs
- Process smaller page ranges
- The system loads entire PDF into memory

### Rate Limits
- The system makes 2 API calls per run (generation + verification)
- Respect Anthropic rate limits for your tier

## Performance

**Approximate execution time** (for ~10 page extraction):
- PDF Extraction: < 1 second
- Podcast Generation: 10-30 seconds
- Verification: 15-40 seconds
- **Total**: ~30-70 seconds

**Cost estimate** (using Claude Sonnet):
- ~$0.10-0.30 per podcast (varies with source document size)

## Limitations

- Requires digital PDF text (not scanned images/OCR)
- Best with structured documents (reports, articles, papers)
- Page-range configuration requires manual inspection
- Currently supports only English language content
- No audio generation (text-only output)

## Future Improvements

See [`process.md`](process.md) for detailed discussion of:
- Potential enhancements
- Known weaknesses
- Alternative approaches considered

## License

This project is provided as-is for assessment purposes.

## Support

For issues or questions, please refer to the technical documentation in [`process.md`](process.md).
