#!/usr/bin/env python3
"""
HTML Slam Book Generator
Creates personalized HTML pages from template.html using slam.csv data
"""

import csv
import os
import re
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def clean_text(text):
    """Clean and format text for display"""
    if not text or text.strip() == "":
        return None  # Return None for empty responses
    
    # Remove extra quotes and clean up
    text = text.strip().strip('"')
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    return text

def extract_name_from_data(person_data):
    """Extract name from various sources in the data"""
    
    # First try to get name from the "Full Name" column
    full_name = person_data.get('Full Name', '').strip()
    if full_name:
        return full_name
    
    # Try to extract from photo filename
    photo_filename = person_data.get('Add a selfie or an old photo with him', '')
    if photo_filename:
        # Extract name from Google Drive filename or other patterns
        name = extract_name_from_photo_filename(photo_filename)
        if name and name != "Anonymous":
            return name
    
    return "Anonymous"

def extract_name_from_photo_filename(filename):
    """Extract name from photo filename"""
    if not filename or filename.strip() == "":
        return "Anonymous"
    
    # Handle Google Drive links
    if "drive.google.com" in filename:
        return "Anonymous"
    
    # Remove file extension and clean up
    name = os.path.splitext(filename)[0]
    # Remove common prefixes and clean up
    name = re.sub(r'^(image|IMG|Screenshot|Sumukh_Anand)\s*[-_]\s*', '', name, flags=re.IGNORECASE)
    name = name.replace('_', ' ').replace('-', ' ')
    return name.strip()

def extract_google_drive_id(url):
    """Extract Google Drive file ID from URL"""
    if not url or "drive.google.com" not in url:
        return None
    
    try:
        parsed_url = urlparse(url)
        
        # Handle /open?id= format
        if parsed_url.path == '/open':
            query_params = parse_qs(parsed_url.query)
            return query_params.get('id', [None])[0]
        
        # Handle the /u/0/open format
        elif parsed_url.path.startswith('/u/0/open'):
            query_params = parse_qs(parsed_url.query)
            return query_params.get('id', [None])[0]
        
        # Handle the /file/d/{id}/view format
        elif parsed_url.path.startswith('/file/d/'):
            path_parts = parsed_url.path.split('/')
            if len(path_parts) >= 4:
                return path_parts[3]
    except:
        pass
    
    return None

