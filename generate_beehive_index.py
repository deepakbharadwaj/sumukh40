#!/usr/bin/env python3
"""
Generate Bee Hive Index HTML
Dynamically creates the bee hive index page by scanning available slam book entries
"""

import os
import re
import glob
from datetime import datetime

def extract_name_from_filename(filename):
    """Extract clean name from filename"""
    # Remove file extension and page prefix
    name = filename.replace('slam_page_', '').replace('.html', '')
    # Remove leading numbers and underscores
    name = re.sub(r'^\d+_', '', name)
    # Replace underscores with spaces
    name = name.replace('_', ' ')
    return name

def scan_slam_book_entries():
    """Scan output folder for slam book entries and photos"""
    output_dir = 'output'
    entries = []
    
    if not os.path.exists(output_dir):
        print(f"Error: {output_dir} directory not found!")
        return entries
    
    # Get all slam page HTML files
    slam_pages = glob.glob(os.path.join(output_dir, 'slam_page_*.html'))
    slam_pages.sort()  # Sort to maintain order
    
    # Fallback image for entries without photos
    fallback_image = 'output/mainPage.png'
    
    for slam_page in slam_pages:
        filename = os.path.basename(slam_page)
        
        # Extract number and name from filename
        match = re.match(r'slam_page_(\d+)_(.+)\.html', filename)
        if match:
            number = match.group(1)
            name_part = match.group(2)
            
            # Look for corresponding photo
            photo_patterns = [
                f'photo_{number}_{name_part}.jpg',
                f'photo_{number}_{name_part}.jpeg',
                f'photo_{number}_{name_part}.png'
            ]
            
            photo_file = None
            for pattern in photo_patterns:
                photo_path = os.path.join(output_dir, pattern)
                if os.path.exists(photo_path):
                    photo_file = pattern
                    break
            
            # If no photo found, use fallback image but still include the entry
            if not photo_file:
                print(f"⚠️  No photo found for {filename}, using fallback image")
                photo_file = fallback_image
            
            clean_name = extract_name_from_filename(filename)
            entries.append({
                'number': int(number),
                'name': clean_name,
                'photo': photo_file,
                'slam_page': filename,
                'has_photo': photo_file != fallback_image
            })
        else:
            print(f"⚠️  Could not parse filename: {filename}")
    
    return entries

def generate_hexagon_data(entries):
    """Generate hexagon data array for JavaScript"""
    hexagon_data = []
    
    # Add prominent hexagon first (main slam book)
    main_entry = {
        'imageUrl': 'output/mainPage.png',
        'linkUrl': 'output/main_slam_book.html',
        'title': "Sumukh's 40th Birthday",
        'isProminent': True
    }
    hexagon_data.append(main_entry)
    
    # Add regular entries
    for entry in entries:
        regular_entry = {
            'imageUrl': f"output/{entry['photo']}",
            'linkUrl': f"output/{entry['slam_page']}",
            'title': entry['name']
        }
        hexagon_data.append(regular_entry)
    
    return hexagon_data

def generate_js_array(hexagon_data):
    """Generate JavaScript array string"""
    js_lines = []
    
    for i, entry in enumerate(hexagon_data):
        if i == 0:  # First entry (prominent)
            js_lines.append(f'          // The prominent hexagon (main slam book)')
            js_lines.append(f'          {{ imageUrl: "{entry["imageUrl"]}", linkUrl: "{entry["linkUrl"]}", title: "{entry["title"]}", isProminent: true }},')
            js_lines.append(f'          ')
            js_lines.append(f'          // The rest of the slam book entries')
        else:
            js_lines.append(f'          {{ imageUrl: "{entry["imageUrl"]}", linkUrl: "{entry["linkUrl"]}", title: "{entry["title"]}" }},')
    
    # Remove trailing comma from last entry
    if js_lines and js_lines[-1].endswith(','):
        js_lines[-1] = js_lines[-1][:-1]
    
    return '\n'.join(js_lines)

