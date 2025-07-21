# 🎉 Slam Book Generator

A beautiful, interactive slam book generator that creates personalized HTML pages from CSV data with photos, questions, and answers.

## ✨ Features

- **Beautiful Design**: Animated stars, floating particles, and gradient backgrounds
- **Personalized Pages**: Each person gets their own customized slam book page
- **Photo Integration**: Downloads and embeds photos from Google Drive
- **Smart Question Handling**: Only shows questions that were actually answered
- **Responsive Design**: Works perfectly on all devices
- **Interactive Elements**: Hover effects, animations, and glass morphism

## 📁 Project Structure

```
bday/
├── slam.csv                    # Source data with questions and answers
├── template.html              # HTML template with all 15 questions
├── generate_html_slam_book.py # Main script to generate HTML pages
├── output/                    # Generated HTML files and photos
│   ├── slam_page_01_Name.html
│   ├── photo_01_Name.jpg
│   └── ...
├── slam_env/                  # Python virtual environment
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd bday
   ```

2. **Create virtual environment**

   ```bash
   python -m venv slam_env
   source slam_env/bin/activate  # On Windows: slam_env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install beautifulsoup4 requests
   ```

4. **Run the generator**
   ```bash
   python generate_html_slam_book.py
   ```

## 📊 CSV Format

The `slam.csv` file should have the following columns:

| Column | Description             |
| ------ | ----------------------- |
| 1      | Timestamp               |
| 2      | Full Name               |
| 3-17   | 15 Questions (in order) |
| 18     | Google Drive Photo URL  |

### Example CSV Structure:

```csv
"Timestamp","Full Name","Question 1","Question 2",...,"Photo URL"
"2025/07/07 4:02:26 pm GMT+5:30","John Doe","Answer 1","Answer 2",...,"https://drive.google.com/open?id=..."
```

## 🎨 Customization

### Questions

The template includes 15 questions with emojis:

1. 🔧 If he were a gadget, what would he be — and what would he do?
2. 👴 What's the most "40-year-old uncle" thing he's ever said?
3. 🔄 What do you think he was in his past life?
4. 🏃 What's his go-to excuse to escape from chores or work?
5. 💬 Whats his signature dialogue or go-to one liner?!
6. ⚠️ If he had a warning label, what would it say?
7. 💭 Whats your fondest or funniest memory with him?!
8. 🎂 A message/wish you'd like to give him as he hits the big 4-0:
9. 🎵 If he was a song, what would the title be?
10. 🏆 What's his secret talent that deserves an award?
11. 📺 If he was in a reality show, which one would it be and why?
12. 😎 What's one thing only he can make look cool… or cringe?
13. 💎 What's one quality in him you wish more people had?
14. 📝 Describe him in three words:
15. 😤 What's that one behaviour of his that annoys you the most?

### Styling

- Modify `template.html` to change the design
- Update CSS classes in the script for different color schemes
- Add new animations or effects

## 🔧 Script Features

### Photo Download

- Automatically downloads photos from Google Drive
- Supports multiple Google Drive URL formats
- Skips download if image already exists
- Creates safe filenames from person names

### Question Processing

- Checks each CSV column for data
- Keeps questions with answers, removes empty ones
- Maintains question order from template
- Shows question count in output

### Output

- Generates individual HTML files for each person
- Includes photos, names, and generation timestamps
- Responsive design for all screen sizes
- Ready to open in any web browser

## 📝 Usage Examples

### Generate all pages:

```bash
python generate_html_slam_book.py
```

### Output:

```
Processing row 1...
  ✅ Image already exists: photo_01_John.jpg
Generated: output/slam_page_01_John.html (15 questions answered)

✅ Successfully generated 17 HTML slam book pages!
```

## 🎯 Output Files

Each person gets:

- `slam_page_XX_Name.html` - Their personalized slam book page
- `photo_XX_Name.jpg` - Their photo downloaded from Google Drive

## 🔗 Dependencies

- **beautifulsoup4**: HTML parsing and manipulation
- **requests**: HTTP requests for photo downloads
- **urllib**: URL parsing for Google Drive links
- **datetime**: Timestamp generation
- **re**: Regular expressions for text cleaning

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Beautiful design inspiration from modern web trends
- Google Drive integration for photo storage
- Tailwind CSS for responsive styling
- BeautifulSoup for HTML manipulation

---

**Made with ❤️ for creating beautiful memories and celebrations!**
