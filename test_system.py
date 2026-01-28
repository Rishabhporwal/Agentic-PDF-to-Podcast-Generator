#!/usr/bin/env python3
"""Quick test script to debug the system."""

import sys
sys.path.insert(0, 'src')

print("=" * 60)
print("TESTING SYSTEM COMPONENTS")
print("=" * 60)

# Test 1: Load environment
print("\n[1] Loading environment...")
from dotenv import load_dotenv
import os
load_dotenv()
provider_type = os.getenv("LLM_PROVIDER", "ollama")
print(f"✓ LLM Provider: {provider_type}")

# Test 2: Create LLM provider
print("\n[2] Creating LLM provider...")
try:
    from utils.llm_provider import create_llm_provider
    llm_provider = create_llm_provider(provider_type=provider_type)
    print(f"✓ LLM Provider created successfully")
except Exception as e:
    print(f"✗ Error creating LLM provider: {e}")
    sys.exit(1)

# Test 3: Load config
print("\n[3] Loading configuration...")
import json
with open('config.json', 'r') as f:
    config = json.load(f)
print(f"✓ Config loaded")
print(f"  PDF: {config['pdf_path']}")
print(f"  Sections: {list(config['sections'].keys())}")

# Test 4: Check PDF exists
print("\n[4] Checking PDF file...")
if not os.path.exists(config['pdf_path']):
    print(f"✗ PDF not found: {config['pdf_path']}")
    sys.exit(1)
print(f"✓ PDF exists")

# Test 5: Test PDF extraction
print("\n[5] Testing PDF extraction...")
from agents.pdf_extractor import PDFExtractor
try:
    with PDFExtractor(config['pdf_path']) as extractor:
        doc_info = extractor.get_document_info()
        print(f"✓ PDF opened: {doc_info['page_count']} pages")

        # Extract first section only for testing
        first_section = list(config['sections'].items())[0]
        section_name, page_range = first_section
        test_sections = {section_name: page_range}

        extracted = extractor.extract_sections(test_sections)
        word_count = len(extracted[section_name].split())
        print(f"✓ Extracted test section: {word_count} words")
except Exception as e:
    print(f"✗ Extraction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Test LLM generation (simple)
print("\n[6] Testing LLM generation...")
try:
    test_response = llm_provider.generate(
        system_prompt="You are a helpful assistant.",
        user_prompt="Say 'test successful' and nothing else.",
        temperature=0.0,
        max_tokens=50
    )
    print(f"✓ LLM responded: {test_response[:100]}...")
except Exception as e:
    print(f"✗ LLM generation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED")
print("=" * 60)
print("\nThe system should work correctly. Try running: python3 src/main.py config.json")
