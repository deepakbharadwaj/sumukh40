#!/usr/bin/env python3
"""
Main Slam Book Generator
Creates a main page that acts as a slam book cover with links to individual pages
"""

import csv
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup

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

def create_main_slam_book_page(people_data, output_dir):
    """Create the main slam book page with cover and links"""
    
    # Create the main HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Slam Book - Main Page</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Dancing+Script:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body {{
        font-family: "Inter", sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        overflow-x: hidden;
      }}

      /* Animated stars */
      .star {{
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s infinite;
      }}

      .star:nth-child(1) {{ width: 3px; height: 3px; top: 10%; left: 10%; animation-delay: 0s; }}
      .star:nth-child(2) {{ width: 2px; height: 2px; top: 20%; left: 80%; animation-delay: 0.5s; }}
      .star:nth-child(3) {{ width: 4px; height: 4px; top: 30%; left: 20%; animation-delay: 1s; }}
      .star:nth-child(4) {{ width: 2px; height: 2px; top: 40%; left: 90%; animation-delay: 1.5s; }}
      .star:nth-child(5) {{ width: 3px; height: 3px; top: 50%; left: 5%; animation-delay: 2s; }}
      .star:nth-child(6) {{ width: 2px; height: 2px; top: 60%; left: 85%; animation-delay: 2.5s; }}
      .star:nth-child(7) {{ width: 4px; height: 4px; top: 70%; left: 15%; animation-delay: 0.3s; }}
      .star:nth-child(8) {{ width: 3px; height: 3px; top: 80%; left: 75%; animation-delay: 0.8s; }}
      .star:nth-child(9) {{ width: 2px; height: 2px; top: 90%; left: 25%; animation-delay: 1.3s; }}
      .star:nth-child(10) {{ width: 3px; height: 3px; top: 15%; left: 60%; animation-delay: 1.8s; }}

      @keyframes twinkle {{
        0%, 100% {{ opacity: 0.3; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.2); }}
      }}

      /* Floating particles */
      .particle {{
        position: absolute;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
      }}

      .particle:nth-child(11) {{ width: 8px; height: 8px; top: 5%; left: 15%; animation-delay: 0s; }}
      .particle:nth-child(12) {{ width: 6px; height: 6px; top: 15%; left: 85%; animation-delay: 1s; }}
      .particle:nth-child(13) {{ width: 10px; height: 10px; top: 25%; left: 25%; animation-delay: 2s; }}
      .particle:nth-child(14) {{ width: 7px; height: 7px; top: 35%; left: 95%; animation-delay: 3s; }}
      .particle:nth-child(15) {{ width: 9px; height: 9px; top: 45%; left: 10%; animation-delay: 4s; }}

      @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
        50% {{ transform: translateY(-20px) rotate(180deg); }}
      }}

      /* Main container */
      .main-container {{
        background: 
          radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
          radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
          radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%),
          linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%);
        backdrop-filter: blur(10px);
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
      }}

      .main-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        border-radius: inherit;
        padding: 3px;
        mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
        mask-composite: exclude;
        z-index: -1;
      }}

      /* Enhanced title */
      .title-gradient {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }}

      @keyframes gradientShift {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
      }}

      /* Cover image with oscillation */
      .cover-image {{
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        padding: 6px;
        border-radius: 20px;
        animation: swing 4s ease-in-out infinite;
      }}

      .cover-image:hover {{
        animation-play-state: paused;
      }}

      @keyframes swing {{
        0%   {{ transform: rotate(-20deg); }}
        10%  {{ transform: rotate(-15deg); }}
        25%  {{ transform: rotate(0deg); }}
        50%  {{ transform: rotate(20deg); }}
        75%  {{ transform: rotate(0deg); }}
        90%  {{ transform: rotate(-15deg); }}
        100% {{ transform: rotate(-20deg); }}
      }}

      /* Person cards */
      .person-card {{
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.2) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
      }}

      .person-card:hover {{
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border-color: rgba(102, 126, 234, 0.5);
      }}

      /* Decorative elements */
      .decorative-line {{
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        height: 2px;
        border-radius: 1px;
      }}

      /* Custom scrollbar */
      ::-webkit-scrollbar {{
        width: 8px;
      }}
      ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
      }}
      ::-webkit-scrollbar-thumb {{
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
        border-radius: 10px;
      }}
      ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(45deg, #ff5252, #26a69a);
      }}
    </style>
  </head>
  <body class="p-4 sm:p-6 md:p-8 lg:p-10 min-h-screen relative">
    <!-- Animated background elements -->
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>

    <div class="main-container p-6 sm:p-8 md:p-10 lg:p-12 max-w-6xl mx-auto rounded-3xl shadow-2xl">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <div class="decorative-line mb-6"></div>
        <h1 class="title-gradient text-6xl sm:text-7xl font-extrabold mb-4">
          🎉 SLAM BOOK 🎉
        </h1>
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-700 mb-2">
          A Collection of Memories & Messages
        </h2>
        <p class="text-lg text-gray-600">
          Click on any person's card to read their special messages
        </p>
        <div class="decorative-line mt-6"></div>
      </div>

      <!-- Cover Image Section -->
      <div class="text-center mb-12">
        <div class="cover-image inline-block">
                     <img
             src="mainPage.png"
             alt="Slam Book Cover"
             class="w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 rounded-2xl shadow-2xl object-cover"
           />
        </div>
      </div>

      <!-- People Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
