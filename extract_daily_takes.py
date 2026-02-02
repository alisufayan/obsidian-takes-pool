#!/usr/bin/env python3
"""
Daily Takes Extractor - How to use this thing

This script extracts "takes" (thoughts/insights) from daily notes and 
dumps them into a pool file with Obsidian links.

FILE FORMAT IT EXPECTS:
Files like: 2024/06 - June/15 June.md or 2024/12 - December/25 December.md

IMPORTANT: This APPENDS to the pool file. Clear it first to avoid dupes:
    truncate -s 0 "Daily Notes/The daily takes pool.md"

Or just use this alias:
    alias takes='truncate -s 0 "Daily Notes/The daily takes pool.md" && python3 extract_daily_takes.py'
"""

import os
import glob
import re


def extract_takes(filepath):
    """Grab takes from a daily note file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return []
    
    # Find the Takes section
    match = re.search(r'###\s*The Takes of the day:\s*\n', content, re.IGNORECASE)
    if not match:
        return []
    
    # Get content after the header until next ### section
    start = match.end()
    remaining = content[start:]
    
    next_section = remaining.find('###')
    if next_section != -1:
        takes_section = remaining[:next_section]
    else:
        takes_section = remaining
    
    # Extract takes (handle multi-line takes)
    takes = []
    current_take_lines = []
    
    for line in takes_section.strip().split('\n'):
        line = line.strip()
        
        # Empty line = end of current take
        if not line:
            if current_take_lines:
                take = ' '.join(current_take_lines)
                # Clean up bullet prefix
                if take.startswith('- '):
                    take = take[2:]
                elif take.startswith('-'):
                    take = take[1:]
                take = take.strip()
                # Skip short takes (< 3 words)
                if len(take.split()) >= 3:
                    takes.append(take)
                current_take_lines = []
            continue
        
        # Skip hashtags and section headers
        if line.startswith('#'):
            continue
            
        current_take_lines.append(line)
    
    # Last take if file doesn't end with empty line
    # (happens sometimes, need to catch it)
    if current_take_lines:
        take = ' '.join(current_take_lines)
        if take.startswith('- '):
            take = take[2:]
        elif take.startswith('-'):
            take = take[1:]
        take = take.strip()
        if len(take.split()) >= 3:
            takes.append(take)
    
    return takes


def get_obsidian_link(filepath):
    """Generate Obsidian link from filename"""
    basename = os.path.basename(filepath)
    return f"[[{basename.replace('.md', '')}]]"


def main():
    # Setup paths
    home_dir = os.path.expanduser("~")
    base_dir = os.path.join(home_dir, "Documents", "My Mind Palace", "Daily Notes")
    pool_file = os.path.join(base_dir, "The daily takes pool.md")
    
    # Check if pool file has content
    if os.path.exists(pool_file) and os.path.getsize(pool_file) > 100:
        print("⚠️  WARNING: Pool file already has content!")
        print("   Running again will ADD duplicates, not replace.")
        print()
        print("Clear it first: truncate -s 0 \"Daily Notes/The daily takes pool.md\"")
        print()
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Find all daily note files
    # NOTE: this pattern match is pretty strict, might need tweaking for different naming conventions
    pattern = os.path.join(base_dir, "**/*.md")
    files = []
    for f in glob.glob(pattern, recursive=True):
        if os.path.basename(f) != "The daily takes pool.md":
            if re.match(r'\w+\s+\d{1,2}\s+\w+\.md$', os.path.basename(f)):
                files.append(f)
    
    # Sort by date - regex pulls YYYY/MM/DD from path
    def get_date_key(filepath):
        match = re.search(r'(\d{4})/(\d{2}).*?(\d{1,2})\s+\w+\.md$', filepath)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return (0, 0, 0)
    
    files.sort(key=get_date_key)
    
    # Extract takes
    all_takes = []
    for filepath in files:
        takes = extract_takes(filepath)
        if takes:
            link = get_obsidian_link(filepath)
            for take in takes:
                all_takes.append(f"{take} {link}")
    
    if not all_takes:
        print("No takes found.")
        return
    
    # Write to pool file (append mode)
    file_exists = os.path.exists(pool_file) and os.path.getsize(pool_file) > 0
    
    with open(pool_file, 'a', encoding='utf-8') as f:
        if not file_exists:
            f.write("Daily note takes :\n")
        
        for take in all_takes:
            f.write(f"\n- {take}\n")
    
    print(f"✅ Added {len(all_takes)} takes to pool")
    print()
    print("Tip: Use this alias to avoid dupes:")
    print('   alias takes=\'truncate -s 0 "Daily Notes/The daily takes pool.md" && python3 extract_daily_takes.py\'')


if __name__ == "__main__":
    main()
