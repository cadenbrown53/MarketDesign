#!/usr/bin/env python3
"""Extract Chapter/Section 4 from the Market Design Handbook PDF."""

import pypdf
import sys

def extract_section_4():
    pdf_path = '/Users/cadenbrown/MarketDesign/MarketDesignHandbook.pdf'
    reader = pypdf.PdfReader(pdf_path)
    
    # Find where Section IV starts
    section_4_start = None
    section_5_start = None
    
    print(f"Total pages in PDF: {len(reader.pages)}")
    print("\nSearching for Section IV...")
    
    for i in range(len(reader.pages)):
        text = reader.pages[i].extract_text()
        lines = text.split('\n')
        
        # Look for "4 Designing Markets" header
        if section_4_start is None:
            for line in lines[:50]:  # Check first 50 lines
                line_stripped = line.strip()
                if ('4 Designing Markets' in line or 
                    line_stripped == '4 Designing Markets' or
                    '4Designing Markets' in line.replace(' ', '')):
                    section_4_start = i
                    print(f"Found '4 Designing Markets' starting at page {i+1}")
                    print(f"Section heading: '{line_stripped}'")
                    break
        
        # Look for Section 5 to know where Section 4 ends
        if section_4_start is not None and section_5_start is None:
            for line in lines[:50]:
                line_stripped = line.strip()
                if (line_stripped.startswith('5 ') and len(line_stripped) < 50):
                    section_5_start = i
                    print(f"Found Section 5 starting at page {i+1}")
                    print(f"Heading: '{line_stripped}'")
                    break
            if section_5_start:
                break
    
    if section_4_start is None:
        print("Could not find Section IV. Let me show you the document structure:")
        for i in [0, 5, 10, 20, 30, 40, 50, 60]:
            if i < len(reader.pages):
                text = reader.pages[i].extract_text()
                print(f"\n=== Page {i+1} (first 400 chars) ===")
                print(text[:400])
        return None
    
    # Extract all text from Section IV (include the page where Section 5 starts since Section 4 content may extend onto it)
    if section_5_start:
        end_page = section_5_start + 1  # Include page 72 where section 5 header is found
    else:
        end_page = len(reader.pages)
    
    print(f"\nExtracting Section IV from pages {section_4_start+1} to {end_page}")
    
    section_text = []
    for i in range(section_4_start, end_page):
        page_text = reader.pages[i].extract_text()
        section_text.append(f"\n--- Page {i+1} ---\n")
        section_text.append(page_text)
    
    full_text = ''.join(section_text)
    
    # Save to file
    output_file = '/Users/cadenbrown/MarketDesign/chapter4_extracted.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"\n✓ Successfully extracted {len(full_text)} characters")
    print(f"✓ Saved to: {output_file}")
    
    # Show preview
    print("\n=== Preview (first 2000 characters) ===")
    print(full_text[:2000])
    
    return full_text

if __name__ == '__main__':
    extract_section_4()