"""

    # Add person cards
    for i, (person_data, html_filename) in enumerate(people_data, 1):
        name = extract_name_from_data(person_data)
        safe_name = re.sub(r'[^\w\s-]', '', name).strip()
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        
        # Get photo filename if it exists
        photo_filename = f"photo_{i:02d}_{safe_name}.jpg"
        photo_path = os.path.join(output_dir, photo_filename)
        photo_src = photo_filename if os.path.exists(photo_path) else "https://placehold.co/200x200/fcd34d/78350f?text=Photo"
        
        html_content += f"""
        <!-- Person {i} -->
        <div class="person-card p-6 rounded-3xl shadow-lg cursor-pointer" onclick="window.open('{html_filename}', '_blank')">
          <div class="text-center">
            <div class="w-24 h-24 mx-auto mb-4 rounded-full overflow-hidden shadow-lg border-4 border-white">
              <img
                src="{photo_src}"
                alt="{name}'s Photo"
                class="w-full h-full object-cover"
              />
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">{name}</h3>
            <p class="text-sm text-gray-600 mb-4">Click to read their messages</p>
            <div class="bg-gradient-to-r from-purple-400 to-pink-400 text-white px-4 py-2 rounded-full text-sm font-semibold">
              📖 Open Slam Book
            </div>
          </div>
        </div>
"""

    # Close the HTML
    html_content += f"""
      </div>

      <!-- Footer -->
      <div class="text-center">
        <div class="decorative-line mb-4"></div>
        <p class="text-gray-600 text-sm">
          ✨ Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | {len(people_data)} Entries ✨
        </p>
        <div class="decorative-line mt-4"></div>
      </div>
    </div>

    <script>
      // Add some interactive effects
      document.addEventListener('DOMContentLoaded', function() {{
        const cards = document.querySelectorAll('.person-card');
        cards.forEach(card => {{
          card.addEventListener('mouseenter', function() {{
            this.style.transform = 'translateY(-10px) scale(1.05)';
          }});
          card.addEventListener('mouseleave', function() {{
            this.style.transform = 'translateY(0) scale(1)';
          }});
        }});
      }});
    </script>
  </body>
</html>
"""
    
    # Save the main HTML file
    main_html_filename = os.path.join(output_dir, "main_slam_book.html")
    with open(main_html_filename, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"Generated: {main_html_filename}")
    return main_html_filename

def main():
    """Main function to create the main slam book page"""
    
    # Ensure output directory exists
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if mainPage.png exists
    main_page_image = "mainPage.png"
    if not os.path.exists(main_page_image):
        print(f"❌ Error: Could not find {main_page_image}")
        return
    
    # Copy mainPage.png to output directory
    import shutil
    output_image_path = os.path.join(output_dir, "mainPage.png")
    shutil.copy2(main_page_image, output_image_path)
    print(f"✅ Copied {main_page_image} to output directory")
    
    # Read the CSV file to get people data
    csv_file = "slam.csv"
    people_data = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Process each row (person)
            for row_num, row in enumerate(reader, 1):
                # Skip rows with no meaningful data
                if not any(row.values()):
                    continue
                
                # Create HTML filename for this person
                name = extract_name_from_data(row)
                safe_name = re.sub(r'[^\w\s-]', '', name).strip()
                safe_name = re.sub(r'[-\s]+', '_', safe_name)
                html_filename = f"slam_page_{row_num:02d}_{safe_name}.html"
                
                people_data.append((row, html_filename))
        
        # Create the main slam book page
        main_file = create_main_slam_book_page(people_data, output_dir)
        
        print(f"\n✅ Successfully generated main slam book page!")
        print(f"📁 Main page saved as: main_slam_book.html")
        print(f"📸 Cover image: mainPage.jpg")
        print(f"👥 Total entries: {len(people_data)}")
        
        print(f"\n🎨 Features of the main slam book page:")
        print("   • Beautiful animated design with stars and particles")
        print("   • Cover image with rotating border animation")
        print("   • Interactive person cards with hover effects")
        print("   • Click to open individual slam book pages")
        print("   • Responsive design for all devices")
        print("   • Professional typography and spacing")
        print("   • Ready to open in any web browser")
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")

if __name__ == "__main__":
    main() 