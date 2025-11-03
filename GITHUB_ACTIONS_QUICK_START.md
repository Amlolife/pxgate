# GitHub Actions Quick Start - Build Mac M-Chip Without a Mac!

## ✅ What's Ready

Your GitHub Actions workflow is **fully configured** to build for Mac M-chip (Apple Silicon) automatically. You don't need a Mac!

---

## 🚀 How to Build & Release (3 Steps)

### Step 1: Push Your Code to GitHub

```bash
# Add all changes
git add .

# Commit with a message
git commit -m "Add Mac M-chip compatibility fixes"

# Push to GitHub
git push origin main
```

**Note**: Replace `main` with `master` if your default branch is master.

---

### Step 2: Create a Version Tag

```bash
# Create a version tag (use v prefix!)
git tag v25.08.06

# Push the tag to GitHub
git push origin v25.08.06
```

**Important**: Always use the `v` prefix (v1.0.0, v2.1.3, etc.)

---

### Step 3: Wait for GitHub to Build

1. Go to your GitHub repository
2. Click the **"Actions"** tab
3. Watch the build progress (takes ~10 minutes)
4. When done, go to **"Releases"** tab
5. Download your builds!

---

## 📦 What You'll Get

After the build completes, you'll have **3 downloadable files**:

1. **Pxgate-Windows.zip** - For Windows 10+
2. **Pxgate-macOS-Intel.zip** - For Intel Macs
3. **Pxgate-macOS-AppleSilicon.zip** - For M1/M2/M3/M4 Macs ⚡

All builds are **automatically created** and **uploaded to GitHub Releases**.

---

## 🎯 GitHub Actions Workflow

### What Happens Automatically

```
You push tag (v25.08.06)
    ↓
GitHub Actions triggers
    ↓
Builds 3 platforms in parallel:
    ├─ Windows (runs-on: windows-latest)
    ├─ macOS Intel (runs-on: macos-13)
    └─ macOS ARM64 (runs-on: macos-14) ← M-chip!
    ↓
Each build:
    1. Checks out your code
    2. Installs Python 3.11
    3. Installs dependencies
    4. Verifies architecture
    5. Builds with PyInstaller
    6. Creates ZIP file
    ↓
Creates GitHub Release
    ↓
Uploads all 3 builds
    ↓
Done! 🎉
```

**Total time: ~10 minutes**

---

## 🔍 How to Monitor Builds

### Watch Build Progress

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Click on the latest workflow run
3. Click on each job to see detailed logs:
   - **Build Windows**
   - **Build macOS Intel**
   - **Build macOS Apple Silicon (M-Chip)** ← This is the M-chip build!

### Check Build Architecture

In the **"Build macOS Apple Silicon"** job, look for:

```
Verify build architecture
✅ Native ARM64 build successful!
```

This confirms it's a native M-chip build (not Rosetta 2).

---

## 📥 How to Download Builds

