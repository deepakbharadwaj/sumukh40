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
    
    # Create the main HTML content with updated darker theme
    html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Slam Book - Main Page</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Dancing+Script:wght@400;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body {{
        font-family: "Inter", sans-serif;
        background: linear-gradient(135deg, 
          rgba(71, 85, 105, 1) 0%, 
          rgba(55, 65, 81, 1) 25%, 
          rgba(75, 85, 99, 1) 50%, 
          rgba(55, 65, 81, 1) 75%, 
          rgba(67, 56, 202, 1) 100%);
        min-height: 100vh;
        overflow-x: hidden;
        position: relative;
      }}

      /* Enhanced background pattern with darker theme */
      body::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
          radial-gradient(circle at 25% 25%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 75% 25%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 25% 75%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 75% 75%, rgba(16, 185, 129, 0.1) 0%, transparent 50%);
        background-size: 250px 250px, 200px 200px, 220px 220px, 280px 280px;
        z-index: -2;
        animation: patternMove 25s ease-in-out infinite;
      }}

      @keyframes patternMove {{
        0%, 100% {{ background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%; }}
        50% {{ background-position: 30% 30%, 70% 30%, 30% 70%, 70% 70%; }}
      }}

      /* Animated stickers */
      .animated-sticker {{
        position: absolute;
        font-size: 1.5rem;
        animation: floatSticker 8s ease-in-out infinite;
        opacity: 0.6;
        pointer-events: none;
        z-index: 1;
      }}

      .sticker-1 {{ top: 8%; left: 5%; animation-delay: 0s; }}
      .sticker-2 {{ top: 12%; right: 6%; animation-delay: 1s; }}
      .sticker-3 {{ bottom: 25%; left: 4%; animation-delay: 2s; }}
      .sticker-4 {{ bottom: 12%; right: 8%; animation-delay: 3s; }}
      .sticker-5 {{ top: 40%; left: 2%; animation-delay: 1.5s; }}
      .sticker-6 {{ top: 60%; right: 3%; animation-delay: 2.5s; }}

      @keyframes floatSticker {{
        0%, 100% {{ 
          transform: translateY(0px) translateX(0px) rotate(0deg) scale(1); 
          opacity: 0.6; 
        }}
        25% {{ 
          transform: translateY(-15px) translateX(8px) rotate(3deg) scale(1.05); 
          opacity: 0.8; 
        }}
        50% {{ 
          transform: translateY(-25px) translateX(-3px) rotate(-2deg) scale(0.95); 
          opacity: 0.4; 
        }}
        75% {{ 
          transform: translateY(-10px) translateX(-8px) rotate(1deg) scale(1.02); 
          opacity: 0.7; 
        }}
      }}

      /* Enhanced sparkles */
      .sparkle {{
        position: absolute;
        width: 5px;
        height: 5px;
        background: linear-gradient(45deg, #fbbf24, #f59e0b);
        border-radius: 50%;
        animation: sparkleShine 4s ease-in-out infinite;
        opacity: 0.7;
        z-index: 1;
      }}

      .sparkle:nth-child(7) {{ top: 15%; left: 20%; animation-delay: 0s; }}
      .sparkle:nth-child(8) {{ top: 30%; right: 15%; animation-delay: 1s; }}
      .sparkle:nth-child(9) {{ bottom: 40%; left: 22%; animation-delay: 2s; }}
      .sparkle:nth-child(10) {{ bottom: 20%; right: 25%; animation-delay: 3s; }}
      .sparkle:nth-child(11) {{ top: 50%; left: 10%; animation-delay: 1.5s; }}

      @keyframes sparkleShine {{
        0%, 100% {{ opacity: 0.4; transform: scale(1); }}
        50% {{ opacity: 1; transform: scale(1.6); }}
      }}

      /* Main container with enhanced elegance */
      .main-container {{
        background: linear-gradient(135deg, 
          rgba(255, 255, 255, 0.95) 0%, 
          rgba(248, 250, 252, 0.93) 50%, 
          rgba(241, 245, 249, 0.95) 100%);
        backdrop-filter: blur(25px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
          0 25px 50px rgba(0, 0, 0, 0.15),
          0 8px 32px rgba(139, 92, 246, 0.15),
          inset 0 1px 0 rgba(255, 255, 255, 0.7);
        position: relative;
        overflow: hidden;
        z-index: 10;
      }}

      .main-container::before {{
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.3), 
          rgba(236, 72, 153, 0.3), 
          rgba(59, 130, 246, 0.3), 
          rgba(16, 185, 129, 0.3));
        border-radius: inherit;
        z-index: -1;
        animation: borderGlow 5s ease-in-out infinite;
      }}

      @keyframes borderGlow {{
        0%, 100% {{ opacity: 0.4; }}
        50% {{ opacity: 0.7; }}
      }}

      /* Enhanced title */
      .title-gradient {{
        background: linear-gradient(135deg, 
          #8b5cf6 0%, 
          #ec4899 25%, 
          #3b82f6 50%, 
          #10b981 75%, 
          #f59e0b 100%);
        background-size: 300% 300%;
        animation: elegantGradient 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: "Playfair Display", serif;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      }}

      @keyframes elegantGradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
      }}

      /* Cover image with enhanced oscillation */
      .cover-image {{
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.9), 
          rgba(236, 72, 153, 0.9), 
          rgba(59, 130, 246, 0.9), 
          rgba(16, 185, 129, 0.9));
        background-size: 400% 400%;
        padding: 8px;
        border-radius: 24px;
        animation: coverSwingAndGlow 5s ease-in-out infinite;
        box-shadow: 
          0 0 50px rgba(139, 92, 246, 0.4),
          0 16px 50px rgba(0, 0, 0, 0.2);
        position: relative;
      }}

      .cover-image::before {{
        content: "";
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        background: linear-gradient(45deg, 
          rgba(255, 255, 255, 0.4), 
          rgba(255, 255, 255, 0.1));
        border-radius: 28px;
        z-index: -1;
        animation: coverShimmer 3s ease infinite;
      }}

      @keyframes coverSwingAndGlow {{
        0% {{ 
          background-position: 0% 50%; 
          transform: rotate(-10deg); 
        }}
        25% {{ 
          background-position: 50% 50%; 
          transform: rotate(0deg); 
        }}
        50% {{ 
          background-position: 100% 50%; 
          transform: rotate(10deg); 
        }}
        75% {{ 
          background-position: 50% 50%; 
          transform: rotate(0deg); 
        }}
        100% {{ 
          background-position: 0% 50%; 
          transform: rotate(-10deg); 
        }}
      }}

      @keyframes coverShimmer {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
      }}

      .cover-image:hover {{
        animation-play-state: paused;
        transform: scale(1.05) rotate(0deg);
      }}

      /* Enhanced person cards */
      .person-card {{
        background: linear-gradient(135deg, 
          rgba(255, 255, 255, 0.95) 0%, 
          rgba(248, 250, 252, 0.9) 100%);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
      }}

      .person-card::before {{
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
          transparent, 
          rgba(139, 92, 246, 0.1), 
          transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
        opacity: 0;
      }}

      .person-card:hover {{
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
        border-color: rgba(139, 92, 246, 0.4);
      }}

      .person-card:hover::before {{
        opacity: 1;
        transform: rotate(45deg) translate(20%, 20%);
      }}

      /* Photo frames in person cards */
      .person-photo {{
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.8), 
          rgba(236, 72, 153, 0.8));
        padding: 3px;
        border-radius: 50%;
        animation: photoGlow 4s ease infinite;
      }}

      @keyframes photoGlow {{
        0%, 100% {{ box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); }}
        50% {{ box-shadow: 0 0 25px rgba(236, 72, 153, 0.4); }}
      }}

      /* Decorative elements */
      .decorative-line {{
        background: linear-gradient(90deg, 
          transparent, 
          rgba(139, 92, 246, 0.4), 
          rgba(236, 72, 153, 0.4), 
          rgba(139, 92, 246, 0.4), 
          transparent);
        height: 3px;
        border-radius: 3px;
        position: relative;
        overflow: hidden;
      }}

      .decorative-line::before {{
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
          transparent, 
          rgba(255, 255, 255, 0.8), 
          transparent);
        animation: lineShimmer 4s ease infinite;
      }}

      @keyframes lineShimmer {{
        0% {{ left: -100%; }}
        100% {{ left: 100%; }}
      }}

      /* Custom scrollbar */
      ::-webkit-scrollbar {{
        width: 10px;
      }}
      ::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.2);
        border-radius: 5px;
      }}
      ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, rgba(139, 92, 246, 0.6), rgba(236, 72, 153, 0.6));
        border-radius: 5px;
      }}
      ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, rgba(139, 92, 246, 0.8), rgba(236, 72, 153, 0.8));
      }}

      /* Typography */
      .subtitle-text {{
        font-family: "Inter", sans-serif;
        font-weight: 600;
        color: #374151;
      }}

      .footer-text {{
        font-family: "Dancing Script", cursive;
        font-weight: 600;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }}

      /* Mobile responsiveness */
      @media (max-width: 768px) {{
        .animated-sticker {{
          font-size: 1.2rem;
          opacity: 0.4;
        }}
        
        .main-container {{
          margin: 0.5rem;
          padding: 1.5rem;
        }}
        
        .title-gradient {{
          font-size: 3rem;
        }}
      }}
    </style>
  </head>
  <body class="p-2 sm:p-4 md:p-6 lg:p-8 min-h-screen relative">
    <!-- Animated stickers -->
    <div class="animated-sticker sticker-1">🎉</div>
    <div class="animated-sticker sticker-2">🎂</div>
    <div class="animated-sticker sticker-3">✨</div>
    <div class="animated-sticker sticker-4">🎈</div>
    <div class="animated-sticker sticker-5">🌟</div>
    <div class="animated-sticker sticker-6">🎊</div>
    
    <!-- Enhanced sparkles -->
    <div class="sparkle"></div>
    <div class="sparkle"></div>
    <div class="sparkle"></div>
    <div class="sparkle"></div>
    <div class="sparkle"></div>

    <div class="main-container p-6 sm:p-8 md:p-10 lg:p-12 max-w-6xl mx-auto rounded-3xl">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <div class="decorative-line mb-8 w-48 mx-auto"></div>
        <h1 class="title-gradient text-5xl sm:text-6xl md:text-7xl font-bold mb-6 leading-tight">
          🎉 SLAM BOOK 🎉
        </h1>
        <h2 class="subtitle-text text-2xl sm:text-3xl mb-4">
          A Collection of Memories & Messages
        </h2>
        <p class="text-lg text-gray-600 mb-2">
          Click on any person's card to read their special messages
        </p>
        <div class="decorative-line mt-8 w-48 mx-auto"></div>
      </div>

      <!-- Cover Image Section -->
      <div class="text-center mb-16">
        <div class="cover-image inline-block">
          <img
            src="mainPage.png"
            alt="Slam Book Cover"
            class="w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 rounded-2xl shadow-2xl object-cover"
          />
        </div>
      </div>

      <!-- People Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
