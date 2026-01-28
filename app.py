"""
Streamlit Web UI for PDF-to-Podcast Generator

A user-friendly web interface for generating podcast scripts from PDF documents.
"""

import streamlit as st
import sys
import os
import tempfile
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from dotenv import load_dotenv
from workflow import PodcastWorkflow
from utils.llm_provider import create_llm_provider
from utils.helpers import format_verification_report, count_words
from agents.pdf_extractor import PDFExtractor

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="PDF to Podcast Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🎙️ PDF to Podcast Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Convert PDF documents into engaging two-host podcast scripts with AI-powered verification</p>', unsafe_allow_html=True)

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # LLM Provider selection
    provider_type = st.selectbox(
        "LLM Provider",
        options=["ollama", "anthropic"],
        index=0 if os.getenv("LLM_PROVIDER", "ollama") == "ollama" else 1,
        help="Choose between local Ollama or cloud-based Anthropic Claude"
    )

    if provider_type == "ollama":
        st.info("🖥️ Using Ollama (local)\n\nFast, free, private")
        ollama_model = st.text_input(
            "Ollama Model",
            value=os.getenv("OLLAMA_MODEL", "llama3"),
            help="e.g., llama3, mixtral, qwen"
        )
    else:
        st.info("☁️ Using Anthropic Claude\n\nHigher quality, API key required")
        anthropic_key = st.text_input(
            "Anthropic API Key",
            type="password",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            help="Get your API key from console.anthropic.com"
        )

    st.divider()

    # Target word count
    target_word_count = st.slider(
        "Target Word Count",
        min_value=500,
        max_value=5000,
        value=2000,
        step=100,
        help="Approximate length of generated podcast script"
    )

    st.divider()

    # Info section
    with st.expander("ℹ️ How it works"):
        st.markdown("""
        **Step 1: Extract**
        - Upload PDF and select page ranges
        - System extracts text from specified sections

        **Step 2: Generate**
        - AI creates natural two-host dialogue
        - Includes friction, teaching, and takeaways

        **Step 3: Verify**
        - Checks factual accuracy
        - Traces claims to source material
        - Detects hallucinations
        """)

# Main content area
tab1, tab2, tab3 = st.tabs(["📤 Generate", "📊 Results", "📖 Documentation"])

