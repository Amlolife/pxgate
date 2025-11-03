# Test Mac M-Chip Build Only

## 🎯 Quick Test - M-Chip Only

I've created a **separate workflow** that only builds for Mac M-chip (Apple Silicon) to save time and test the fixes.

---

## 📁 Two Workflows Available

### 1. **build-mac-m-chip-only.yml** ← Use this for testing!
- ✅ Only builds Mac M-chip version
- ✅ Faster (~6 minutes)
- ✅ Saves GitHub Actions minutes
- ✅ Perfect for testing the fix

### 2. **build-all-platforms.yml** ← Use for full release
- Builds Windows + macOS Intel + macOS M-chip
- Slower (~10 minutes)
- Use when everything is tested and ready

---

## 🚀 How to Test M-Chip Build Only

### Option 1: Manual Trigger (Recommended for Testing)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Test Mac M-chip fixes"
   git push origin main
   ```

2. **Go to GitHub Actions**:
   - Navigate to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
   - Click on **"Build Mac M-Chip Only (Test)"** workflow
   - Click **"Run workflow"** button
   - Select branch: `main`
   - Click **"Run workflow"**

3. **Watch the build** (~6 minutes):
   - Click on the running workflow
   - Watch the logs in real-time
   - Look for: "✅ SUCCESS: Native ARM64 build!"

4. **Download the build**:
   - Scroll down to "Artifacts"
   - Download: `Pxgate-macOS-AppleSilicon-M-Chip.zip`

### Option 2: Push a Tag (Creates Release)

```bash
# Push code
git add .
git commit -m "Mac M-chip test"
git push origin main

# Create and push tag
git tag v25.08.06-test
git push origin v25.08.06-test
```

This will:
- Build M-chip version only
- Create a GitHub Release
- Attach the ZIP file

---

## ⏱️ Time Comparison

| Workflow | Platforms | Time | Use Case |
|----------|-----------|------|----------|
| **build-mac-m-chip-only.yml** | M-chip only | ~6 min | Testing fixes |
| **build-all-platforms.yml** | All 3 | ~10 min | Full release |

**Savings**: ~4 minutes per test + saves Windows/Intel build minutes

---

## 🔍 What to Look For

### In the GitHub Actions Log

1. **Architecture Verification**:
   ```
   Python architecture: arm64
   Expected: arm64 for native M-chip build
   ```

2. **Package Verification**:
   ```
   ✓ numpy 1.26.x
   ✓ PySide6 6.x.x
   ✓ rawpy
   ✓ pillow_heif
   ```

3. **Build Success**:
   ```
   ✅ SUCCESS: Native ARM64 build!
   ```

### In the Downloaded Build

After downloading, verify locally:

```bash
# Extract the ZIP
unzip Pxgate-macOS-AppleSilicon-M-Chip.zip

# Check architecture (on a Mac)
file Pxgate.app/Contents/MacOS/Pxgate
# Should show: Mach-O 64-bit executable arm64

# Try to open (on M-chip Mac)
open Pxgate.app
```

---

## 🎯 Testing Checklist

After the build completes:

- [ ] Build shows "✅ SUCCESS: Native ARM64 build!"
- [ ] Artifact is available for download
- [ ] ZIP file size is reasonable (~180 MB)
- [ ] (If you have M-chip Mac) App launches without "already running" error
- [ ] (If you have M-chip Mac) RAW files load correctly
- [ ] (If you have M-chip Mac) No crashes during use

---

## 🔄 Iteration Workflow

For testing and fixing:

1. **Make changes** to code
2. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Fix attempt #1"
   git push origin main
   ```
3. **Manually trigger** M-chip-only workflow
4. **Wait 6 minutes**
5. **Check logs** for errors
6. **Download and test** (if you have M-chip Mac)
7. **Repeat** if needed

---

## 📊 GitHub Actions Minutes Usage

### M-Chip Only Build

- macOS runner: 10x multiplier
- Build time: ~6 minutes
- **Cost**: 60 minutes per build

### Full Build (All Platforms)

- Windows: ~5 min = 5 minutes
- macOS Intel: ~7 min = 70 minutes  
- macOS M-chip: ~6 min = 60 minutes
- **Cost**: 135 minutes per build

**Savings**: 75 minutes per test!

---

## 🎉 When to Switch to Full Build

Once M-chip build is working:

1. **Disable** or delete `build-mac-m-chip-only.yml`
2. **Use** `build-all-platforms.yml` for releases
3. **Push a proper version tag**: `v25.08.06`

---

## 🔧 Quick Commands

### Test M-Chip Only

```bash
# Push and manually trigger
git add .
git commit -m "Test M-chip"
git push origin main
# Then go to Actions tab and click "Run workflow"
```

### Test with Tag (Creates Release)

```bash
# Push with test tag
git add .
git commit -m "Test M-chip"
git push origin main
git tag v25.08.06-test
git push origin v25.08.06-test
```

### Full Release (All Platforms)

```bash
# When ready for production
git tag v25.08.06
git push origin v25.08.06
# This uses build-all-platforms.yml
```

---

## 📝 Notes

### Both Workflows Can Coexist

- Both `.yml` files can exist in `.github/workflows/`
- They trigger independently
- Use whichever you need

### Workflow Selection

GitHub Actions will run:
- **build-mac-m-chip-only.yml** when you manually trigger it OR push to main
- **build-all-platforms.yml** when you push a tag starting with `v`

You can control which runs by:
- Manual trigger (choose the workflow)
- Branch push (both may run)
- Tag push (build-all-platforms runs)

---

## ✅ Summary

**For Testing M-Chip Fixes**:
- Use: `build-mac-m-chip-only.yml`
- Time: ~6 minutes
- Trigger: Manual or push to main

**For Full Release**:
- Use: `build-all-platforms.yml`
- Time: ~10 minutes
- Trigger: Push version tag (v25.08.06)

**Start with M-chip only to verify the fixes work!** 🚀
