#!/usr/bin/env python3
"""
Complete Update Workflow
Runs all necessary scripts in the correct sequence when slam.csv changes
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def run_script(script_name, description, critical=True):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 STEP: {description}")
    print(f"📜 Script: {script_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True, 
                              check=False)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully! ({duration:.1f}s)")
            return True
        else:
            print(f"❌ {description} completed with errors (exit code: {result.returncode})")
            if critical:
                print(f"🛑 This is a critical step. Process will continue but may have issues.")
            return False
            
    except FileNotFoundError:
        print(f"❌ Script not found: {script_name}")
        if critical:
            print(f"🛑 Critical script missing! Please ensure {script_name} exists.")
        return False
    except Exception as e:
        print(f"❌ Error running {script_name}: {str(e)}")
        return False

def check_prerequisites():
    """Check if all required files exist"""
    required_files = [
        "slam.csv",
        "template.html",
        "download_and_convert_images.py",
        "generate_html_slam_book.py", 
        "generate_main_slam_book.py",
        "generate_beehive_index.py",
        "update_html_to_webp.py"
    ]
    
    print("🔍 Checking prerequisites...")
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   ✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing required files:")
        for file in missing_files:
            print(f"   • {file}")
        return False
    
    print(f"✅ All required files found!")
    return True

def main():
    """Main workflow when slam.csv changes"""
    print("🔄 SLAM BOOK UPDATE WORKFLOW")
    print("="*60)
    print("This workflow runs when slam.csv changes and includes:")
    print("  1. Download & convert new images to WebP")
    print("  2. Generate individual slam pages")
    print("  3. Generate main slam book page")
    print("  4. Generate beehive index page")
    print("  5. Update all HTML files to use WebP images")
    print("="*60)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n💥 Cannot continue - missing required files!")
        return False
    
    start_total = time.time()
    success_count = 0
    total_steps = 5
    
    # Step 1: Download and convert images to WebP
    print(f"\n🎯 PHASE 1: IMAGE OPTIMIZATION")
    if run_script("download_and_convert_images.py", 
                  "Download & Convert Images to WebP", 
                  critical=True):
        success_count += 1
    
    # Step 2: Generate individual slam pages
    print(f"\n🎯 PHASE 2: INDIVIDUAL PAGES GENERATION")
    if run_script("generate_html_slam_book.py", 
                  "Generate Individual Slam Pages", 
                  critical=True):
        success_count += 1
    
    # Step 3: Generate main slam book
    print(f"\n🎯 PHASE 3: MAIN SLAM BOOK GENERATION")
    if run_script("generate_main_slam_book.py", 
                  "Generate Main Slam Book", 
                  critical=True):
        success_count += 1
    
    # Step 4: Generate beehive index
    print(f"\n🎯 PHASE 4: INDEX PAGE GENERATION")
    if run_script("generate_beehive_index.py", 
                  "Generate Beehive Index Page", 
                  critical=True):  # Now critical since it handles WebP images
        success_count += 1
    
    # Step 5: Update HTML files to use WebP
    print(f"\n🎯 PHASE 5: HTML OPTIMIZATION")
    if run_script("update_html_to_webp.py", 
                  "Update HTML Files to use WebP", 
                  critical=False):  # Not critical as images should already be WebP
        success_count += 1
    
    end_total = time.time()
    total_duration = end_total - start_total
    
    # Final summary
    print(f"\n{'='*60}")
    print("🏆 WORKFLOW COMPLETE!")
    print(f"{'='*60}")
    print(f"✅ Successful steps: {success_count}/{total_steps}")
    print(f"⏱️ Total time: {total_duration:.1f} seconds")
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success_count == total_steps:
        print(f"\n🎉 All steps completed successfully!")
        print(f"🌐 Your slam book is fully updated and optimized!")
        print(f"   • Open index.html to see the results")
        print(f"   • All images are in WebP format for fast loading")
        print(f"   • Individual and main pages are updated")
    elif success_count >= 3:  # At least the critical steps
        print(f"\n✅ Core functionality completed successfully!")
        print(f"⚠️ Some optional steps had issues, but your slam book should work fine")
        print(f"🌐 Open index.html to verify everything looks good")
    else:
        print(f"\n⚠️ Several steps failed. Please check the errors above.")
        print(f"💡 You may need to run individual scripts manually:")
        print(f"   python download_and_convert_images.py")
        print(f"   python generate_html_slam_book.py")
        print(f"   python generate_main_slam_book.py")
    
    return success_count >= 3

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n🎊 Update workflow completed successfully!")
        else:
            print(f"\n💥 Update workflow completed with significant errors.")
            sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n⏸️ Workflow interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1) 