def generate_beehive_html(hexagon_data):
    """Generate the complete bee hive HTML"""
    
    js_array = generate_js_array(hexagon_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>🐝 Happy 40th Birthday Sumukh! 🐝</title>
    <link rel="preload" href="output/mainPage.png" as="image" />
    <style>
      :root {{
        /* -- Color Palette -- */
        --honey-gold: #ffb300;
        --dark-brown: #4a2e04;
        --bg-color: #fff8e1;
        --shadow-color: rgba(74, 46, 4, 0.4);

        /* -- Sizing for the main grid -- */
        --hex-size: 12vw;
        --hex-gap: 0.5vw;

        /* -- Sizing for the featured hexagon -- */
        --prominent-hex-size: 22vw;
      }}

      /* --- Basic Setup --- */
      body {{
        margin: 0;
        font-family: 'Arial', sans-serif;
        background: linear-gradient(
          135deg,
          rgba(71, 85, 105, 1) 0%,
          rgba(55, 65, 81, 1) 25%,
          rgba(75, 85, 99, 1) 50%,
          rgba(55, 65, 81, 1) 75%,
          rgba(67, 56, 202, 1) 100%
        );
        min-height: 100vh;
        overflow-x: auto;
        padding: 20px;
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
        background-image: radial-gradient(
            circle at 25% 25%,
            rgba(139, 92, 246, 0.1) 0%,
            transparent 50%
          ),
          radial-gradient(circle at 75% 25%, rgba(236, 72, 153, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 25% 75%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
          radial-gradient(circle at 75% 75%, rgba(16, 185, 129, 0.1) 0%, transparent 50%),
          linear-gradient(45deg, transparent 49%, rgba(99, 102, 241, 0.05) 50%, transparent 51%),
          linear-gradient(-45deg, transparent 49%, rgba(236, 72, 153, 0.05) 50%, transparent 51%);
        background-size: 250px 250px, 200px 200px, 220px 220px, 280px 280px, 60px 60px, 60px 60px;
        z-index: -2;
        animation: patternMove 25s ease-in-out infinite;
      }}

      @keyframes patternMove {{
        0%,
        100% {{
          background-position: 0% 0%, 100% 0%, 0% 100%, 100% 100%, 0px 0px, 30px 30px;
        }}
        50% {{
          background-position: 30% 30%, 70% 30%, 30% 70%, 70% 70%, 30px 30px, 0px 0px;
        }}
      }}

      /* --- Floating Particles --- */
      .floating-particles {{
        position: fixed;
        width: 100%;
        height: 100%;
        pointer-events: none;
        top: 0;
        left: 0;
        z-index: 1;
      }}

      .particle {{
        position: absolute;
        background: radial-gradient(circle, #8b5cf6, #ec4899);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
      }}

      @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); opacity: 0.7; }}
        50% {{ transform: translateY(-20px) rotate(180deg); opacity: 1; }}
      }}

      /* --- Confetti Styles --- */
      .confetti-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
      }}

      .confetti {{
        position: absolute;
        width: 10px;
        height: 10px;
        background: #f39c12;
        animation: confettiFall 3s linear forwards;
      }}

      .confetti:nth-child(odd) {{
        background: #e74c3c;
        border-radius: 50%;
      }}

      .confetti:nth-child(3n) {{
        background: #3498db;
      }}

      .confetti:nth-child(4n) {{
        background: #2ecc71;
      }}

      .confetti:nth-child(5n) {{
        background: #9b59b6;
      }}

      .confetti:nth-child(6n) {{
        background: #f1c40f;
        transform: rotate(45deg);
      }}

      @keyframes confettiFall {{
        0% {{
          opacity: 1;
          transform: translateY(-100vh) rotate(0deg);
        }}
        100% {{
          opacity: 0;
          transform: translateY(100vh) rotate(720deg);
        }}
      }}

      /* --- Main wrapper to ensure proper spacing --- */
      #hive-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 4rem 1rem;
        position: relative;
        z-index: 2;
      }}

      /* --- Keyframes for the pulsing glow effect --- */
      @keyframes pulse-glow {{
        0%,
        100% {{
          box-shadow: 
            0 0 1.5vw #8b5cf6,
            0 0 3vw rgba(139, 92, 246, 0.3),
            0 10px 30px rgba(139, 92, 246, 0.4);
        }}
        50% {{
          box-shadow: 
            0 0 3vw #8b5cf6,
            0 0 6vw rgba(139, 92, 246, 0.5),
            0 15px 40px rgba(139, 92, 246, 0.6);
        }}
      }}

      /*
        ========================================
        >> PROMINENT HEXAGON STYLES <<
        ========================================
        */
      #prominent-hexagon-container .hexagon {{
        width: var(--prominent-hex-size);
        height: calc(var(--prominent-hex-size) * 1.1547);
      }}

      #prominent-hexagon-container .hexagon a {{
        /* Apply the pulsing glow animation with enhanced 3D shadow */
        animation: pulse-glow 3s infinite ease-in-out;
        border: none !important;
        background: linear-gradient(135deg, #6366f1, #4f46e5, #3730a3);
        transform: translateZ(25px);
        box-shadow: 
          0 15px 35px rgba(0, 0, 0, 0.4),
          0 8px 20px rgba(0, 0, 0, 0.3),
          0 0 40px rgba(139, 92, 246, 0.6),
          inset 0 3px 0 rgba(255, 255, 255, 0.2),
          inset 0 -3px 0 rgba(0, 0, 0, 0.2),
          /* Prominent 3D thickness */
          0 0 0 4px #5b21b6,
          0 0 0 8px #4c1d95,
          0 0 0 12px #3c1677;
      }}

      #prominent-hexagon-container .hexagon img {{
        padding: 0 !important;
        border-radius: 0 !important;
        transform: scale(1.3);
        transition: transform 0.5s ease;
      }}

      #prominent-hexagon-container .hexagon:hover img {{
        transform: scale(1.4);
      }}

      /*
        ========================================
        >> MAIN HIVE GRID STYLES <<
        ========================================
        */
      #hive-grid-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        /* Negative margin pulls the grid up to nest under the prominent hexagon */
        margin-top: calc(var(--prominent-hex-size) * -0.25);
      }}

      .hive-row {{
        display: flex;
        justify-content: center;
        margin-top: calc(var(--hex-size) * -0.134);
      }}

      .hive-row:first-child {{
        margin-top: 0;
      }}

      /* --- General Hexagon Styles (applies to all) --- */
      .hexagon {{
        position: relative;
        width: var(--hex-size);
        height: calc(var(--hex-size) * 1.1547);
        margin: 0 var(--hex-gap);
        transition: transform 0.3s ease-in-out;
        transform-style: preserve-3d;
      }}

      .hexagon a {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #4a5568, #2d3748);
        text-decoration: none;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        transition: all 0.3s ease;
        overflow: hidden;
        border: none;
        /* Enhanced 3D thickness effects */
        box-shadow: 
          0 8px 16px rgba(0, 0, 0, 0.3),
          0 4px 8px rgba(0, 0, 0, 0.2),
          inset 0 2px 0 rgba(255, 255, 255, 0.15),
          inset 0 -2px 0 rgba(0, 0, 0, 0.2),
          /* 3D thickness layers */
          0 0 0 2px #3a4556,
          0 0 0 4px #2a3441,
          0 0 0 6px #1a242f;
        transform: translateZ(0);
      }}

      .hexagon img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.3s ease;
        padding: 3px;
        border-radius: 4px;
      }}

      /* --- Enhanced 3D Interactivity --- */
      .hexagon a:hover,
      .hexagon a:focus {{
        transform: scale(1.1) translateZ(15px) rotateX(5deg);
        z-index: 10;
        box-shadow: 
          0 20px 40px rgba(0, 0, 0, 0.4),
          0 12px 25px rgba(0, 0, 0, 0.3),
          0 0 30px rgba(139, 92, 246, 0.4),
          inset 0 3px 0 rgba(255, 255, 255, 0.25),
          inset 0 -3px 0 rgba(0, 0, 0, 0.3),
          /* Enhanced 3D thickness on hover */
          0 0 0 3px #4a5568,
          0 0 0 6px #3a4556,
          0 0 0 9px #2a3441;
      }}

      .hexagon a:focus {{
        outline: 3px solid #8b5cf6;
        outline-offset: 5px;
      }}

      .hexagon a:hover img,
      .hexagon a:focus img {{
        transform: scale(1.15);
      }}

      /* --- Responsive Design for Mobile --- */
      @media (max-width: 768px) {{
        :root {{
          --hex-size: 24vw;
          --prominent-hex-size: 55vw;
        }}
        #hive-wrapper {{
          padding: 2rem 0.5rem;
        }}

        /* Reduce 3D effects on mobile for performance */
        .hexagon a:hover,
        .hexagon a:focus {{
          transform: scale(1.1) translateZ(5px);
        }}

        #prominent-hexagon-container .hexagon img {{
          transform: scale(1.2);
        }}
      }}

      /* --- Hexagon appear animation --- */
      .hexagon {{
        animation: hexAppear 0.8s ease-out forwards;
        opacity: 0;
        transform: scale(0) rotate(180deg) translateZ(-50px);
      }}

      /* Prominent hexagon appears immediately without delay */
      #prominent-hexagon-container .hexagon {{
        animation: hexAppearFast 0.3s ease-out forwards;
        animation-delay: 0s !important;
      }}

      @keyframes hexAppear {{
        0% {{
          opacity: 0;
          transform: scale(0) rotate(180deg) translateZ(-50px);
        }}
        70% {{
          transform: scale(1.1) rotate(-10deg) translateZ(10px);
        }}
        100% {{
          opacity: 1;
          transform: scale(1) rotate(0deg) translateZ(0px);
        }}
      }}

      @keyframes hexAppearFast {{
        0% {{
          opacity: 0;
          transform: scale(0.8);
        }}
        100% {{
          opacity: 1;
          transform: scale(1);
        }}
      }}

      .hexagon:nth-child(1) {{ animation-delay: 0.1s; }}
      .hexagon:nth-child(2) {{ animation-delay: 0.2s; }}
      .hexagon:nth-child(3) {{ animation-delay: 0.3s; }}
      .hexagon:nth-child(4) {{ animation-delay: 0.4s; }}
      .hexagon:nth-child(5) {{ animation-delay: 0.5s; }}
      .hexagon:nth-child(6) {{ animation-delay: 0.6s; }}
      .hexagon:nth-child(7) {{ animation-delay: 0.7s; }}
    </style>
  </head>
  <body>
    <div id="confetti-container" class="confetti-container"></div>

    <div class="floating-particles">
      <div class="particle" style="width: 6px; height: 6px; left: 10%; top: 20%; animation-delay: 0s;"></div>
      <div class="particle" style="width: 4px; height: 4px; left: 20%; top: 60%; animation-delay: 1s;"></div>
      <div class="particle" style="width: 8px; height: 8px; left: 30%; top: 10%; animation-delay: 2s;"></div>
      <div class="particle" style="width: 5px; height: 5px; left: 40%; top: 70%; animation-delay: 3s;"></div>
      <div class="particle" style="width: 7px; height: 7px; left: 60%; top: 30%; animation-delay: 4s;"></div>
      <div class="particle" style="width: 4px; height: 4px; left: 70%; top: 80%; animation-delay: 5s;"></div>
      <div class="particle" style="width: 6px; height: 6px; left: 80%; top: 15%; animation-delay: 0.5s;"></div>
      <div class="particle" style="width: 5px; height: 5px; left: 90%; top: 50%; animation-delay: 1.5s;"></div>
    </div>

    <main id="hive-wrapper">
      <div id="prominent-hexagon-container"></div>

      <div id="hive-grid-container"></div>
    </main>

    <script>
      // Confetti blast function
      function createConfetti() {{
        const container = document.getElementById('confetti-container');
        const colors = ['#f39c12', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f1c40f'];
        
        // Create 150 confetti pieces
        for (let i = 0; i < 150; i++) {{
          const confetti = document.createElement('div');
          confetti.className = 'confetti';
          confetti.style.left = Math.random() * 100 + 'vw';
          confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
          confetti.style.animationDelay = Math.random() * 3 + 's';
          confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
          
          // Random shapes
          if (Math.random() > 0.5) {{
            confetti.style.borderRadius = '50%';
          }}
          
          container.appendChild(confetti);
          
          // Remove confetti after animation
          setTimeout(() => {{
            if (confetti.parentNode) {{
              confetti.parentNode.removeChild(confetti);
            }}
          }}, 6000);
        }}
        
        // Remove container after all animations complete
        setTimeout(() => {{
          container.style.display = 'none';
        }}, 6000);
      }}

      document.addEventListener("DOMContentLoaded", () => {{
        // Helper function to create a single hexagon element
        function createHexagon(hexData) {{
          const hexagon = document.createElement("div");
          hexagon.classList.add("hexagon");

          const link = document.createElement("a");
          link.href = hexData.linkUrl;
          link.title = hexData.title;
          link.setAttribute('tabindex', '0');

          const image = document.createElement("img");
          image.src = hexData.imageUrl;
          image.alt = hexData.title;

          link.appendChild(image);
          hexagon.appendChild(link);
          return hexagon;
        }}

        // Preload the main hexagon image for immediate display
        const mainImage = new Image();
        mainImage.src = 'output/mainPage.png';
        
        // Create prominent hexagon immediately
        const prominentContainer = document.getElementById("prominent-hexagon-container");
        const prominentData = {{
          imageUrl: 'output/mainPage.png',
          linkUrl: 'output/main_slam_book.html', 
          title: "Sumukh's 40th Birthday",
          isProminent: true
        }};
        prominentContainer.appendChild(createHexagon(prominentData));
        
        // Trigger confetti blast on page load (after main hexagon is created)
        setTimeout(createConfetti, 500);

        const allHexagonsData = [
{js_array}
        ];

        // --- Logic to build the hive ---

        // Get only the regular hexagon data (prominent already created above)
        const gridData = allHexagonsData.filter((hex) => !hex.isProminent);
        const gridContainer = document.getElementById("hive-grid-container");

        // 3. Create and append the rest of the hive grid
        const rowLayout = [5, 6, 7, 8, 7, 6, 5, 4, 3]; // Layout for the main grid ({len(hexagon_data)-1} hexagons total)
        let dataIndex = 0;

        rowLayout.forEach((hexCount) => {{
          const row = document.createElement("div");
          row.classList.add("hive-row");
          for (let i = 0; i < hexCount; i++) {{
            if (dataIndex >= gridData.length) break;
            row.appendChild(createHexagon(gridData[dataIndex]));
            dataIndex++;
          }}
          gridContainer.appendChild(row);
        }});

        // Create more floating particles dynamically
        function createParticles() {{
          const container = document.querySelector('.floating-particles');
          for (let i = 0; i < 15; i++) {{
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.width = Math.random() * 8 + 3 + 'px';
            particle.style.height = particle.style.width;
            particle.style.left = Math.random() * 100 + '%';
            particle.style.top = Math.random() * 100 + '%';
            particle.style.animationDelay = Math.random() * 6 + 's';
            container.appendChild(particle);
          }}
        }}

        createParticles();

        // Add keyboard navigation
        document.addEventListener('keydown', function(event) {{
          if (event.key === 'Enter' || event.key === ' ') {{
            const focused = document.activeElement;
            if (focused.tagName === 'A' && focused.closest('.hexagon')) {{
              event.preventDefault();
              focused.click();
            }}
          }}
        }});
      }});
    </script>
    
    <!-- Generated on {current_time} -->
  </body>
</html>'''

    return html_content

def main():
    """Main function to generate the bee hive index"""
    print("🐝 Generating Bee Hive Index HTML...")
    
    # Scan for slam book entries
    print("📂 Scanning output folder for slam book entries...")
    entries = scan_slam_book_entries()
    
    if not entries:
        print("❌ No slam book entries found!")
        return
    
    print(f"✅ Found {len(entries)} slam book entries")
    
    # Check if mainPage.png exists
    main_page_path = os.path.join('output', 'mainPage.png')
    if not os.path.exists(main_page_path):
        print("⚠️  Warning: mainPage.png not found in output folder")
    
    # Check if main_slam_book.html exists
    main_html_path = os.path.join('output', 'main_slam_book.html')
    if not os.path.exists(main_html_path):
        print("⚠️  Warning: main_slam_book.html not found in output folder")
    
    # Generate hexagon data
    print("🏗️  Generating hexagon data...")
    hexagon_data = generate_hexagon_data(entries)
    
    # Generate HTML
    print("📝 Generating HTML content...")
    html_content = generate_beehive_html(hexagon_data)
    
    # Write to file
    output_file = 'index.html'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"🎉 Successfully generated {output_file}")
        print(f"📊 Total hexagons: {len(hexagon_data)} (1 prominent + {len(hexagon_data)-1} regular)")
        
        # Display summary
        print("\n📋 Summary:")
        print(f"   • Prominent hexagon: Sumukh's 40th Birthday")
        print(f"   • Regular hexagons: {len(entries)}")
        for i, entry in enumerate(entries[:5], 1):
            print(f"   • {i:2d}. {entry['name']}")
        if len(entries) > 5:
            print(f"   • ... and {len(entries)-5} more entries")
            
    except Exception as e:
        print(f"❌ Error writing to {output_file}: {e}")

if __name__ == "__main__":
    main() 