with tab1:
    # PDF Upload
    st.subheader("1️⃣ Upload PDF Document")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf'],
        help="Upload the PDF document you want to convert into a podcast"
    )

    if uploaded_file:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name

        st.success(f"✅ Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")

        # Extract PDF info
        try:
            with PDFExtractor(pdf_path) as extractor:
                doc_info = extractor.get_document_info()
                total_pages = doc_info['page_count']

            st.info(f"📄 Document has **{total_pages}** pages")

            # Section configuration
            st.subheader("2️⃣ Configure Sections to Extract")
            st.write("Define which sections of the PDF to include in the podcast:")

            # Initialize session state for sections
            if 'sections' not in st.session_state:
                st.session_state.sections = [
                    {"name": "Section 1", "start": 1, "end": 2}
                ]

            # Display section inputs
            for i, section in enumerate(st.session_state.sections):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    section['name'] = st.text_input(
                        "Section Name",
                        value=section['name'],
                        key=f"name_{i}",
                        label_visibility="collapsed"
                    )

                with col2:
                    section['start'] = st.number_input(
                        "Start Page",
                        min_value=1,
                        max_value=total_pages,
                        value=min(section['start'], total_pages),
                        key=f"start_{i}",
                        label_visibility="collapsed"
                    )

                with col3:
                    section['end'] = st.number_input(
                        "End Page",
                        min_value=section['start'],
                        max_value=total_pages,
                        value=min(max(section['end'], section['start']), total_pages),
                        key=f"end_{i}",
                        label_visibility="collapsed"
                    )

                with col4:
                    if st.button("🗑️", key=f"del_{i}", disabled=len(st.session_state.sections) == 1):
                        st.session_state.sections.pop(i)
                        st.rerun()

            # Add section button
            if st.button("➕ Add Section"):
                st.session_state.sections.append({
                    "name": f"Section {len(st.session_state.sections) + 1}",
                    "start": 1,
                    "end": min(2, total_pages)
                })
                st.rerun()

            st.divider()

            # Generate button
            st.subheader("3️⃣ Generate Podcast")

            col1, col2 = st.columns([1, 3])

            with col1:
                generate_button = st.button(
                    "🎙️ Generate Podcast",
                    type="primary",
                    use_container_width=True
                )

            with col2:
                if provider_type == "anthropic" and not anthropic_key:
                    st.warning("⚠️ Anthropic API key required")

            # Generation process
            if generate_button:
                if provider_type == "anthropic" and not anthropic_key:
                    st.error("❌ Please provide Anthropic API key in the sidebar")
                else:
                    # Prepare sections config
                    sections_config = {
                        section['name']: [section['start'], section['end']]
                        for section in st.session_state.sections
                    }

                    # Progress tracking
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        # Initialize LLM provider
                        status_text.text("🔧 Initializing LLM provider...")
                        progress_bar.progress(10)

                        if provider_type == "anthropic":
                            llm_provider = create_llm_provider(
                                provider_type="anthropic",
                                api_key=anthropic_key
                            )
                        else:
                            llm_provider = create_llm_provider(
                                provider_type="ollama",
                                model=ollama_model
                            )

                        # Initialize workflow
                        status_text.text("🔧 Setting up workflow...")
                        progress_bar.progress(20)
                        workflow = PodcastWorkflow(llm_provider)

                        # Run workflow
                        status_text.text("📄 Extracting PDF content...")
                        progress_bar.progress(30)

                        final_state = workflow.run(
                            pdf_path=pdf_path,
                            sections_config=sections_config,
                            target_word_count=target_word_count
                        )

                        progress_bar.progress(100)
                        status_text.text("✅ Generation complete!")

                        # Check if successful
                        if final_state["status"] == "verification_complete":
                            # Store results in session state
                            st.session_state.script = final_state["podcast_script"]
                            st.session_state.verification = final_state["verification_report"]
                            st.session_state.extracted_sections = final_state["extracted_sections"]

                            st.success("🎉 Podcast script generated successfully!")
                            st.info("👉 Check the **Results** tab to view and download your podcast script")

                            # Auto-switch to results tab (user needs to click)
                            st.balloons()
                        else:
                            error_msg = final_state.get("error", "Unknown error")
                            st.error(f"❌ Generation failed: {error_msg}")

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        import traceback
                        with st.expander("🔍 Error Details"):
                            st.code(traceback.format_exc())

                    finally:
                        # Clean up temp file
                        if os.path.exists(pdf_path):
                            try:
                                os.unlink(pdf_path)
                            except:
                                pass

        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")

