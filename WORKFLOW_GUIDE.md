# 🔄 Slam Book Update Workflow Guide

## When `slam.csv` Changes - Run This!

Whenever you make changes to your `slam.csv` file (add new people, update information, change Google Drive links), you need to run scripts in a specific sequence to update everything properly.

---

## 🚀 **EASIEST METHOD: One-Click Update**

Just run this single script that does everything automatically:

```bash
python update_workflow.py
```

This will run all necessary scripts in the correct order and give you a complete summary.

---

## 📋 **MANUAL METHOD: Step-by-Step**

If you prefer to run scripts manually or if the automatic workflow fails, follow this exact sequence:

### **Phase 1: Images** 📸

```bash
python download_and_convert_images.py
```

- Downloads new images from Google Drive links
- Converts all images to WebP format (faster loading)
- Removes old JPG files to save space

### **Phase 2: Individual Pages** 📄

```bash
python generate_html_slam_book.py
```

- Creates individual HTML pages for each person
- Uses data from slam.csv
- Creates pages in the `output/` folder

### **Phase 3: Main Slam Book** 📖

```bash
python generate_main_slam_book.py
```

- Creates the main slam book page with all entries
- Combines all individual data into one view

### **Phase 4: Index Page** 🏠

```bash
python generate_beehive_index.py
```

- Generates the main index.html page
- Creates the beehive/grid layout of all photos

### **Phase 5: WebP Optimization** ⚡

```bash
python update_html_to_webp.py
```

- Updates all HTML files to use WebP images
- Ensures maximum loading speed

---

## ⚠️ **CRITICAL vs OPTIONAL Steps**

### **Critical Steps** (Must succeed):

1. **Image Download** - Need photos for the slam book
2. **Individual Pages** - Core functionality
3. **Main Slam Book** - Main viewing experience

### **Optional Steps** (Nice to have):

4. **Index Page** - Better navigation
5. **WebP Optimization** - Performance boost

---

## 🎯 **Quick Reference**

| **Scenario**                             | **Command**                             |
| ---------------------------------------- | --------------------------------------- |
| **CSV changed, want everything updated** | `python update_workflow.py`             |
| **Only new images needed**               | `python download_and_convert_images.py` |
| **Only HTML pages need updating**        | `python generate_html_slam_book.py`     |
| **Just want WebP optimization**          | `python update_html_to_webp.py`         |

---

## 🔍 **What Each Script Does**

| **Script**                       | **Purpose**                 | **Input**                | **Output**             |
| -------------------------------- | --------------------------- | ------------------------ | ---------------------- |
| `download_and_convert_images.py` | Downloads & converts images | slam.csv (Drive links)   | WebP images in output/ |
| `generate_html_slam_book.py`     | Creates individual pages    | slam.csv + template.html | Individual HTML pages  |
| `generate_main_slam_book.py`     | Creates main slam book      | slam.csv + images        | main_slam_book.html    |
| `generate_beehive_index.py`      | Creates index page          | slam.csv + images        | index.html             |
| `update_html_to_webp.py`         | Updates HTML for WebP       | All HTML files           | Updated HTML files     |

---

## 🚀 **Performance Tips**

- **Always run the full workflow** when slam.csv changes significantly
- **WebP images are 25-35% smaller** than JPG - huge speed boost!
- **The workflow automatically cleans up old files** to save disk space
- **Run `update_workflow.py` for best results** - it handles everything

---

## 🆘 **Troubleshooting**

### **If the workflow fails:**

1. Check that all required files exist (slam.csv, template.html, etc.)
2. Verify your Google Drive links are shareable/public
3. Run scripts individually to identify which one is failing
4. Check the error messages for specific guidance

### **Common issues:**

- **Google Drive access denied** → Make sure Drive links are public/shareable
- **Template not found** → Ensure template.html exists in the same folder
- **CSV format errors** → Check slam.csv for proper CSV formatting

---

## ✅ **Success Indicators**

After running the workflow, you should see:

- ✅ WebP images in output/ folder
- ✅ Individual HTML pages (slam_page_XX_Name.html)
- ✅ Updated main_slam_book.html
- ✅ Updated index.html
- ✅ No old JPG files (cleaned up automatically)

**Test it:** Open `index.html` in your browser - everything should load quickly with all images showing properly!

---

_💡 **Pro Tip:** Bookmark this guide and always run `python update_workflow.py` when you change slam.csv!_
