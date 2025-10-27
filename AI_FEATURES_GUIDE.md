# 🤖 AI-Powered Photo Analysis Features

## Overview

Pxgate now includes **offline AI-powered image analysis** to help you identify the best photos faster. All processing happens locally on your computer - no internet connection required.

---

## 🎯 New Features

### 1. **Intelligent Image Quality Analysis**

Automatically analyzes each photo for:

#### **Sharpness Detection** (0-100 score)
- Uses Laplacian variance to detect focus quality
- Higher scores = sharper, better-focused images
- Helps identify blurry or out-of-focus shots

#### **Exposure Analysis** (0-100 score)
- Evaluates brightness and contrast
- Detects overexposed (blown highlights) or underexposed (blocked shadows) images
- Identifies optimal exposure balance

#### **Noise Detection** (0-100 score)
- Estimates ISO noise and grain
- Higher scores = cleaner images
- Useful for identifying high-ISO shots

#### **Composition Score** (0-100 score)
- Basic rule-of-thirds analysis
- Evaluates subject placement
- Identifies images with strong composition

#### **Overall Quality Score** (0-100 score)
- Weighted combination of all metrics:
  - Sharpness: 35%
  - Exposure: 25%
  - Noise: 20%
  - Composition: 20%
  - Face bonus: up to 10% (if faces detected)

---

### 2. **Face Detection & Analysis**

Detects and analyzes human faces in photos:

#### **Face Count**
- Counts number of faces in each image
- Ideal range: 1-3 faces (portraits and small groups)

#### **Eye Detection**
- Detects if eyes are visible and open
- Important for portrait quality assessment

#### **Smile Detection**
- Identifies smiling faces
- Helps find the best expressions

#### **Face Quality Score**
- Evaluates face detection quality
- Considers: face count, eye detection, face size

---

### 3. **Duplicate & Similar Image Detection**

Finds duplicate and similar images using perceptual hashing:

#### **Perceptual Hashing**
- Creates a "fingerprint" of each image
- Resistant to minor edits (resize, compression, slight color changes)
- Works even if images are different file formats

#### **Similarity Threshold**
- Configurable sensitivity (0-20)
- Lower values = more strict matching
- Default: 5 (good balance)

#### **Duplicate Groups**
- Groups similar images together
- Helps identify burst shots and near-duplicates
- Quick navigation to review similar images

---

## 🚀 Workflow Integration

### **Recommended Workflow**

```
1. Load Folder
   ↓
2. Auto-Analysis Starts (Background)
   • Quality scoring
   • Face detection
   • Duplicate detection
   ↓
3. Review with AI Assistance
   • View quality scores in file info
   • Sort by quality (best first)
   • Filter out low-quality images
   ↓
4. Check Duplicates
   • View duplicate groups
   • Keep best of similar shots
   ↓
5. Final Culling
   • Use keyboard shortcuts (1-9)
   • Move keepers to folders
```

---

## 💡 How to Use

### **Automatic Analysis**

When you load a folder:
1. Analysis starts automatically in the background
2. Progress dialog shows analysis status
3. Results appear as images are processed
4. No action needed - just wait for completion

### **View Analysis Results**

Quality scores appear in the **File Info Panel**:
```
📊 Quality Analysis:
   Overall Score: 87.5
   Sharpness: 92.3
   Exposure: 85.0
   Noise: 88.5
   Composition: 78.0

👤 Face Detection:
   Faces: 2
   Eyes Detected: ✓
   Smiles: ✓
```

### **Sort by Quality**

New sorting options:
- **Sort by Quality (High to Low)** - Best photos first
- **Sort by Quality (Low to High)** - Worst photos first
- **Sort by Face Count** - Photos with people first

### **Filter by Quality**

Enable quality filtering:
1. Open **Analysis Settings**
2. Check "Enable quality-based filtering"
3. Set minimum quality score (e.g., 60)
4. Only photos above threshold will be shown

### **Find Duplicates**

1. After analysis completes, click **"Find Duplicates"** button
2. Dialog shows groups of similar images
3. Double-click a group to view first image
4. Navigate through group to compare
5. Keep best, move others to reject folder

---

## ⚙️ Settings & Configuration

### **Analysis Settings Dialog**

Access via: **Settings → Analysis Settings**

#### **Quality Filtering**
- ☐ Enable quality-based filtering
- Minimum quality score: [0-100]

#### **Face Detection**
- ☑ Enable face detection (slower)
- ☐ Prioritize images with faces

#### **Duplicate Detection**
- Similarity threshold: [0-20]
  - 0 = Only exact duplicates
  - 5 = Similar images (default)
  - 10 = Loosely similar
  - 20 = Very loose matching

---

## 🎮 Keyboard Shortcuts

New shortcuts for AI features:

