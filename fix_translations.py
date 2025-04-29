#!/usr/bin/env python
"""
Script to fix duplicate translations in a Django PO file.
This script reads a PO file, removes duplicate msgid entries,
and writes a clean version.
"""

import re
import sys
from collections import OrderedDict

def clean_po_file(input_file, output_file):
    # Read the file content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by message blocks
    # Message blocks typically start with a blank line followed by #: or msgid
    pattern = r'\n\n(#:.*?\n)?msgid ".*?"'
    blocks = re.split(pattern, content)
    
    # The first block is the header, keep it separately
    header = blocks[0]
    
    # Dictionary to store unique translations
    translations = OrderedDict()
    
    # Process each block
    for i in range(1, len(blocks), 2):
        # Combine the split parts back
        if i < len(blocks) - 1:
            block = "\n\n" + (blocks[i] or "") + "msgid " + blocks[i+1].strip()
        else:
            continue
        
        # Extract msgid
        msgid_match = re.search(r'msgid "(.*?)"', block, re.DOTALL)
        if not msgid_match:
            continue
        
        msgid = msgid_match.group(1)
        
        # Only add if not already present
        if msgid not in translations:
            translations[msgid] = block
    
    # Write the cleaned file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(header)
        for block in translations.values():
            f.write(block)

if __name__ == "__main__":
    input_file = "locale/ru/LC_MESSAGES/django.po"
    output_file = "locale/ru/LC_MESSAGES/django.po.cleaned"
    
    clean_po_file(input_file, output_file)
    print(f"Cleaned file written to {output_file}")
    print("Review the cleaned file, and if it looks good, replace the original with it.") 