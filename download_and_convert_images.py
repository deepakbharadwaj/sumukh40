#!/usr/bin/env python3
"""
Download and Convert Images to WebP
Downloads images from Google Drive links in slam.csv and converts them to WebP format for faster web loading
"""

import csv
import os
import re
import requests
import time
from PIL import Image
from urllib.parse import urlparse, parse_qs
import io
import glob

def extract_google_drive_id(drive_url):
    """Extract file ID from Google Drive URL"""
    if not drive_url or drive_url.strip() == "":
        return None
    
    # Remove any extra whitespace
    drive_url = drive_url.strip()
    
    # Pattern 1: https://drive.google.com/file/d/FILE_ID/view?usp=...
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_url)
    if match:
        return match.group(1)
    
    # Pattern 2: https://drive.google.com/open?id=FILE_ID
    match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', drive_url)
    if match:
        return match.group(1)
    
    # Pattern 3: https://drive.google.com/drive/folders/... (not supported)
    if 'folders' in drive_url:
        print(f"⚠️ Folder URL not supported: {drive_url}")
        return None
    
    print(f"⚠️ Could not extract file ID from: {drive_url}")
    return None

def download_image_from_google_drive(file_id, output_path):
    """Download image from Google Drive using file ID"""
    if not file_id:
        return False
    
    # Google Drive direct download URL
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        print(f"   📥 Downloading from Google Drive...")
        
        # Send request with a reasonable timeout
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(download_url, headers=headers, timeout=30)
        
        # Check if we got redirected to a confirmation page (for large files)
        if "confirm=" in response.url or "virus scan warning" in response.text.lower():
            # Try to extract the actual download URL from the confirmation page
            confirm_match = re.search(r'confirm=([^&]+)', response.url)
            if confirm_match:
                confirm_token = confirm_match.group(1)
                download_url = f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}"
                response = requests.get(download_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            # Verify it's actually an image
            content_type = response.headers.get('content-type', '').lower()
            if 'image' not in content_type:
                print(f"   ⚠️ Downloaded file may not be an image (content-type: {content_type})")
            
            with open(output_path, 'wb') as file:
                file.write(response.content)
            
            print(f"   ✅ Downloaded: {os.path.basename(output_path)} ({len(response.content)} bytes)")
            return True
        else:
            print(f"   ❌ Failed to download: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Network error: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {str(e)}")
        return False

def convert_image_to_webp(input_path, output_path, quality=85):
    """Convert image to WebP format with specified quality"""
    try:
        print(f"   🔄 Converting to WebP...")
        
        # Open and convert the image
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (WebP doesn't support all modes)
            if img.mode in ('RGBA', 'LA'):
                # For images with transparency, keep as RGBA
                pass
            elif img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Save as WebP with specified quality
            img.save(output_path, 'WebP', quality=quality, optimize=True)
            
            # Get file size info
            original_size = os.path.getsize(input_path)
            webp_size = os.path.getsize(output_path)
            compression_ratio = ((original_size - webp_size) / original_size) * 100
            
            print(f"   ✅ WebP created: {os.path.basename(output_path)}")
            print(f"      Original: {original_size:,} bytes, WebP: {webp_size:,} bytes")
            print(f"      Compression: {compression_ratio:.1f}% smaller")
            
            return True
            
    except Exception as e:
        print(f"   ❌ Conversion error: {str(e)}")
        return False

def create_photo_filename(full_name, index):
    """Create standardized photo filename"""
    # Clean the name for filename
    safe_name = re.sub(r'[^\w\s-]', '', full_name)
    safe_name = re.sub(r'\s+', '_', safe_name)
    safe_name = safe_name.strip('_')
    
    if not safe_name:
        safe_name = "Anonymous"
    
    return f"photo_{index:02d}_{safe_name}"

def clean_up_jpg_files(output_dir):
    """Remove existing JPG files that are no longer needed"""
    jpg_files = glob.glob(os.path.join(output_dir, "photo_*.jpg"))
    jpeg_files = glob.glob(os.path.join(output_dir, "photo_*.jpeg"))
    png_files = glob.glob(os.path.join(output_dir, "photo_*.png"))
    
    all_old_files = jpg_files + jpeg_files + png_files
    
    if all_old_files:
        print(f"\n🧹 Cleaning up {len(all_old_files)} old image files...")
        removed_count = 0
        for file_path in all_old_files:
            try:
                os.remove(file_path)
                print(f"   🗑️ Removed: {os.path.basename(file_path)}")
                removed_count += 1
            except Exception as e:
                print(f"   ⚠️ Could not remove {os.path.basename(file_path)}: {e}")
        
        print(f"   ✅ Cleaned up {removed_count} old image files")
    
    return len(all_old_files)

def process_slam_csv():
    """Process slam.csv and download/convert all images"""
    csv_file = "slam.csv"
    output_dir = "output"
    temp_dir = os.path.join(output_dir, "temp_downloads")
    
    # Create directories
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    success_count = 0
    error_count = 0
    processed_files = []
    
    print("🚀 Starting image download and WebP conversion process...")
    print(f"📁 Output directory: {output_dir}")
    print("=" * 60)
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row_num, row in enumerate(reader, 1):
                full_name = row.get('Full Name', '').strip()
                drive_url = row.get('Add a selfie or an old photo with him', '').strip()
                
                if not full_name:
                    full_name = f"Person_{row_num}"
                
                print(f"\n[{row_num}/51] Processing: {full_name}")
                
                if not drive_url or drive_url.strip() == "":
                    print("   ⚠️ No image URL provided, skipping...")
                    error_count += 1
                    continue
                
                # Extract Google Drive file ID
                file_id = extract_google_drive_id(drive_url)
                if not file_id:
                    error_count += 1
                    continue
                
                # Create filenames
                base_filename = create_photo_filename(full_name, row_num)
                temp_jpg_path = os.path.join(temp_dir, f"{base_filename}.jpg")
                final_webp_path = os.path.join(output_dir, f"{base_filename}.webp")
                
                # Skip if WebP already exists
                if os.path.exists(final_webp_path):
                    print(f"   ✅ WebP already exists: {os.path.basename(final_webp_path)}")
                    success_count += 1
                    processed_files.append(final_webp_path)
                    continue
                
                # Download the image
                if download_image_from_google_drive(file_id, temp_jpg_path):
                    # Convert to WebP
                    if convert_image_to_webp(temp_jpg_path, final_webp_path):
                        success_count += 1
                        processed_files.append(final_webp_path)
                        
                        # Clean up temporary JPG file immediately after conversion
                        try:
                            os.remove(temp_jpg_path)
                            print(f"   🗑️ Cleaned up temporary file")
                        except Exception as e:
                            print(f"   ⚠️ Could not remove temp file: {e}")
                    else:
                        error_count += 1
                        # Clean up temp file even if conversion failed
                        try:
                            os.remove(temp_jpg_path)
                        except:
                            pass
                else:
                    error_count += 1
                
                # Small delay to be respectful to Google's servers
                time.sleep(0.5)
    
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
    
    finally:
        # Clean up temp directory
        try:
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
        except:
            pass
    
    # Clean up any existing JPG/PNG files in output directory
    cleaned_files = clean_up_jpg_files(output_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DOWNLOAD AND CONVERSION SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully processed: {success_count} images")
    print(f"❌ Failed: {error_count} images")
    print(f"📁 Total WebP files created: {len(processed_files)}")
    print(f"🧹 Old JPG/PNG files removed: {cleaned_files}")
    
    if processed_files:
        print("\n📋 WebP files created:")
        for file_path in processed_files:
            print(f"   • {os.path.basename(file_path)}")
    
    # Calculate total space saved
    total_webp_size = sum(os.path.getsize(f) for f in processed_files if os.path.exists(f))
    print(f"\n💾 Total WebP files size: {total_webp_size:,} bytes ({total_webp_size/1024/1024:.1f} MB)")
    
    print(f"\n🎯 Next step: Run the update script to modify HTML files to use WebP images")
    print(f"   python update_html_to_webp.py")
    
    return success_count > 0

if __name__ == "__main__":
    success = process_slam_csv()
    if success:
        print("\n🎉 Image download and conversion completed successfully!")
        print("✨ All JPG files have been removed to save space - only optimized WebP files remain!")
    else:
        print("\n💥 Process completed with errors. Check the log above.") 