| Key | Action |
|-----|--------|
| `Alt + A` | Start/Restart Analysis |
| `Alt + D` | Show Duplicates Dialog |
| `Alt + S` | Analysis Settings |
| `Alt + Q` | Sort by Quality (toggle) |
| `Alt + F` | Filter by Quality (toggle) |

---

## 📊 Understanding Scores

### **Quality Score Interpretation**

| Score | Quality | Recommendation |
|-------|---------|----------------|
| 90-100 | Excellent | Definite keeper |
| 75-89 | Good | Likely keeper |
| 60-74 | Acceptable | Review carefully |
| 40-59 | Below Average | Consider rejecting |
| 0-39 | Poor | Likely reject |

### **What Affects Scores?**

**High Scores:**
- Sharp focus
- Good exposure (not too bright/dark)
- Low noise
- Faces with visible eyes
- Strong composition

**Low Scores:**
- Blurry/out of focus
- Over/underexposed
- High ISO noise
- Poor composition
- No clear subject

---

## 🔧 Performance Considerations

### **Analysis Speed**

Typical processing times (per image):
- **Quality Analysis**: ~0.5-1 second
- **Face Detection**: +0.5-1 second (optional)
- **Duplicate Hashing**: ~0.1 second

Total: ~1-2 seconds per image with face detection

### **System Requirements**

- **Minimum**: 8GB RAM, dual-core CPU
- **Recommended**: 16GB RAM, quad-core CPU
- **Optimal**: 32GB+ RAM, 6+ core CPU

### **Optimization Tips**

1. **Disable face detection** if you don't need it (faster)
2. **Analyze in batches** - don't load 1000+ images at once
3. **Close other apps** during analysis for best performance
4. **Use SSD** for faster image loading

---

## 🎯 Use Cases

### **Wedding Photography**
- Find best shots from burst sequences
- Identify photos with all eyes open
- Detect smiling faces
- Remove duplicates from continuous shooting

### **Portrait Sessions**
- Sort by face quality score
- Find shots with best expressions
- Identify sharp vs. soft focus
- Compare similar poses

### **Landscape Photography**
- Sort by sharpness (focus stacking candidates)
- Identify best exposure
- Find cleanest (lowest noise) shots
- Remove bracketed duplicates

### **Event Photography**
- Quick quality assessment of hundreds of shots
- Find photos with faces
- Identify key moments (smiles, expressions)
- Remove accidental duplicates

---

## 🐛 Troubleshooting

### **Analysis Not Starting**

**Problem**: Analysis doesn't start when loading folder

**Solutions**:
1. Check that `opencv-python` and `imagehash` are installed
2. Manually start: Click "Analyze Images" button
3. Check logs for errors

### **Slow Analysis**

**Problem**: Analysis takes too long

**Solutions**:
1. Disable face detection in settings
2. Reduce number of images loaded
3. Close other applications
4. Check system resources (RAM, CPU)

### **Inaccurate Scores**

**Problem**: Quality scores don't match expectations

**Solutions**:
1. Scores are objective metrics, not artistic judgment
2. Adjust quality threshold in settings
3. Use scores as guidance, not absolute truth
4. Combine with your own visual assessment

### **Face Detection Issues**

**Problem**: Faces not detected or false positives

**Solutions**:
1. Face detection works best with frontal faces
2. Profile shots may not be detected
3. Small faces (distant subjects) may be missed
4. Adjust similarity threshold for better results

---

## 📝 Technical Details

### **Algorithms Used**

1. **Sharpness**: Laplacian variance method
2. **Exposure**: Histogram analysis with clipping detection
3. **Noise**: High-frequency content estimation
4. **Composition**: Edge detection with rule-of-thirds grid
5. **Face Detection**: Haar Cascade classifiers (OpenCV)
6. **Duplicate Detection**: Average perceptual hashing (imagehash)

### **Privacy & Security**

- ✅ **100% Offline** - No data sent to servers
- ✅ **No Cloud Processing** - All analysis on your computer
- ✅ **No Tracking** - No usage data collected
- ✅ **Open Source** - Code is auditable

### **Data Storage**

- Analysis results cached in memory during session
- No permanent storage of analysis data
- Results cleared when folder is closed
- No modification to original image files

---

## 🚀 Future Enhancements

Potential future features:
- [ ] Custom quality scoring weights
- [ ] Export analysis results to CSV
- [ ] Batch quality comparison
- [ ] Advanced composition analysis
- [ ] Color harmony detection
- [ ] Subject detection (beyond faces)
- [ ] Motion blur detection
- [ ] HDR/exposure bracketing detection

---

## 💬 Feedback

Found a bug or have a suggestion? Please report it on GitHub!

---

**Enjoy smarter, faster photo culling with AI assistance!** 🎉