def download_google_drive_image(drive_url, output_dir, person_name, page_num):
    """Download image from Google Drive and save it locally"""
    if not drive_url or "drive.google.com" not in drive_url:
        return None
    
    file_id = extract_google_drive_id(drive_url)
    if not file_id:
        return None
    
    # Create safe filename
    safe_name = re.sub(r'[^\w\s-]', '', person_name).strip()
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    image_filename = f"photo_{page_num:02d}_{safe_name}.webp"
    image_path = os.path.join(output_dir, image_filename)
    
    # Check if image already exists
    if os.path.exists(image_path):
        print(f"  ✅ Image already exists: {image_filename}")
        return image_filename
    
    # Create direct download URL
    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        # Download the image
        print(f"  Downloading image for {person_name}...")
        response = requests.get(direct_url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Save the image
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  ✅ Image saved: {image_filename}")
        return image_filename
        
    except Exception as e:
        print(f"  ❌ Failed to download image: {str(e)}")
        return None

def get_question_emoji(question_number):
    """Get emoji for question number"""
    emojis = {
        1: "🔧",
        2: "👴", 
        3: "🔄",
        4: "🏃",
        5: "💬",
        6: "⚠️",
        7: "💭",
        8: "🎂",
        9: "🎵",
        10: "🏆",
        11: "📺",
        12: "😎",
        13: "💎",
        14: "📝",
        15: "😤"
    }
    return emojis.get(question_number, "❓")

def get_card_class(question_number):
    """Get CSS class for card based on question number"""
    classes = {
        1: "card-bg-blue",
        2: "card-bg-green",
        3: "card-bg-red", 
        4: "card-bg-yellow",
        5: "card-bg-purple",
        6: "card-bg-pink",
        7: "card-bg-indigo",
        8: "card-bg-teal",
        9: "card-bg-orange",
        10: "card-bg-cyan",
        11: "card-bg-lime"
    }
    # Cycle through colors for questions beyond 11
    if question_number > 11:
        cycle_index = ((question_number - 1) % 11) + 1
        return classes[cycle_index]
    return classes.get(question_number, "card-bg-blue")

def create_html_slam_page(person_data, template_path, output_dir, page_num):
    """Create a single HTML slam book page for one person"""
    
    # Extract name
    name = extract_name_from_data(person_data)
    
    # Create HTML filename
    safe_name = re.sub(r'[^\w\s-]', '', name).strip()
    safe_name = re.sub(r'[-\s]+', '_', safe_name)
    html_filename = os.path.join(output_dir, f"slam_page_{page_num:02d}_{safe_name}.html")
    
    # Read the template
    with open(template_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
    
    # Update the name in the template - Updated selector to handle the new font-bold class
    name_span = soup.find('span', class_='text-purple-600 font-bold')
    if name_span:
        name_span.string = name
    else:
        # Fallback to the old selector
        name_span = soup.find('span', class_='text-purple-600')
        if name_span:
            name_span.string = name
    
    # Download and update photo
    photo_url = person_data.get('Add a selfie or an old photo with him', '')
    photo_filename = None
    if photo_url:
        photo_filename = download_google_drive_image(photo_url, output_dir, name, page_num)
    
    # Update the photo in the template
    photo_img = soup.find('img', alt='Your Photo')
    if photo_img and photo_filename:
        photo_img['src'] = photo_filename
        photo_img['alt'] = f"{name}'s Photo"
    elif photo_img:
        # Keep placeholder if no photo downloaded
        photo_img['alt'] = f"{name}'s Photo"
    
    # Get all CSV columns (excluding Timestamp, Full Name, and photo URL)
    csv_columns = list(person_data.keys())
    question_columns = csv_columns[2:-1]  # Skip Timestamp, Full Name, and photo URL
    
    # Process each question (columns 3-17 in CSV)
    question_count = 0
    
    # Fill the first question (next to the photo) - Updated selector to remove max-w-xl
    first_question_div = soup.find('div', class_='flex-grow card-bg-blue p-6 sm:p-8 rounded-3xl shadow-lg min-h-[280px] flex flex-col')
    if first_question_div and len(question_columns) > 0:
        first_answer = person_data.get(question_columns[0], "")
        clean_first_answer = clean_text(first_answer)
        if clean_first_answer is not None:
            textarea = first_question_div.find('textarea')
            if textarea:
                textarea.string = clean_first_answer
            question_count += 1
        else:
            first_question_div.decompose()

    # Fill the remaining questions (2-15) in the 2-column grid - Updated selector to use lg:grid-cols-2
    questions_container = soup.select_one('div.grid.grid-cols-1.lg\\:grid-cols-2')
    if questions_container:
        question_divs = questions_container.select('div[class*="card-bg-"]')
        for i, question_div in enumerate(question_divs):
            question_number = i + 2  # Questions 2-15
            if question_number <= len(question_columns):
                csv_column = question_columns[question_number - 1]
                answer = person_data.get(csv_column, "")
                clean_answer = clean_text(answer)
                if clean_answer is not None:
                    textarea = question_div.find('textarea')
                    if textarea:
                        textarea.string = clean_answer
                    question_count += 1
                else:
                    question_div.decompose()
    else:
        print(f"    ❌ Could not find questions container")
    
    # Update page title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = f"Slam Book - {name}"
    
    # Update footer with generation info - Updated to use the new footer-text class
    footer_text = soup.find('p', class_='footer-text')
    if footer_text:
        footer_text.string = f"✨ Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Page {page_num} ✨"
    else:
        # Fallback to the old selector
        footer_text = soup.find('p', class_='text-gray-600 text-sm')
        if footer_text:
            footer_text.string = f"✨ Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Page {page_num} ✨"
    
    # Save the HTML file
    with open(html_filename, 'w', encoding='utf-8') as file:
        file.write(str(soup))
    
    print(f"Generated: {html_filename} ({question_count} questions answered)")
    return html_filename

def main():
    """Main function to process slam.csv and generate HTML pages"""
    
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Template and CSV file paths
    template_path = "template.html"
    csv_file = "slam.csv"
    generated_files = []
    
    try:
        # Check if template exists
        if not os.path.exists(template_path):
            print(f"❌ Error: Could not find {template_path}")
            return
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Process each row (person)
            for row_num, row in enumerate(reader, 1):
                print(f"Processing row {row_num}...")
                
                # Skip rows with no meaningful data
                if not any(row.values()):
                    continue
                
                # Generate HTML page for this person
                html_file = create_html_slam_page(row, template_path, output_dir, row_num)
                if html_file:
                    generated_files.append(html_file)
        
        print(f"\n✅ Successfully generated {len(generated_files)} HTML slam book pages!")
        print(f"📁 All files saved in the '{output_dir}' folder")
        print("\n📋 Generated files:")
        for file in generated_files:
            print(f"   • {os.path.basename(file)}")
        
        print(f"\n🎨 Features of the generated HTML pages:")
        print("   • Beautiful elegant design with darker backgrounds")
        print("   • Animated stickers and floating elements")
        print("   • Personalized with each person's name")
        print("   • Real photos downloaded from Google Drive with oscillating frames")
        print("   • Shows ALL questions that were actually answered")
        print("   • Removes questions with no answers")
        print("   • Enhanced mobile responsive design")
        print("   • Interactive elements and sophisticated animations")
        print("   • Ready to open in any web browser")
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")

if __name__ == "__main__":
    main() 