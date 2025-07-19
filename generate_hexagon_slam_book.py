import csv
import os
import re
from pathlib import Path

class HexagonSlamBookGenerator:
    def __init__(self, csv_file="slam.csv", output_base_dir="hexagon_slam_output"):
        self.csv_file = csv_file
        self.output_base_dir = output_base_dir
        self.template_file = "hexagon_template.html"
        
        # Question emojis mapping (matching original generate_html_slam_book.py)
        self.question_emojis = {
            1: "🔧",  # gadget
            2: "👴",  # 40-year-old uncle
            3: "🔄",  # past life
            4: "🏃",  # escape excuse
            5: "💬",  # signature dialogue
            6: "⚠️",  # warning label
            7: "💭",  # fondest memory
            8: "🎂",  # birthday message
            9: "🎵",  # song title
            10: "🏆", # secret talent
            11: "📺", # reality show
            12: "😎", # cool/cringe
            13: "💎", # quality wish
            14: "📝", # three words
            15: "😤"  # annoying behavior
        }
        
        # Light background colors (more visible, avoiding too white colors)
        self.light_colors = [
            "#e8f4f8",  # light blue
            "#fce4ec",  # light pink
            "#e8f5e8",  # light green
            "#fff3a0",  # light yellow (darker)
            "#f3e5f5",  # light purple
            "#ffebb3",  # light orange (darker)
            "#e6e6e6",  # light gray (darker)
            "#f0f8ff",  # alice blue
            "#e0f2f1",  # mint
            "#f5e6d3",  # cream (darker)
            "#f0e6ff",  # light lavender (darker)
            "#ffe4e6",  # light rose (darker)
            "#d4f4dd",  # light mint green
            "#ffe0cc",  # light peach
            "#e6f3ff"   # very light blue
        ]
        
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create base output directory if it doesn't exist"""
        if not os.path.exists(self.output_base_dir):
            os.makedirs(self.output_base_dir)
    
    def sanitize_folder_name(self, name):
        """Convert name to valid folder name"""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
        sanitized = sanitized.replace(' ', '_')
        return sanitized
    
    def load_hexagon_template(self):
        """Load the hexagon HTML template"""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Template file {self.template_file} not found!")
            return None
    
    def create_hexagon_html(self, emoji, answer_text, background_color, question_num):
        """Create customized hexagon HTML"""
        template = self.load_hexagon_template()
        if not template:
            return None
        
        # Clean up the answer text
        answer_text = answer_text.strip() if answer_text else "No answer provided"
        
        # Replace emoji
        customized_html = template.replace('🎉', emoji)
        
        # Replace text with answer
        customized_html = customized_html.replace('Sample Text', answer_text)
        
        # Remove subtitle for cleaner look
        customized_html = customized_html.replace('<div class="subtitle">Subtitle here</div>', '')
        
        # Replace background color
        customized_html = customized_html.replace('background-color: #e8f4f8;', f'background-color: {background_color};')
        
        # Add handwritten font style with dynamic sizing
        font_style = """
        @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@300;400;700&display=swap');
        
        .text-section {
            font-family: 'Kalam', cursive !important;
            font-size: 1.1rem !important;
            line-height: 1.3 !important;
            max-width: 85% !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            hyphens: auto !important;
        }
        
        /* Dynamic hexagon sizing based on text length */
        .hexagon {
            width: 350px !important;
            height: 304px !important;
            min-width: 250px !important;
            min-height: 217px !important;
            max-width: 500px !important;
            max-height: 433px !important;
        }
        
        /* Size adjustments for different text lengths */
        .hexagon.short-text {
            width: 280px !important;
            height: 243px !important;
        }
        
        .hexagon.medium-text {
            width: 350px !important;
            height: 304px !important;
        }
        
        .hexagon.long-text {
            width: 420px !important;
            height: 365px !important;
        }
        
        .hexagon.very-long-text {
            width: 500px !important;
            height: 433px !important;
        }
        
        @media (max-width: 768px) {
            .hexagon {
                width: 300px !important;
                height: 260px !important;
            }
            .hexagon.short-text {
                width: 250px !important;
                height: 217px !important;
            }
            .hexagon.medium-text {
                width: 300px !important;
                height: 260px !important;
            }
            .hexagon.long-text {
                width: 350px !important;
                height: 304px !important;
            }
            .hexagon.very-long-text {
                width: 400px !important;
                height: 347px !important;
            }
            .text-section {
                font-size: 1rem !important;
            }
        }
        """
        
        # Insert the custom styles before closing </style> tag
        customized_html = customized_html.replace('</style>', font_style + '\n        </style>')
        
        # Add JavaScript to dynamically adjust hexagon size based on text length
        javascript_code = """
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const textSection = document.querySelector('.text-section');
            const hexagon = document.querySelector('.hexagon');
            
            if (textSection && hexagon) {
                const textLength = textSection.textContent.trim().length;
                
                // Remove any existing size classes
                hexagon.classList.remove('short-text', 'medium-text', 'long-text', 'very-long-text');
                
                // Apply appropriate size class based on text length
                if (textLength <= 30) {
                    hexagon.classList.add('short-text');
                } else if (textLength <= 80) {
                    hexagon.classList.add('medium-text');
                } else if (textLength <= 150) {
                    hexagon.classList.add('long-text');
                } else {
                    hexagon.classList.add('very-long-text');
                }
            }
        });
        </script>
        """
        
        # Insert JavaScript before closing </body> tag
        customized_html = customized_html.replace('</body>', javascript_code + '\n    </body>')
        
        return customized_html
    
    def process_csv_and_generate_hexagons(self):
        """Process CSV file and generate hexagon HTML files"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                headers = next(csv_reader)  # Skip header row
                
                for row in csv_reader:
                    if len(row) < 18:  # Make sure we have enough columns
                        continue
                    
                    full_name = row[1].strip()
                    if not full_name:
                        continue
                    
                    # Create folder for this person
                    folder_name = self.sanitize_folder_name(full_name)
                    person_dir = os.path.join(self.output_base_dir, folder_name)
                    
                    if not os.path.exists(person_dir):
                        os.makedirs(person_dir)
                    
                    print(f"Processing: {full_name}")
                    
                    # Process each question-answer pair (columns 2-16, which are indices 2-16)
                    for i in range(2, 17):  # Questions are in columns 2-16
                        question_num = i - 1  # Question numbers 1-15
                        answer = row[i].strip() if i < len(row) else ""
                        
                        # Skip empty answers
                        if not answer:
                            continue
                        
                        # Get emoji for this question
                        emoji = self.question_emojis.get(question_num, "❓")
                        
                        # Get background color (cycle through colors)
                        bg_color = self.light_colors[(question_num - 1) % len(self.light_colors)]
                        
                        # Create hexagon HTML
                        hexagon_html = self.create_hexagon_html(
                            emoji, 
                            answer, 
                            bg_color, 
                            question_num
                        )
                        
                        if hexagon_html:
                            # Save HTML file
                            html_filename = f"{question_num}.html"
                            html_filepath = os.path.join(person_dir, html_filename)
                            
                            with open(html_filepath, 'w', encoding='utf-8') as html_file:
                                html_file.write(hexagon_html)
                            
                            print(f"  Created: {html_filename}")
                    
                    print(f"Completed: {full_name}\n")
                        
        except FileNotFoundError:
            print(f"CSV file {self.csv_file} not found!")
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
    
    def generate_index_file(self):
        """Generate an index file listing all generated folders"""
        index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hexagon Slam Book Index</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .person-list {
            list-style: none;
            padding: 0;
        }
        .person-item {
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
        .person-item a {
            text-decoration: none;
            color: #333;
            font-weight: bold;
        }
        .person-item a:hover {
            color: #007bff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Hexagon Slam Book Collection</h1>
        <ul class="person-list">
"""
        
        # List all person directories
        if os.path.exists(self.output_base_dir):
            for folder_name in os.listdir(self.output_base_dir):
                folder_path = os.path.join(self.output_base_dir, folder_name)
                if os.path.isdir(folder_path):
                    # Convert folder name back to readable format
                    display_name = folder_name.replace('_', ' ')
                    index_content += f'            <li class="person-item"><a href="{folder_name}/">{display_name}</a></li>\n'
        
        index_content += """        </ul>
    </div>
</body>
</html>"""
        
        # Save index file
        index_path = os.path.join(self.output_base_dir, "index.html")
        with open(index_path, 'w', encoding='utf-8') as index_file:
            index_file.write(index_content)
        
        print(f"Index file created: {index_path}")

def main():
    generator = HexagonSlamBookGenerator()
    
    print("🎯 Starting Hexagon Slam Book Generation...")
    print("=" * 50)
    
    # Process CSV and generate hexagons
    generator.process_csv_and_generate_hexagons()
    
    # Generate index file
    generator.generate_index_file()
    
    print("=" * 50)
    print("✅ Hexagon Slam Book generation completed!")
    print(f"📁 Output directory: {generator.output_base_dir}")
    print(f"🌐 Open index.html to browse all generated hexagons")

if __name__ == "__main__":
    main() 