"""

    # Add person cards with enhanced styling
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
        <div class="person-card p-8 rounded-3xl shadow-lg cursor-pointer" onclick="window.open('{html_filename}', '_blank')">
          <div class="text-center">
            <div class="person-photo w-28 h-28 mx-auto mb-6 rounded-full overflow-hidden shadow-xl">
              <img
                src="{photo_src}"
                alt="{name}'s Photo"
                class="w-full h-full object-cover rounded-full"
              />
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-3">{name}</h3>
            <p class="text-sm text-gray-600 mb-6">Click to read their messages</p>
            <div class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-full text-sm font-semibold shadow-lg hover:shadow-xl transition-all duration-300">
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
        <div class="decorative-line mb-6 w-64 mx-auto"></div>
        <p class="footer-text">
          ✨ Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | {len(people_data)} Entries ✨
        </p>
        <div class="decorative-line mt-6 w-64 mx-auto"></div>
      </div>
    </div>

    <script>
      // Enhanced interactive effects
      document.addEventListener('DOMContentLoaded', function() {{
        const cards = document.querySelectorAll('.person-card');
        
        cards.forEach(card => {{
          card.addEventListener('mouseenter', function() {{
            this.style.transform = 'translateY(-12px) scale(1.05)';
            this.style.transition = 'all 0.4s ease';
          }});
          
          card.addEventListener('mouseleave', function() {{
            this.style.transform = 'translateY(0) scale(1)';
            this.style.transition = 'all 0.4s ease';
          }});
        }});

        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
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
        print(f"📸 Cover image: mainPage.png")
        print(f"👥 Total entries: {len(people_data)}")
        
        print(f"\n🎨 Features of the main slam book page:")
        print("   • Beautiful elegant design with darker backgrounds")
        print("   • Animated stickers and floating elements")
        print("   • Cover image with enhanced oscillating border animation")
        print("   • Interactive person cards with sophisticated hover effects")
        print("   • Click to open individual slam book pages")
        print("   • Enhanced mobile responsive design")
        print("   • Professional typography and spacing")
        print("   • Consistent with individual page styling")
        print("   • Ready to open in any web browser")
            
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")

if __name__ == "__main__":
    main() 