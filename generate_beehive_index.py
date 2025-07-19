#!/usr/bin/env python3
"""
Generate Bee Hive Index HTML with Performance Optimizations
Dynamically creates the bee hive index page by scanning available slam book entries
Features: Lazy loading, progressive loading, image optimization, loading states
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
    """Generate the complete bee hive HTML with performance optimizations"""
    
    js_array = generate_js_array(hexagon_data)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>🐝 Happy 40th Birthday Sumukh! 🐝</title>
    
    <!-- Critical resource preloading -->
    <link rel="preload" href="output/mainPage.png" as="image" />
    <link rel="dns-prefetch" href="//fonts.googleapis.com" />
    
    <!-- Performance hints -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
    <meta name="theme-color" content="#8b5cf6" />
    
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

      /* --- Performance-optimized Basic Setup --- */
      * {{
        box-sizing: border-box;
      }}
      
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
        overflow-y: auto;
        padding: 20px;
        position: relative;
        /* Enable smooth scrolling on mobile */
        -webkit-overflow-scrolling: touch;
        /* Optimize rendering */
        will-change: scroll-position;
      }}

      /* Optimized background pattern with reduced complexity */
      body::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: radial-gradient(
            circle at 25% 25%,
            rgba(139, 92, 246, 0.08) 0%,
            transparent 50%
          ),
          radial-gradient(circle at 75% 75%, rgba(236, 72, 153, 0.08) 0%, transparent 50%);
        background-size: 400px 400px, 300px 300px;
        z-index: -2;
        /* Reduce animation for better performance */
        animation: patternMove 30s ease-in-out infinite;
        will-change: background-position;
      }}

      @keyframes patternMove {{
        0%, 100% {{ background-position: 0% 0%, 100% 100%; }}
        50% {{ background-position: 30% 30%, 70% 70%; }}
      }}

      /* --- Reduced Floating Particles for performance --- */
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
        animation: float 8s ease-in-out infinite;
        will-change: transform;
      }}

      @keyframes float {{
        0%, 100% {{ transform: translateY(0px) rotate(0deg); opacity: 0.6; }}
        50% {{ transform: translateY(-15px) rotate(180deg); opacity: 0.8; }}
      }}

      /* --- Optimized Confetti Styles --- */
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
        width: 8px;
        height: 8px;
        background: #f39c12;
        animation: confettiFall 2.5s linear forwards;
        will-change: transform;
      }}

      .confetti:nth-child(odd) {{ background: #e74c3c; border-radius: 50%; }}
      .confetti:nth-child(3n) {{ background: #3498db; }}
      .confetti:nth-child(4n) {{ background: #2ecc71; }}
      .confetti:nth-child(5n) {{ background: #9b59b6; }}

      @keyframes confettiFall {{
        0% {{ opacity: 1; transform: translateY(-100vh) rotate(0deg); }}
        100% {{ opacity: 0; transform: translateY(100vh) rotate(360deg); }}
      }}

      /* --- Main wrapper --- */
      #hive-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 4rem 1rem;
        position: relative;
        z-index: 2;
        min-width: 100%;
        width: max-content;
        margin: 0 auto;
      }}

      .beehive-container {{
        width: 100%;
        overflow-x: auto;
        overflow-y: visible;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 2rem;
        scrollbar-width: thin;
        scrollbar-color: #8b5cf6 transparent;
      }}

      .beehive-container::-webkit-scrollbar {{
        height: 8px;
      }}

      .beehive-container::-webkit-scrollbar-track {{
        background: rgba(139, 92, 246, 0.1);
        border-radius: 4px;
      }}

      .beehive-container::-webkit-scrollbar-thumb {{
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
        border-radius: 4px;
      }}

      .scroll-hint {{
        display: none;
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(139, 92, 246, 0.9);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.9rem;
        z-index: 1000;
        animation: pulseHint 2s infinite;
        pointer-events: none;
      }}

      @keyframes pulseHint {{
        0%, 100% {{ opacity: 0.7; transform: translateX(-50%) scale(1); }}
        50% {{ opacity: 1; transform: translateX(-50%) scale(1.05); }}
      }}

      @media (max-width: 768px) {{
        .scroll-hint {{ display: block; }}
      }}

      .beehive {{
        width: max-content;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
      }}

      /* --- Optimized pulse glow effect --- */
      @keyframes pulse-glow {{
        0%, 100% {{
          box-shadow: 0 0 20px rgba(139, 92, 246, 0.4), 0 10px 30px rgba(139, 92, 246, 0.3);
        }}
        50% {{
          box-shadow: 0 0 30px rgba(139, 92, 246, 0.6), 0 15px 40px rgba(139, 92, 246, 0.4);
        }}
      }}

      /* --- PROMINENT HEXAGON STYLES --- */
      #prominent-hexagon-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-bottom: 2rem;
      }}

      #prominent-hexagon-container .hexagon {{
        width: var(--prominent-hex-size);
        height: calc(var(--prominent-hex-size) * 1.1547);
      }}

      #prominent-hexagon-container .hexagon a {{
        animation: pulse-glow 3s infinite ease-in-out;
        border: none !important;
        background: linear-gradient(135deg, #6366f1, #4f46e5, #3730a3);
        box-shadow: 
          0 15px 35px rgba(0, 0, 0, 0.4),
          0 0 40px rgba(139, 92, 246, 0.6),
          0 0 0 4px #5b21b6;
        will-change: box-shadow;
      }}

      #prominent-hexagon-container .hexagon img {{
        padding: 0 !important;
        border-radius: 0 !important;
        transform: scale(1.3);
        transition: transform 0.3s ease;
        will-change: transform;
      }}

      /* --- MAIN HIVE GRID STYLES --- */
      #hive-grid-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: calc(var(--prominent-hex-size) * -0.15);
      }}

      .hive-row {{
        display: flex;
        justify-content: center;
        margin-top: calc(var(--hex-size) * -0.134);
      }}

      .hive-row:first-child {{ margin-top: 0; }}

      /* --- Optimized Hexagon Styles --- */
      .hexagon {{
        position: relative;
        width: var(--hex-size);
        height: calc(var(--hex-size) * 1.1547);
        margin: 0 var(--hex-gap);
        transition: transform 0.2s ease-in-out;
        will-change: transform;
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
        transition: all 0.2s ease;
        overflow: hidden;
        border: none;
        box-shadow: 
          0 8px 16px rgba(0, 0, 0, 0.3),
          0 0 0 2px #3a4556;
        will-change: transform, box-shadow;
      }}

      .hexagon img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.2s ease;
        padding: 3px;
        border-radius: 4px;
        will-change: transform;
      }}

      /* --- Performance-optimized loading states --- */
      .hexagon.loading a {{
        background: linear-gradient(135deg, #64748b, #475569);
        animation: shimmer 1.5s ease-in-out infinite;
      }}

      @keyframes shimmer {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
      }}

      .hexagon.loading img {{
        opacity: 0;
        transition: opacity 0.3s ease;
      }}

      .hexagon.loaded img {{
        opacity: 1;
      }}

      /* --- Reduced hover effects for better performance --- */
      .hexagon a:hover,
      .hexagon a:focus {{
        transform: scale(1.05);
        box-shadow: 
          0 12px 24px rgba(0, 0, 0, 0.4),
          0 0 20px rgba(139, 92, 246, 0.3);
      }}

      .hexagon a:hover img,
      .hexagon a:focus img {{
        transform: scale(1.1);
      }}

      /* --- Mobile Responsive Design --- */
      @media (max-width: 768px) {{
        :root {{
          --hex-size: 18vw;
          --prominent-hex-size: 45vw;
        }}
        
        body {{ padding: 10px; }}
        #hive-wrapper {{ padding: 2rem 0.5rem; width: max-content; min-width: 100vw; }}
        
        /* Disable heavy effects on mobile */
        .hexagon a:hover {{ transform: scale(1.02); }}
        .particle {{ animation-duration: 10s; }}
        body::before {{ animation: none; }}
      }}

      @media (max-width: 480px) {{
        :root {{
          --hex-size: 22vw;
          --prominent-hex-size: 50vw;
        }}
        
        #hive-wrapper {{ min-width: 120vw; }}
        .beehive {{ transform: scale(0.9); }}
      }}

      /* --- Optimized appearance animations --- */
      .hexagon {{
        opacity: 0;
        transform: scale(0.8) translateY(20px);
        animation: hexAppear 0.5s ease-out forwards;
      }}

      #prominent-hexagon-container .hexagon {{
        animation: hexAppearFast 0.3s ease-out forwards;
        animation-delay: 0s !important;
      }}

      @keyframes hexAppear {{
        0% {{ opacity: 0; transform: scale(0.8) translateY(20px); }}
        100% {{ opacity: 1; transform: scale(1) translateY(0); }}
      }}

      @keyframes hexAppearFast {{
        0% {{ opacity: 0; transform: scale(0.9); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}

      /* Staggered animation delays */
      .hexagon:nth-child(1) {{ animation-delay: 0.1s; }}
      .hexagon:nth-child(2) {{ animation-delay: 0.15s; }}
      .hexagon:nth-child(3) {{ animation-delay: 0.2s; }}
      .hexagon:nth-child(4) {{ animation-delay: 0.25s; }}
      .hexagon:nth-child(5) {{ animation-delay: 0.3s; }}
      .hexagon:nth-child(6) {{ animation-delay: 0.35s; }}
      .hexagon:nth-child(7) {{ animation-delay: 0.4s; }}

      /* --- Loading indicator --- */
      .page-loader {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(71, 85, 105, 0.9), rgba(67, 56, 202, 0.9));
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        transition: opacity 0.5s ease;
      }}

      .loader-hexagon {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #8b5cf6, #ec4899);
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        animation: loaderSpin 1s ease-in-out infinite;
      }}

      @keyframes loaderSpin {{
        0%, 100% {{ transform: rotate(0deg) scale(1); }}
        50% {{ transform: rotate(180deg) scale(1.1); }}
      }}

      .page-loader.hidden {{
        opacity: 0;
        pointer-events: none;
      }}
    </style>
  </head>
  <body>
    <!-- Page loader -->
    <div id="page-loader" class="page-loader">
      <div class="loader-hexagon"></div>
    </div>

    <div id="confetti-container" class="confetti-container"></div>

    <!-- Reduced floating particles for better performance -->
    <div class="floating-particles">
      <div class="particle" style="width: 6px; height: 6px; left: 15%; top: 25%; animation-delay: 0s;"></div>
      <div class="particle" style="width: 4px; height: 4px; left: 85%; top: 75%; animation-delay: 2s;"></div>
      <div class="particle" style="width: 5px; height: 5px; left: 50%; top: 10%; animation-delay: 4s;"></div>
      <div class="particle" style="width: 7px; height: 7px; left: 20%; top: 80%; animation-delay: 6s;"></div>
    </div>

    <main id="hive-wrapper">
      <div class="beehive-container">
        <div class="beehive">
          <div id="prominent-hexagon-container"></div>
          <div id="hive-grid-container"></div>
        </div>
      </div>
      <div class="scroll-hint">Scroll to see more! 👈</div>
    </main>

    <script>
      // Performance optimized confetti with reduced particles
      function createConfetti() {{
        const container = document.getElementById('confetti-container');
        const colors = ['#f39c12', '#e74c3c', '#3498db', '#2ecc71', '#9b59b6'];
        
        // Reduced to 75 particles for better performance
        for (let i = 0; i < 75; i++) {{
          const confetti = document.createElement('div');
          confetti.className = 'confetti';
          confetti.style.left = Math.random() * 100 + 'vw';
          confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
          confetti.style.animationDelay = Math.random() * 2 + 's';
          confetti.style.animationDuration = (Math.random() * 2 + 1.5) + 's';
          
          container.appendChild(confetti);
          
          // Clean up after animation
          setTimeout(() => {{
            if (confetti.parentNode) {{
              confetti.parentNode.removeChild(confetti);
            }}
          }}, 4000);
        }}
        
        // Hide container after animations
        setTimeout(() => {{
          container.style.display = 'none';
        }}, 4000);
      }}

      // Intersection Observer for lazy loading
      const imageObserver = new IntersectionObserver((entries, observer) => {{
        entries.forEach(entry => {{
          if (entry.isIntersecting) {{
            const hexagon = entry.target;
            const img = hexagon.querySelector('img');
            
            if (img && img.dataset.src) {{
              // Start loading the image
              hexagon.classList.add('loading');
              
              const imageLoader = new Image();
              imageLoader.onload = () => {{
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                hexagon.classList.remove('loading');
                hexagon.classList.add('loaded');
                observer.unobserve(hexagon);
              }};
              
              imageLoader.onerror = () => {{
                // Fallback to placeholder or error image
                img.src = 'output/mainPage.png';
                hexagon.classList.remove('loading');
                hexagon.classList.add('loaded');
                observer.unobserve(hexagon);
              }};
              
              imageLoader.src = img.dataset.src;
            }}
          }}
        }});
      }}, {{
        rootMargin: '100px', // Start loading 100px before entering viewport
        threshold: 0.1
      }});

      document.addEventListener("DOMContentLoaded", () => {{
        const pageLoader = document.getElementById('page-loader');
        
        // Helper function to create a single hexagon element with lazy loading
        function createHexagon(hexData, isProminent = false) {{
          const hexagon = document.createElement("div");
          hexagon.classList.add("hexagon");

          const link = document.createElement("a");
          link.href = hexData.linkUrl;
          link.title = hexData.title;
          link.setAttribute('tabindex', '0');

          const image = document.createElement("img");
          image.alt = hexData.title;
          
          // Implement lazy loading for non-prominent images
          if (isProminent) {{
            image.src = hexData.imageUrl;
            hexagon.classList.add('loaded');
          }} else {{
            image.dataset.src = hexData.imageUrl;
            image.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzY0NzQ4YiIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LXNpemU9IjE0IiBmaWxsPSIjZmZmIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgdGV4dC1hbmNob3I9Im1pZGRsZSI+TG9hZGluZy4uLjwvdGV4dD48L3N2Zz4='; // Base64 placeholder
            hexagon.classList.add('loading');
          }}

          link.appendChild(image);
          hexagon.appendChild(link);
          return hexagon;
        }}

        // Priority loading: Create prominent hexagon immediately
        const prominentContainer = document.getElementById("prominent-hexagon-container");
        const prominentData = {{
          imageUrl: 'output/mainPage.png',
          linkUrl: 'output/main_slam_book.html', 
          title: "Sumukh's 40th Birthday",
          isProminent: true
        }};
        
        const prominentHex = createHexagon(prominentData, true);
        prominentContainer.appendChild(prominentHex);

        const allHexagonsData = [
{js_array}
        ];

        // Progressive loading strategy
        const gridData = allHexagonsData.filter((hex) => !hex.isProminent);
        const gridContainer = document.getElementById("hive-grid-container");
        const rowLayout = [5, 6, 7, 8, 7, 6, 5, 4, 3];
        let dataIndex = 0;

        // Build the hive grid with lazy loading
        rowLayout.forEach((hexCount, rowIndex) => {{
          const row = document.createElement("div");
          row.classList.add("hive-row");
          
          for (let i = 0; i < hexCount; i++) {{
            if (dataIndex >= gridData.length) break;
            
            const hexagon = createHexagon(gridData[dataIndex]);
            row.appendChild(hexagon);
            
            // Start observing for lazy loading
            imageObserver.observe(hexagon);
            
            dataIndex++;
          }}
          gridContainer.appendChild(row);
        }});

        // Hide page loader after critical content is ready
        setTimeout(() => {{
          pageLoader.classList.add('hidden');
          
          // Trigger confetti after loader is hidden
          setTimeout(createConfetti, 300);
        }}, 200);

        // Mobile scroll hint management
        const scrollHint = document.querySelector('.scroll-hint');
        if (scrollHint) {{
          const hideHint = () => {{
            scrollHint.style.opacity = '0';
            setTimeout(() => scrollHint.style.display = 'none', 300);
          }};
          
          setTimeout(hideHint, 6000);
          
          const beehiveContainer = document.querySelector('.beehive-container');
          if (beehiveContainer) {{
            beehiveContainer.addEventListener('scroll', () => {{
              setTimeout(hideHint, 1000);
            }}, {{ once: true }});
          }}
          
          document.addEventListener('touchstart', hideHint, {{ once: true }});
        }}

        // Keyboard navigation
        document.addEventListener('keydown', function(event) {{
          if (event.key === 'Enter' || event.key === ' ') {{
            const focused = document.activeElement;
            if (focused.tagName === 'A' && focused.closest('.hexagon')) {{
              event.preventDefault();
              focused.click();
            }}
          }}
        }});

        // Preload next batch of images on user interaction
        let preloadTriggered = false;
        const triggerPreload = () => {{
          if (preloadTriggered) return;
          preloadTriggered = true;
          
          // Preload first few images for smoother scrolling
          const firstBatch = gridData.slice(0, 10);
          firstBatch.forEach(hexData => {{
            const preloadImg = new Image();
            preloadImg.src = hexData.imageUrl;
          }});
        }};

        // Trigger preload on first user interaction
        ['click', 'scroll', 'touchstart', 'keydown'].forEach(event => {{
          document.addEventListener(event, triggerPreload, {{ once: true, passive: true }});
        }});
      }});
    </script>
    
    <!-- Generated on {current_time} with performance optimizations -->
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