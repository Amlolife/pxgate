# GitHub Actions Setup - Complete Guide

## ✅ What's Already Set Up

I've created the following files for you:

1. **`.github/workflows/build-all-platforms.yml`** - Main workflow that builds all 3 platforms
2. **`BUILD.md`** - Developer build instructions
3. **`INSTALL.md`** - End-user installation guide
4. **`RELEASE-GUIDE.md`** - Quick reference for creating releases

## 🚀 How It Works

### Automatic Builds

When you push a **version tag** (like `v1.0.0`), GitHub Actions will:

1. ✅ Build **Windows** executable on `windows-latest` runner
2. ✅ Build **macOS Intel** app on `macos-13` runner (Intel)
3. ✅ Build **macOS Apple Silicon** app on `macos-14` runner (ARM)
4. ✅ Create a **GitHub Release** automatically
5. ✅ Upload all 3 builds to the release

### Manual Builds

You can also trigger builds manually from the GitHub Actions tab without creating a release.

---

## 📝 First-Time Setup

### 1. Push Your Code to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/VibeCulling.git

# Push to GitHub
git push -u origin main
```

### 2. Enable GitHub Actions

GitHub Actions should be enabled by default. To verify:

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. If you see "Get started with GitHub Actions", click **"I understand my workflows, go ahead and enable them"**

### 3. Create Your First Release

```bash
# Make sure everything is committed
git status

# Create a version tag
git tag v1.0.0

# Push the tag
git push origin --tags
```

### 4. Watch the Build

1. Go to **Actions** tab
2. You'll see **Build All Platforms** workflow running
3. Wait for all 3 jobs to complete (green checkmarks)
4. Go to **Releases** tab to see your release

---

## 🎯 Workflow Triggers

The workflow runs when:

1. **You push a version tag** (e.g., `v1.0.0`, `v2.1.3`)
   - Creates a GitHub Release with all builds
   
2. **You manually trigger it** from Actions tab
   - Builds all platforms but doesn't create a release
   - Artifacts available for 30 days

---

## 📦 What Gets Built

### Windows Build
- **Runner**: `windows-latest` (Windows Server 2022)
- **Python**: 3.11
- **Output**: `Pxgate-Windows.zip` containing `pxgate.exe` and dependencies
- **Size**: ~300 MB
- **Build time**: ~5 minutes

### macOS Intel Build
- **Runner**: `macos-13` (Intel-based macOS)
- **Python**: 3.11
- **Output**: `Pxgate-macOS-Intel.zip` containing `Pxgate.app`
- **Size**: ~350 MB
- **Build time**: ~7 minutes

### macOS Apple Silicon Build
- **Runner**: `macos-14` (ARM-based macOS)
- **Python**: 3.11
- **Output**: `Pxgate-macOS-AppleSilicon.zip` containing `Pxgate.app`
- **Size**: ~320 MB
- **Build time**: ~6 minutes

---

## 🔧 Customizing the Workflow

### Change Python Version

Edit `.github/workflows/build-all-platforms.yml`:

```yaml
- name: Set up Python 3.11
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'  # Change this
```

### Add Build Steps

Add steps after the build step:

```yaml
- name: Build Windows executable
  run: |
    pyinstaller pxgate.spec --noconfirm --clean

- name: Run tests  # NEW STEP
  run: |
    pytest tests/
```

### Change Trigger Conditions

```yaml
on:
  push:
    tags:
      - 'v*'          # Triggers on v1.0.0, v2.1.3, etc.
      - 'release-*'   # Also trigger on release-1.0.0
  workflow_dispatch:  # Manual trigger
```

---

## 📊 Monitoring Builds

### View Build Status

1. Go to **Actions** tab
2. Click on a workflow run
3. See status of all 3 jobs:
   - 🟢 Green = Success
   - 🔴 Red = Failed
   - 🟡 Yellow = In progress

### View Build Logs

1. Click on a job (e.g., "Build Windows")
2. Expand each step to see detailed logs
3. Download logs if needed (top right corner)

### Download Artifacts (Manual Builds)

If you triggered manually (no release):

1. Go to the workflow run
2. Scroll down to **Artifacts** section
3. Download the builds you need

---

## 🚨 Troubleshooting

### Build Fails on Windows

**Common causes:**
- Missing dependencies in `requirements.txt`
- Spec file errors
- Python version incompatibility

**Solution:**
1. Check the error logs in Actions tab
2. Test locally: `pyinstaller pxgate.spec --noconfirm --clean`
3. Fix the issue and push again

### Build Fails on macOS

**Common causes:**
- macOS-specific dependencies missing
- Architecture mismatch (x86_64 vs arm64)
- Qt/PySide6 issues

**Solution:**
1. Check if `pxgate-mac.spec` exists and is correct
2. Verify `requirements.txt` has `PySide6>=6.5,<6.6`
3. Test locally on a Mac if possible

### Release Not Created

**Possible reasons:**
- Tag doesn't start with `v` (e.g., `1.0.0` instead of `v1.0.0`)
- One or more builds failed
- GitHub token permissions issue

**Solution:**
```bash
# Delete and recreate tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag v1.0.0
git push origin --tags
```

---

## 💰 GitHub Actions Costs

### Free Tier (Public Repositories)
- ✅ **Unlimited** minutes for public repos
- ✅ All 3 platforms included
- ✅ No cost to you

### Private Repositories
- 2,000 minutes/month free
- Windows: 2x multiplier (1 min = 2 mins)
- macOS: 10x multiplier (1 min = 10 mins)

**Example cost for private repo:**
- Windows build: 5 min × 2 = 10 minutes
- macOS Intel: 7 min × 10 = 70 minutes
- macOS ARM: 6 min × 10 = 60 minutes
- **Total per release: 140 minutes**

With 2,000 free minutes, you can do ~14 releases/month for free.

---

## ✅ Checklist

Before your first release:

- [ ] Code pushed to GitHub
- [ ] GitHub Actions enabled
- [ ] `.github/workflows/build-all-platforms.yml` exists
- [ ] `pxgate.spec` exists (Windows)
- [ ] `pxgate-mac.spec` exists (macOS)
- [ ] `requirements.txt` is up to date
- [ ] Version numbers updated
- [ ] Ready to create tag

---

## 🎉 You're All Set!

Your repository is now configured to automatically build for all 3 platforms.

**Next steps:**
1. Push your code to GitHub
2. Create a version tag: `git tag v1.0.0 && git push --tags`
3. Watch the magic happen in the Actions tab
4. Download your builds from the Releases page

**Questions?**
- Check `BUILD.md` for build details
- Check `RELEASE-GUIDE.md` for release process
- Check `INSTALL.md` for user installation guide

Happy releasing! 🚀