with tab2:
    st.subheader("📊 Generated Results")

    if 'script' in st.session_state and st.session_state.script:
        # Script section
        st.markdown("### 🎙️ Podcast Script")

        script = st.session_state.script
        word_count = count_words(script)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", word_count)
        with col2:
            st.metric("Est. Duration", f"~{word_count // 150} min")
        with col3:
            claims = len(st.session_state.verification.get("claim_traceability", []))
            st.metric("Claims Verified", claims)

        # Display script
        st.markdown("---")
        st.markdown(script)

        # Download button
        st.download_button(
            label="📥 Download Script",
            data=script,
            file_name="podcast_script.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.divider()

        # Verification report
        st.markdown("### 🔍 Verification Report")

        verification = st.session_state.verification

        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Claims",
                verification['summary']['total_claims']
            )
        with col2:
            hallucinations = verification['summary']['hallucinated_claims']
            st.metric(
                "Hallucinations",
                hallucinations,
                delta=None,
                delta_color="inverse"
            )
        with col3:
            st.metric(
                "Sections Analyzed",
                verification['summary']['sections_analyzed']
            )

        # Show hallucination flags if any
        if verification['hallucination_flags']:
            st.warning("⚠️ Hallucinations Detected")
            for flag in verification['hallucination_flags']:
                st.error(f"**Claim:** {flag['claim']}\n\n**Reason:** {flag['reason']}")
        else:
            st.success("✅ No hallucinations detected - all claims are traceable to source material")

        # Claim traceability in expander
        with st.expander("📋 Detailed Claim Traceability"):
            for i, claim in enumerate(verification['claim_traceability'], 1):
                st.markdown(f"**Claim {i}:** {claim['claim']}")
                st.caption(f"Type: {claim['claim_type']} | Traceable: {claim['traceable']} | Confidence: {claim['confidence']}")
                if claim.get('source_evidence'):
                    st.info(f"📄 Source: {claim['source_evidence'][:200]}...")
                st.markdown("---")

        # Coverage analysis
        with st.expander("📊 Coverage Analysis"):
            if 'sections' in verification['coverage_analysis']:
                for section in verification['coverage_analysis']['sections']:
                    st.markdown(f"### {section['section_name']}")
                    st.caption(f"Overall Coverage: **{section['overall_coverage']}**")

                    for point in section['key_points']:
                        icon = {"FULL": "✅", "PARTIAL": "⚠️", "OMITTED": "❌"}.get(point['coverage'], "❓")
                        st.markdown(f"{icon} **{point['coverage']}**: {point['point']}")

                    st.markdown("---")

        # Download verification report
        report_md = format_verification_report(verification)
        st.download_button(
            label="📥 Download Verification Report",
            data=report_md,
            file_name="verification_report.md",
            mime="text/markdown",
            use_container_width=True
        )

        # Extracted sections
        st.divider()
        with st.expander("📄 View Extracted Source Content"):
            for section_name, content in st.session_state.extracted_sections.items():
                st.markdown(f"### {section_name}")
                st.caption(f"{count_words(content)} words")
                st.text_area(
                    "Content",
                    value=content,
                    height=200,
                    key=f"extract_{section_name}",
                    label_visibility="collapsed"
                )

    else:
        st.info("👈 Generate a podcast first to see results here")

with tab3:
    st.subheader("📖 Documentation")

    st.markdown("""
    ## About This System

    This AI-powered system converts PDF documents into engaging podcast scripts using a sophisticated
    agentic architecture built with LangGraph.

    ### Architecture

    The system uses three specialized agents:

    1. **PDF Extractor Agent**
       - Extracts text from specified page ranges
       - Preserves document structure
       - Handles multi-page sections

    2. **Podcast Generator Agent**
       - Creates natural two-host dialogue
       - Ensures conversational quality with friction
       - Targets specified word count
       - Uses carefully crafted prompts

    3. **Verification Agent**
       - Extracts factual claims from script
       - Traces claims to source material
       - Detects hallucinations
       - Analyzes coverage of key information

    ### LLM Providers

    **Ollama (Local)**
    - ✅ Free and private
    - ✅ Fast response times
    - ✅ No API costs
    - ⚠️ May produce shorter outputs
    - ⚠️ Less precise instruction following

    **Anthropic Claude**
    - ✅ Higher quality output
    - ✅ Better instruction following
    - ✅ More natural dialogue
    - ⚠️ Requires API key (~$0.10-0.30/run)

    ### Tips for Best Results

    1. **Section Selection**: Choose sections with clear, factual content
    2. **Page Ranges**: Keep sections reasonably sized (2-10 pages each)
    3. **Word Count**: 2,000 words ≈ 10 minutes of spoken content
    4. **LLM Choice**: Use Claude for production-quality output

    ### Technical Details

    - **Framework**: LangGraph for workflow orchestration
    - **PDF Processing**: PyMuPDF for text extraction
    - **LLM Integration**: Multi-provider abstraction layer
    - **Output Formats**: Markdown (script) + JSON/Markdown (verification)

    ### Source Code

    This project is built with:
    - Python 3.8+
    - LangGraph for agentic workflows
    - Streamlit for web interface
    - Anthropic/Ollama for LLM generation

    See the [README.md](README.md) and [process.md](process.md) for more details.
    """)

    st.divider()

    st.markdown("""
    ### Example Use Cases

    - 📚 **Research Papers** → Educational podcast episodes
    - 📊 **Annual Reports** → Business insights podcasts
    - 📰 **White Papers** → Explainer podcasts
    - 📖 **Documentation** → Tutorial podcasts
    """)

# Footer
st.markdown("---")
st.caption("🎙️ PDF to Podcast Generator | Built with LangGraph & Streamlit")
