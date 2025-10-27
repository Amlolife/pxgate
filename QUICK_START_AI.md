# 🚀 Quick Start: AI Features

## 5-Minute Setup

### Step 1: Install Dependencies (1 minute)

```bash
pip install opencv-python imagehash
```

That's it! These two packages add all AI capabilities.

---

### Step 2: Test Installation (1 minute)

```bash
python test_analysis.py
```

You should see:
```
✓ ALL TESTS PASSED!
You're ready to use AI analysis features in Pxgate!
```

---

### Step 3: Try It Out (3 minutes)

#### Quick Test Script

Create a file `quick_test.py`:

```python
from image_analyzer import quick_analyze

# Analyze any photo
result = quick_analyze("path/to/your/photo.jpg")

print(f"Quality Score: {result['quality_score']:.1f}/100")
print(f"Sharpness: {result['sharpness']:.1f}")
print(f"Exposure: {result['exposure']['exposure_score']:.1f}")
print(f"Faces Found: {result['face_data']['face_count']}")
```

Run it:
```bash
python quick_test.py
```

---

## Integration into Pxgate

### Option 1: Automatic Integration (Recommended)

I've prepared all the code. You just need to:

1. **Copy the integration code** from `INTEGRATION_INSTRUCTIONS.md`
2. **Add imports** to `pxgate.py` (line ~48)
3. **Initialize manager** in `__init__()` (line ~4950)
4. **Add UI buttons** in control panel (line ~5500)
5. **Done!**

Full instructions in `INTEGRATION_INSTRUCTIONS.md` with exact line numbers and code snippets.

---

### Option 2: Manual Testing First

Test the modules independently before integrating:

```python
# test_standalone.py
from image_analyzer import ImageAnalysisEngine
from pathlib import Path

# Initialize engine
engine = ImageAnalysisEngine(max_workers=2)

# Analyze your photos
photos = list(Path("your_photos_folder").glob("*.jpg"))
results = engine.analyze_batch([str(p) for p in photos[:10]])

# Print results
for path, result in results.items():
    print(f"{Path(path).name}: {result['quality_score']:.1f}")

# Find duplicates
duplicates = engine.get_duplicate_groups()
print(f"\nFound {len(duplicates)} duplicate groups")

engine.shutdown()
```

---

## What You Get

### Instant Benefits

✅ **Quality Scores** - Every photo gets 0-100 score
✅ **Face Detection** - Finds faces, eyes, smiles
✅ **Duplicate Finder** - Groups similar images
✅ **100% Offline** - No internet needed
✅ **Fast** - 1-2 seconds per image

### New Workflow

```
Load Folder → Auto-Analyze → View Scores → Sort by Quality → Find Duplicates → Cull Faster
```

---

## Example Output

When you analyze a photo, you get:

```
📊 Quality Analysis:
   Overall Score: 87.5
   Sharpness: 92.3 (excellent focus)
   Exposure: 85.0 (well exposed)
   Noise: 88.5 (clean)
   Composition: 78.0 (good)

👤 Face Detection:
   Faces: 2
   Eyes Detected: ✓
   Smiles: ✓
   Face Quality: 85.0
```

---

## Common Use Cases

### Find Your Best Shots

```python
from image_analyzer import ImageAnalysisEngine
from pathlib import Path

engine = ImageAnalysisEngine()
photos = [str(p) for p in Path("photos").glob("*.jpg")]
results = engine.analyze_batch(photos)

# Get top 10
top_10 = sorted(results.items(), 
                key=lambda x: x[1]['quality_score'], 
                reverse=True)[:10]

print("Your best photos:")
for path, result in top_10:
    print(f"{Path(path).name}: {result['quality_score']:.1f}")

engine.shutdown()
```

### Remove Duplicates

```python
from image_analyzer import DuplicateDetector
from pathlib import Path

detector = DuplicateDetector(similarity_threshold=5)

# Add all photos
for photo in Path("photos").glob("*.jpg"):
    detector.add_image(str(photo))

# Find duplicates
groups = detector.find_duplicates()

print(f"Found {len(groups)} groups of similar images")
for i, group in enumerate(groups, 1):
    print(f"\nGroup {i} ({len(group)} images):")
    for photo in group:
        print(f"  - {Path(photo).name}")
```

### Filter by Quality

```python
from image_analyzer import ImageAnalysisEngine
from pathlib import Path

engine = ImageAnalysisEngine()
photos = [str(p) for p in Path("photos").glob("*.jpg")]
results = engine.analyze_batch(photos)

# Keep only high quality (>= 70)
keepers = [path for path, r in results.items() 
           if r['quality_score'] >= 70]

print(f"Keeping {len(keepers)} out of {len(photos)} photos")

engine.shutdown()
```

---

## Keyboard Shortcuts (After Integration)

| Key | Action |
|-----|--------|
| `Alt + A` | Start analysis |
| `Alt + D` | Show duplicates |
| `Alt + S` | Settings |
| `Alt + Q` | Sort by quality |

---

## Performance Tips

### For Speed
```python
# Disable face detection (50% faster)
result = engine.analyze_image(path, include_faces=False)

# Use fewer workers on slower systems
engine = ImageAnalysisEngine(max_workers=2)
```

### For Accuracy
```python
# Stricter duplicate detection
detector = DuplicateDetector(similarity_threshold=3)

# More lenient duplicate detection
detector = DuplicateDetector(similarity_threshold=10)
```

---

## Troubleshooting

### "Module not found"
```bash
pip install opencv-python imagehash
```

### "Slow performance"
- Disable face detection
- Reduce worker threads
- Process smaller batches

### "Face detection not working"
```bash
pip uninstall opencv-python
pip install opencv-python
```

---

## Next Steps

1. ✅ **Test** - Run `test_analysis.py`
2. 📖 **Read** - Check `AI_FEATURES_GUIDE.md` for details
3. 🔧 **Integrate** - Follow `INTEGRATION_INSTRUCTIONS.md`
4. 🎉 **Enjoy** - Faster photo culling!

---

## Full Documentation

- **`AI_FEATURES_GUIDE.md`** - Complete user guide
- **`AI_FEATURES_README.md`** - Technical documentation
- **`INTEGRATION_INSTRUCTIONS.md`** - Integration steps
- **`AI_IMPLEMENTATION_SUMMARY.md`** - Overview

---

## Support

Questions? Check the docs or run the test suite:
```bash
python test_analysis.py
```

---

**You're ready to go! Start analyzing photos with AI!** 🎉
