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
    
    # Create the main HTML content with performance optimizations
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
      /* Performance optimizations */
      * {{
        box-sizing: border-box;
      }}
      
      html {{
        scroll-behavior: smooth;
      }}

      body {{
        font-family: "Inter", sans-serif;
        background: linear-gradient(135deg, 
          rgba(71, 85, 105, 1) 0%, 
          rgba(55, 65, 81, 1) 25%, 
          rgba(75, 85, 99, 1) 50%, 
          rgba(55, 65, 81, 1) 75%, 
          rgba(67, 56, 202, 1) 100%);
        background-attachment: fixed;
        min-height: 100vh;
        overflow-x: hidden;
        position: relative;
        /* Performance optimizations */
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeSpeed;
        contain: layout style;
      }}

      /* Optimized background pattern */
      body::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
          radial-gradient(circle at 25% 25%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
          radial-gradient(circle at 75% 75%, rgba(236, 72, 153, 0.08) 0%, transparent 50%);
        background-size: 400px 400px, 300px 300px;
        z-index: -2;
        animation: patternMove 30s ease-in-out infinite;
        /* Performance optimization */
        will-change: background-position;
        transform: translateZ(0);
        backface-visibility: hidden;
      }}

      @keyframes patternMove {{
        0%, 100% {{ background-position: 0% 0%, 100% 100%; }}
        50% {{ background-position: 20% 20%, 80% 80%; }}
      }}

      /* Reduced and optimized animated stickers */
      .animated-sticker {{
        position: absolute;
        font-size: 1.3rem;
        animation: floatSticker 12s ease-in-out infinite;
        opacity: 0.5;
        pointer-events: none;
        z-index: 1;
        /* Performance optimizations */
        will-change: transform;
        transform: translateZ(0);
        backface-visibility: hidden;
        contain: layout style paint;
      }}

      .sticker-1 {{ top: 8%; left: 5%; animation-delay: 0s; }}
      .sticker-2 {{ top: 12%; right: 6%; animation-delay: 4s; }}
      .sticker-3 {{ bottom: 25%; left: 4%; animation-delay: 8s; }}
      .sticker-4 {{ bottom: 12%; right: 8%; animation-delay: 2s; }}

      @keyframes floatSticker {{
        0%, 100% {{ 
          transform: translate3d(0, 0, 0) rotate(0deg) scale(1); 
          opacity: 0.5; 
        }}
        50% {{ 
          transform: translate3d(0, -15px, 0) rotate(2deg) scale(1.05); 
          opacity: 0.7; 
        }}
      }}

      /* Simplified sparkles */
      .sparkle {{
        position: absolute;
        width: 4px;
        height: 4px;
        background: linear-gradient(45deg, #fbbf24, #f59e0b);
        border-radius: 50%;
        animation: sparkleShine 6s ease-in-out infinite;
        opacity: 0.6;
        z-index: 1;
        /* Performance optimizations */
        will-change: opacity, transform;
        transform: translateZ(0);
        backface-visibility: hidden;
      }}

      .sparkle:nth-child(5) {{ top: 15%; left: 20%; animation-delay: 0s; }}
      .sparkle:nth-child(6) {{ bottom: 30%; right: 15%; animation-delay: 3s; }}
      .sparkle:nth-child(7) {{ top: 50%; left: 10%; animation-delay: 1.5s; }}

      @keyframes sparkleShine {{
        0%, 100% {{ opacity: 0.3; transform: scale(1) translateZ(0); }}
        50% {{ opacity: 0.8; transform: scale(1.3) translateZ(0); }}
      }}

      /* Main container with performance optimizations */
      .main-container {{
        background: linear-gradient(135deg, 
          rgba(255, 255, 255, 0.95) 0%, 
          rgba(248, 250, 252, 0.93) 50%, 
          rgba(241, 245, 249, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
          0 25px 50px rgba(0, 0, 0, 0.12),
          0 8px 32px rgba(139, 92, 246, 0.12);
        position: relative;
        overflow: hidden;
        z-index: 10;
        /* Performance optimizations */
        contain: layout style paint;
        transform: translateZ(0);
        backface-visibility: hidden;
      }}

      .main-container::before {{
        content: "";
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.25), 
          rgba(236, 72, 153, 0.25), 
          rgba(59, 130, 246, 0.25), 
          rgba(16, 185, 129, 0.25));
        border-radius: inherit;
        z-index: -1;
        animation: borderGlow 8s ease-in-out infinite;
        /* Performance optimization */
        will-change: opacity;
        transform: translateZ(0);
      }}

      @keyframes borderGlow {{
        0%, 100% {{ opacity: 0.3; }}
        50% {{ opacity: 0.6; }}
      }}

      /* Optimized title */
      .title-gradient {{
        background: linear-gradient(135deg, 
          #8b5cf6 0%, 
          #ec4899 25%, 
          #3b82f6 50%, 
          #10b981 75%, 
          #f59e0b 100%);
        background-size: 200% 200%;
        animation: elegantGradient 8s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: "Playfair Display", serif;
        /* Performance optimization */
        will-change: background-position;
        transform: translateZ(0);
      }}

      @keyframes elegantGradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
      }}

      /* Optimized cover image */
      .cover-image {{
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.9), 
          rgba(236, 72, 153, 0.9), 
          rgba(59, 130, 246, 0.9), 
          rgba(16, 185, 129, 0.9));
        background-size: 300% 300%;
        padding: 8px;
        border-radius: 24px;
        animation: coverSwing 6s ease-in-out infinite;
        box-shadow: 
          0 0 40px rgba(139, 92, 246, 0.3),
          0 16px 40px rgba(0, 0, 0, 0.15);
        position: relative;
        /* Performance optimizations */
        will-change: transform, background-position;
        transform: translateZ(0);
        backface-visibility: hidden;
        contain: layout style paint;
      }}

      .cover-image::before {{
        content: "";
        position: absolute;
        top: -4px;
        left: -4px;
        right: -4px;
        bottom: -4px;
        background: linear-gradient(45deg, 
          rgba(255, 255, 255, 0.3), 
          rgba(255, 255, 255, 0.1));
        border-radius: 28px;
        z-index: -1;
        animation: coverShimmer 4s ease infinite;
        /* Performance optimization */
        will-change: opacity;
        transform: translateZ(0);
      }}

      @keyframes coverSwing {{
        0%, 100% {{ 
          background-position: 0% 50%; 
          transform: rotate(-5deg) translateZ(0); 
        }}
        50% {{ 
          background-position: 100% 50%; 
          transform: rotate(5deg) translateZ(0); 
        }}
      }}

      @keyframes coverShimmer {{
        0%, 100% {{ opacity: 0.2; }}
        50% {{ opacity: 0.4; }}
      }}

      .cover-image:hover {{
        animation-play-state: paused;
        transform: scale(1.02) rotate(0deg) translateZ(0);
        transition: transform 0.3s ease;
      }}

      /* Optimized person cards */
      .person-card {{
        background: linear-gradient(135deg, 
          rgba(255, 255, 255, 0.95) 0%, 
          rgba(248, 250, 252, 0.9) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
        /* Performance optimizations */
        will-change: transform;
        transform: translateZ(0);
        backface-visibility: hidden;
        contain: layout style paint;
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
          rgba(139, 92, 246, 0.08), 
          transparent);
        transform: rotate(45deg) translateZ(0);
        transition: opacity 0.4s ease, transform 0.4s ease;
        opacity: 0;
      }}

      .person-card:hover {{
        transform: translate3d(0, -6px, 0) scale(1.02);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
        border-color: rgba(139, 92, 246, 0.3);
      }}

      .person-card:hover::before {{
        opacity: 1;
        transform: rotate(45deg) translate(15%, 15%) translateZ(0);
      }}

      /* Optimized photo frames */
      .person-photo {{
        background: linear-gradient(45deg, 
          rgba(139, 92, 246, 0.8), 
          rgba(236, 72, 153, 0.8));
        padding: 3px;
        border-radius: 50%;
        animation: photoGlow 6s ease infinite;
        /* Performance optimizations */
        will-change: box-shadow;
        transform: translateZ(0);
      }}

      @keyframes photoGlow {{
        0%, 100% {{ box-shadow: 0 0 12px rgba(139, 92, 246, 0.25); }}
        50% {{ box-shadow: 0 0 20px rgba(236, 72, 153, 0.3); }}
      }}

      /* Optimized lazy loading */
      .lazy-image {{
        opacity: 0;
        transition: opacity 0.3s ease;
      }}

      .lazy-image.loaded {{
        opacity: 1;
      }}

      .lazy-image.loading {{
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading-shimmer 1.5s infinite;
      }}

      @keyframes loading-shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
      }}

      /* Decorative elements */
      .decorative-line {{
        background: linear-gradient(90deg, 
          transparent, 
          rgba(139, 92, 246, 0.3), 
          rgba(236, 72, 153, 0.3), 
          rgba(139, 92, 246, 0.3), 
          transparent);
        height: 3px;
        border-radius: 3px;
        position: relative;
        overflow: hidden;
        /* Performance optimization */
        contain: layout style;
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
          rgba(255, 255, 255, 0.6), 
          transparent);
        animation: lineShimmer 6s ease infinite;
        /* Performance optimization */
        will-change: transform;
      }}

      @keyframes lineShimmer {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(200%); }}
      }}

      /* Custom scrollbar */
      ::-webkit-scrollbar {{
        width: 8px;
      }}
      ::-webkit-scrollbar-track {{
        background: rgba(0, 0, 0, 0.1);
        border-radius: 4px;
      }}
      ::-webkit-scrollbar-thumb {{
        background: linear-gradient(180deg, rgba(139, 92, 246, 0.5), rgba(236, 72, 153, 0.5));
        border-radius: 4px;
      }}
      ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(180deg, rgba(139, 92, 246, 0.7), rgba(236, 72, 153, 0.7));
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

      /* Performance optimizations for mobile */
      @media (max-width: 768px) {{
        .animated-sticker {{
          animation-duration: 15s;
          font-size: 1.1rem;
          opacity: 0.3;
        }}
        
        .main-container {{
          margin: 0.5rem;
          padding: 1.5rem;
          backdrop-filter: blur(15px);
        }}
        
        .title-gradient {{
          font-size: 3rem;
          animation-duration: 10s;
        }}

        .cover-image {{
          animation-duration: 8s;
        }}

        /* Disable some animations on mobile for better performance */
        .sparkle {{
          display: none;
        }}

        body::before {{
          animation-duration: 40s;
        }}
      }}

      /* Reduce motion for users who prefer it */
      @media (prefers-reduced-motion: reduce) {{
        * {{
          animation-duration: 0.01ms !important;
          animation-iteration-count: 1 !important;
          transition-duration: 0.01ms !important;
        }}
      }}
    </style>
  </head>
  <body class="p-2 sm:p-4 md:p-6 lg:p-8 min-h-screen relative">
    <!-- Reduced animated stickers for better performance -->
    <div class="animated-sticker sticker-1">🎉</div>
    <div class="animated-sticker sticker-2">🎂</div>
    <div class="animated-sticker sticker-3">✨</div>
    <div class="animated-sticker sticker-4">🎈</div>
    
    <!-- Reduced sparkles -->
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
            src="mainPage.webp"
            alt="Slam Book Cover"
            class="w-64 h-64 sm:w-80 sm:h-80 md:w-96 md:h-96 rounded-2xl shadow-2xl object-cover lazy-image"
            loading="lazy"
          />
        </div>
      </div>

      <!-- People Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
