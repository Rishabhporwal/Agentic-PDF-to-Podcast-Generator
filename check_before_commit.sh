#!/bin/bash
# Pre-commit Security Check Script
# Run this before pushing to GitHub to verify no sensitive data is included

echo "🔒 Pre-Commit Security Check"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env is staged
echo "1. Checking .env file..."
if git diff --cached --name-only | grep -q "^.env$"; then
    echo -e "${RED}❌ ERROR: .env is staged! This contains API keys.${NC}"
    echo "   Run: git reset HEAD .env"
    exit 1
else
    echo -e "${GREEN}✅ .env is not staged${NC}"
fi

# Check if any log files are staged
echo ""
echo "2. Checking log files..."
if git diff --cached --name-only | grep -q "\.log$"; then
    echo -e "${RED}❌ ERROR: Log files are staged!${NC}"
    echo "   Run: git reset HEAD logs/"
    exit 1
else
    echo -e "${GREEN}✅ No log files staged${NC}"
fi

# Check if generated outputs are staged
echo ""
echo "3. Checking generated outputs..."
if git diff --cached --name-only | grep -q "example_output/.*\.md$\|example_output/.*\.json$"; then
    echo -e "${YELLOW}⚠️  WARNING: Generated output files are staged${NC}"
    echo "   These are usually not committed. Review with: git diff --staged"
fi

# Check for potential API keys in staged changes
echo ""
echo "4. Scanning for potential secrets..."
SECRETS_FOUND=false

if git diff --cached | grep -iE "(api[_-]?key|secret|password|token|bearer)" | grep -v ".gitignore" | grep -v "check_before_commit.sh" | grep -q .; then
    echo -e "${RED}❌ WARNING: Potential secrets found in staged changes!${NC}"
    echo ""
    echo "Found lines containing sensitive keywords:"
    git diff --cached | grep -iE "(api[_-]?key|secret|password|token|bearer)" | grep -v ".gitignore" | grep -v "check_before_commit.sh"
    echo ""
    echo "Please review these carefully!"
    SECRETS_FOUND=true
else
    echo -e "${GREEN}✅ No obvious secrets detected${NC}"
fi

# Check for large PDF files
echo ""
echo "5. Checking for PDF files..."
if git diff --cached --name-only | grep -q "\.pdf$"; then
    echo -e "${YELLOW}⚠️  WARNING: PDF files are staged${NC}"
    echo "   PDFs can be large. List:"
    git diff --cached --name-only | grep "\.pdf$"
    echo "   If these are example/demo files, this may be intentional."
fi

# Show summary of what will be committed
echo ""
echo "=============================="
echo "6. Files to be committed:"
echo "=============================="
git diff --cached --name-only | head -20

if [ $(git diff --cached --name-only | wc -l) -gt 20 ]; then
    echo "... and $(( $(git diff --cached --name-only | wc -l) - 20 )) more files"
fi

# Show ignored files for reference
echo ""
echo "=============================="
echo "7. Properly ignored files:"
echo "=============================="
git status --ignored --short | grep "^!!" | head -10
echo ""

# Final check
echo "=============================="
if [ "$SECRETS_FOUND" = true ]; then
    echo -e "${RED}❌ FAILED: Please review and fix issues above${NC}"
    exit 1
else
    echo -e "${GREEN}✅ PASSED: Safe to commit${NC}"
    echo ""
    echo "Next steps:"
    echo "  git commit -m \"Your commit message\""
    echo "  git push"
fi
