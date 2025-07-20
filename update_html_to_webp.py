#!/usr/bin/env python3
"""
Update HTML Files to Use WebP Images
Updates all HTML files to reference WebP images instead of JPG/PNG for faster loading
"""

import os
import re
import glob
from pathlib import Path

def update_html_file_to_webp(file_path):
    """Update a single HTML file to use WebP images"""
    try:
        print(f"📝 Updating: {os.path.basename(file_path)}")
        
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        changes_made = 0
        
        # Pattern to match image src attributes with jpg/jpeg/png extensions
        # This covers both relative and absolute paths
        patterns = [
            # Match src="photo_XX_Name.jpg" or src="output/photo_XX_Name.jpg"
            (r'src="((?:output/)?photo_\d{2}_[^"]+)\.jpg"', r'src="\1.webp"'),
            (r'src="((?:output/)?photo_\d{2}_[^"]+)\.jpeg"', r'src="\1.webp"'),
            (r'src="((?:output/)?photo_\d{2}_[^"]+)\.png"', r'src="\1.webp"'),
            
            # Match imageUrl: "output/photo_XX_Name.jpg" in JavaScript objects
            (r'imageUrl: "(output/photo_\d{2}_[^"]+)\.jpg"', r'imageUrl: "\1.webp"'),
            (r'imageUrl: "(output/photo_\d{2}_[^"]+)\.jpeg"', r'imageUrl: "\1.webp"'),
            (r'imageUrl: "(output/photo_\d{2}_[^"]+)\.png"', r'imageUrl: "\1.webp"'),
            
            # Match any other image references (more generic)
            (r'(["\'])([^"\']*photo_\d{2}_[^"\']*)\.jpg(["\'])', r'\1\2.webp\3'),
            (r'(["\'])([^"\']*photo_\d{2}_[^"\']*)\.jpeg(["\'])', r'\1\2.webp\3'),
            (r'(["\'])([^"\']*photo_\d{2}_[^"\']*)\.png(["\'])', r'\1\2.webp\3'),
        ]
        
        # Apply all patterns
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                changes_made += count
                content = new_content
                print(f"   ✅ Applied pattern: {count} replacements")
        
        # Write back if changes were made
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"   💾 Saved {changes_made} changes to {os.path.basename(file_path)}")
            return True
        else:
            print(f"   ℹ️ No changes needed for {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error updating {os.path.basename(file_path)}: {str(e)}")
        return False

def update_generation_script_to_webp():
    """Update the generation script to use WebP format by default"""
    script_path = "generate_html_slam_book.py"
    
    try:
        print(f"🔧 Updating generation script: {script_path}")
        
        with open(script_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        changes_made = 0
        
        # Update the download_and_save_image function to save as WebP
        patterns = [
            # Update photo filename creation
            (r'photo_filename = f"photo_{row_num:02d}_{safe_name}\.jpg"', 
             r'photo_filename = f"photo_{row_num:02d}_{safe_name}.webp"'),
            
            # Update any hardcoded jpg references
            (r'\.jpg"', r'.webp"'),
            (r'\.jpeg"', r'.webp"'),
            
            # Update file extension in comments or strings
            (r'# Save as JPG', r'# Save as WebP'),
            (r'# Download.*JPG', r'# Download as WebP'),
        ]
        
        for pattern, replacement in patterns:
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                changes_made += count
                content = new_content
        
        if changes_made > 0:
            with open(script_path, 'w', encoding='utf-8') as file:
                file.write(content)
            print(f"   ✅ Updated generation script with {changes_made} changes")
            return True
        else:
            print(f"   ℹ️ Generation script already uses WebP format")
            return False
            
    except FileNotFoundError:
        print(f"   ⚠️ Generation script not found: {script_path}")
        return False
    except Exception as e:
        print(f"   ❌ Error updating generation script: {str(e)}")
        return False

def find_html_files():
    """Find all HTML files that need to be updated"""
    html_files = []
    
    # Find HTML files in output directory
    output_files = glob.glob("output/*.html")
    html_files.extend(output_files)
    
    # Find main index.html
    if os.path.exists("index.html"):
        html_files.append("index.html")
    
    # Find any other HTML files in root
    root_files = glob.glob("*.html")
    for file in root_files:
        if file not in html_files:
            html_files.append(file)
    
    return html_files

def verify_webp_images_exist():
    """Verify that WebP images exist in the output directory"""
    webp_files = glob.glob("output/*.webp")
    jpg_files = glob.glob("output/photo_*.jpg")
    
    print(f"🔍 Found {len(webp_files)} WebP files and {len(jpg_files)} JPG files")
    
    if len(webp_files) == 0:
        print("⚠️ No WebP images found! Please run the download script first:")
        print("   python download_and_convert_images.py")
        return False
    
    return True

def main():
    """Main function to update all HTML files to use WebP images"""
    print("🔄 Starting HTML to WebP update process...")
    print("=" * 60)
    
    # Verify WebP images exist
    if not verify_webp_images_exist():
        return False
    
    # Find all HTML files
    html_files = find_html_files()
    
    if not html_files:
        print("❌ No HTML files found to update")
        return False
    
    print(f"📋 Found {len(html_files)} HTML files to process:")
    for file in html_files:
        print(f"   • {file}")
    
    print("\n" + "=" * 60)
    
    # Update each HTML file
    updated_count = 0
    error_count = 0
    
    for file_path in html_files:
        if update_html_file_to_webp(file_path):
            updated_count += 1
        else:
            # Check if it's an error or just no changes needed
            if os.path.exists(file_path):
                # File exists but no changes made - not an error
                pass
            else:
                error_count += 1
        print()  # Empty line for readability
    
    # Update generation script
    print("🔧 Updating generation scripts...")
    update_generation_script_to_webp()
    print()
    
    # Summary
    print("=" * 60)
    print("📊 UPDATE SUMMARY")
    print("=" * 60)
    print(f"✅ Files updated: {updated_count}")
    print(f"ℹ️ Files with no changes: {len(html_files) - updated_count - error_count}")
    print(f"❌ Errors: {error_count}")
    
    if updated_count > 0:
        print(f"\n🎉 Successfully updated HTML files to use WebP images!")
        print(f"📈 Expected performance improvements:")
        print(f"   • Faster page load times (WebP is 25-35% smaller than JPG)")
        print(f"   • Better compression with same visual quality")
        print(f"   • Improved user experience on slower connections")
    else:
        print(f"\n✅ All HTML files are already using WebP format!")
    
    print(f"\n🌐 You can now open the HTML files in a browser to see the improvements.")
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🏆 HTML to WebP conversion completed successfully!")
    else:
        print("\n💥 Process completed with errors. Check the log above.") 