### Option 1: From Releases (Recommended)

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases`
2. Click on the latest release (e.g., `v25.08.06`)
3. Download the files under "Assets"

### Option 2: From Actions (For Testing)

1. Go to: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Click on a completed workflow run
3. Scroll down to "Artifacts"
4. Download individual builds (expires after 30 days)

---

## 🔄 Manual Trigger (No Release)

You can also trigger builds manually without creating a release:

1. Go to **Actions** tab
2. Click **"Build All Platforms"** workflow
3. Click **"Run workflow"** button
4. Select branch (usually `main`)
5. Click **"Run workflow"**

**Note**: Manual builds don't create a release, but artifacts are available for 30 days.

---

## 🎯 What's Different from Before

### Old Way (Your Previous Setup)
- Used `pxgate-simple.spec` (basic config)
- No architecture verification
- No M-chip specific fixes

### New Way (Current Setup)
- Uses `pxgate-mac.spec` (M-chip optimized)
- Verifies ARM64 architecture
- Includes all M-chip compatibility fixes:
  - ✅ Multiprocessing lock fix
  - ✅ Stale lock detection
  - ✅ Child process handling
  - ✅ Explicit spawn method

---

## 🔧 Workflow Configuration

### File Location
```
.github/workflows/build-all-platforms.yml
```

### Key Changes Made

1. **Triggers on main/master branches**
   ```yaml
   on:
     push:
       branches:
         - 'main'
         - 'master'
       tags:
         - 'v*'
   ```

2. **Uses pxgate-mac.spec** (has M-chip fixes)
   ```yaml
   pyinstaller pxgate-mac.spec --noconfirm --clean
   ```

3. **Verifies ARM64 architecture**
   ```yaml
   file dist/Pxgate.app/Contents/MacOS/Pxgate
   # Should show: arm64
   ```

4. **Tests critical packages**
   ```yaml
   python -c "import numpy; print('✓ numpy')"
   python -c "import rawpy; print('✓ rawpy')"
   ```

---

## 📊 Build Matrix

| Runner | OS | Architecture | Python Arch | Build Output |
|--------|----|--------------| ------------|--------------|
| `windows-latest` | Windows Server 2022 | x64 | x64 | Windows .exe |
| `macos-13` | macOS 13 Ventura | Intel | x86_64 | Intel .app |
| `macos-14` | macOS 14 Sonoma | Apple Silicon | arm64 | M-chip .app |

---

## 💰 Cost (GitHub Actions Minutes)

### For Public Repositories
- **FREE** unlimited minutes
- All platforms included
- No credit card needed

### For Private Repositories
- **2,000 free minutes/month**
- Windows: 1x multiplier
- macOS: 10x multiplier

**Example**: One full build uses:
- Windows: ~5 minutes = 5 minutes
- macOS Intel: ~7 minutes = 70 minutes
- macOS ARM: ~6 minutes = 60 minutes
- **Total: 135 minutes per release**

With 2,000 free minutes, you can make **~14 releases/month** for free.

---

## 🐛 Troubleshooting

### Build Fails on macOS ARM

**Check the logs for:**

1. **Architecture mismatch**
   ```
   Expected: arm64
   Got: x86_64
   ```
   → This shouldn't happen with macos-14 runner

2. **Package installation failure**
   ```
   ERROR: Could not find a version that satisfies...
   ```
   → Check `requirements.txt` has correct versions

3. **PyInstaller errors**
   ```
   ModuleNotFoundError: No module named 'multiprocessing'
   ```
   → Check imports in `pxgate.py`

### Release Not Created

**Possible reasons:**

1. **No version tag**
   - Solution: Push a tag starting with `v`
   
2. **Tag doesn't start with 'v'**
   - Solution: Use `v1.0.0` not `1.0.0`

3. **Build failed**
   - Solution: Check Actions tab for errors

### Artifacts Not Available

- Artifacts expire after 30 days
- Create a release to keep builds permanently

---

## 📝 Version Numbering

### Recommended Format

```
v[MAJOR].[MINOR].[PATCH]

Examples:
v1.0.0    - First release
v1.0.1    - Bug fix
v1.1.0    - New features
v2.0.0    - Breaking changes
```

### Your Current Version
```
v25.08.06  - Based on date (2025-08-06)
```

---

## 🎉 Quick Commands Cheat Sheet

```bash
# Create and push a release
git tag v25.08.06
git push origin v25.08.06

# Delete a tag (if you made a mistake)
git tag -d v25.08.06
git push origin :refs/tags/v25.08.06

# List all tags
git tag -l

# Push all changes and create release
git add .
git commit -m "Update"
git push origin main
git tag v25.08.06
git push origin v25.08.06
```

---

## ✅ Verification Checklist

After pushing a tag, verify:

- [ ] Actions tab shows workflow running
- [ ] All 3 jobs (Windows, Intel, ARM) complete successfully
- [ ] macOS ARM job shows "✅ Native ARM64 build successful!"
- [ ] Release is created automatically
- [ ] All 3 ZIP files are attached to the release
- [ ] Release notes are generated

---

## 🔗 Useful Links

After you push to GitHub, bookmark these:

- **Actions**: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
- **Releases**: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases`
- **Latest Release**: `https://github.com/YOUR_USERNAME/YOUR_REPO/releases/latest`

---

## 📞 Next Steps

1. **Push your code** to GitHub
2. **Create a tag**: `git tag v25.08.06 && git push origin v25.08.06`
3. **Watch the magic happen** in the Actions tab
4. **Download your builds** from the Releases tab
5. **Share with users**!

---

## 🎯 Summary

✅ **No Mac needed** - GitHub provides M-chip runners  
✅ **Automatic builds** - Just push a tag  
✅ **Native ARM64** - Full M-chip optimization  
✅ **All fixes included** - Lock file, multiprocessing, etc.  
✅ **Free for public repos** - Unlimited builds  
✅ **Professional distribution** - GitHub Releases  

**You're all set! Just push and let GitHub build for you! 🚀**