"""

    # Add person cards with lazy loading
    for i, (person_data, html_filename) in enumerate(people_data, 1):
        name = extract_name_from_data(person_data)
        safe_name = re.sub(r'[^\w\s-]', '', name).strip()
        safe_name = re.sub(r'[-\s]+', '_', safe_name)
        
        # Get photo filename if it exists (prioritize WebP format)
        photo_filename = f"photo_{i:02d}_{safe_name}.webp"
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
                class="w-full h-full object-cover rounded-full lazy-image"
                loading="lazy"
                decoding="async"
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

    # Close the HTML with performance optimized JavaScript
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
      // Performance optimized JavaScript
      document.addEventListener('DOMContentLoaded', function() {{
        // Optimized card interactions with throttling
        const cards = document.querySelectorAll('.person-card');
        let ticking = false;
        
        function updateCard(card, isHover) {{
          if (!ticking) {{
            requestAnimationFrame(function() {{
              if (isHover) {{
                card.style.transform = 'translate3d(0, -6px, 0) scale(1.02)';
              }} else {{
                card.style.transform = 'translate3d(0, 0, 0) scale(1)';
              }}
              ticking = false;
            }});
            ticking = true;
          }}
        }}
        
        cards.forEach(card => {{
          card.addEventListener('mouseenter', () => updateCard(card, true), {{ passive: true }});
          card.addEventListener('mouseleave', () => updateCard(card, false), {{ passive: true }});
        }});

        // Lazy loading implementation with Intersection Observer
        if ('IntersectionObserver' in window) {{
          const lazyImages = document.querySelectorAll('.lazy-image');
          const imageObserver = new IntersectionObserver((entries, observer) => {{
            entries.forEach(entry => {{
              if (entry.isIntersecting) {{
                const img = entry.target;
                img.classList.add('loading');
                
                // Create a new image to preload
                const newImg = new Image();
                newImg.onload = function() {{
                  img.src = this.src;
                  img.classList.remove('loading');
                  img.classList.add('loaded');
                }};
                newImg.onerror = function() {{
                  img.classList.remove('loading');
                  img.classList.add('loaded');
                }};
                
                if (img.dataset.src) {{
                  newImg.src = img.dataset.src;
                }} else {{
                  newImg.src = img.src;
                  img.classList.remove('loading');
                  img.classList.add('loaded');
                }}
                
                imageObserver.unobserve(img);
              }}
            }});
          }}, {{
            rootMargin: '50px 0px',
            threshold: 0.01
          }});
          
          lazyImages.forEach(img => {{
            imageObserver.observe(img);
          }});
        }} else {{
          // Fallback for browsers without Intersection Observer
          document.querySelectorAll('.lazy-image').forEach(img => {{
            img.classList.add('loaded');
          }});
        }}

        // Optimize animations based on device performance
        const isLowPerformanceDevice = navigator.hardwareConcurrency <= 2 || 
                                      navigator.deviceMemory <= 4 ||
                                      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (isLowPerformanceDevice) {{
          // Disable heavy animations on low-performance devices
          document.body.classList.add('low-performance');
          const style = document.createElement('style');
          style.textContent = `
            .low-performance .animated-sticker,
            .low-performance .sparkle {{
              animation-play-state: paused;
              opacity: 0.2;
            }}
            .low-performance body::before {{
              animation: none;
            }}
          `;
          document.head.appendChild(style);
        }}

        // Throttle scroll events for better performance
        let scrollTicking = false;
        window.addEventListener('scroll', function() {{
          if (!scrollTicking) {{
            requestAnimationFrame(function() {{
              scrollTicking = false;
            }});
            scrollTicking = true;
          }}
        }}, {{ passive: true }});

        // Preload critical resources
        const preloadLinks = [
          '{html_filename}' // Preload the first slam book page
        ];
        
        preloadLinks.forEach(href => {{
          if (href && href !== 'undefined') {{
            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = href;
            document.head.appendChild(link);
          }}
        }});
      }});

      // Optimize CSS animations based on user preferences
      if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {{
        document.documentElement.style.setProperty('--animation-duration', '0.01s');
      }}
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
    
    # Check if mainPage.webp exists
    main_page_image = "mainPage.webp"
    if not os.path.exists(main_page_image):
        print(f"❌ Error: Could not find {main_page_image}")
        return
    
    # Copy mainPage.webp to output directory
    import shutil
    output_image_path = os.path.join(output_dir, "mainPage.webp")
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
        
        print(f"\n✅ Successfully generated optimized main slam book page!")
        print(f"📁 Main page saved as: main_slam_book.html")
        print(f"📸 Cover image: mainPage.webp")
        print(f"👥 Total entries: {len(people_data)}")
        
        print(f"\n🚀 Performance optimizations applied:")
        print("   • Smooth scrolling with GPU acceleration")
        print("   • Lazy loading for faster page loads")
        print("   • Reduced animation complexity")
        print("   • Performance-based animation control")
        print("   • Optimized CSS transforms and transitions")
        print("   • Throttled scroll events")
        print("   • Reduced motion support")
        print("   • Low-performance device detection")
        
        print(f"\n🎨 Visual features:")
        print("   • Beautiful elegant design with darker backgrounds")
        print("   • Optimized animations and floating elements")
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