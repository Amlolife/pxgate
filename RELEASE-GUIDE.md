# Quick Release Guide

## 🎯 How to Create a Release

### Step 1: Prepare the Release

```bash
# Make sure all changes are committed
git status

# Update version if needed
# Edit: version.txt and version_info.txt

# Commit version changes
git add version.txt version_info.txt
git commit -m "Bump version to 1.0.0"
```

### Step 2: Create and Push Tag

```bash
# Create a version tag
git tag v1.0.0

# Push everything to GitHub
git push origin main --tags
```

### Step 3: Wait for GitHub Actions

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Watch the **Build All Platforms** workflow run
4. Wait for all 3 builds to complete (~10-15 minutes total)

### Step 4: Check the Release

1. Go to the **Releases** page
2. You'll see a new release with:
   - ✅ `Pxgate-Windows.zip`
   - ✅ `Pxgate-macOS-Intel.zip`
   - ✅ `Pxgate-macOS-AppleSilicon.zip`

### Step 5: Test (Optional but Recommended)

Download and test each build:
- Windows: Run `pxgate.exe`
- macOS Intel: Open `Pxgate.app` (right-click → Open)
- macOS ARM: Open `Pxgate.app` (right-click → Open)

---

## 🔧 Manual Build (Without Release)

If you just want to test builds without creating a release:

1. Go to **Actions** tab on GitHub
2. Click **Build All Platforms**
3. Click **Run workflow**
4. Select branch (usually `main`)
5. Click **Run workflow** button

Builds will be available as **Artifacts** (not as a release).

---

## 📋 Pre-Release Checklist

Before creating a release tag:

- [ ] All features tested and working
- [ ] Version numbers updated in:
  - [ ] `version.txt`
  - [ ] `version_info.txt`
- [ ] CHANGELOG updated (if you have one)
- [ ] All changes committed
- [ ] Code pushed to GitHub
- [ ] Local build tested on at least one platform

---

## 🏷️ Version Tag Format

Use semantic versioning with a `v` prefix:

- `v1.0.0` - Major release
- `v1.1.0` - Minor update (new features)
- `v1.1.1` - Patch (bug fixes)
- `v2.0.0` - Breaking changes

Examples:
```bash
git tag v1.0.0      # First release
git tag v1.1.0      # Added new features
git tag v1.1.1      # Fixed bugs
git tag v2.0.0      # Major rewrite
```

---

## 🚨 If Build Fails

### Check the Logs

1. Go to **Actions** tab
2. Click on the failed workflow
3. Click on the failed job (Windows/macOS Intel/macOS ARM)
4. Expand the failed step
5. Read the error message

### Common Issues

**Missing dependencies:**
```bash
# Update requirements.txt with the missing package
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

**Spec file errors:**
```bash
# Test locally first
pyinstaller pxgate.spec --noconfirm --clean
# OR for macOS
pyinstaller pxgate-mac.spec --noconfirm --clean
```

**Python version mismatch:**
- Workflow uses Python 3.11
- Make sure your code is compatible

### Retry Failed Build

After fixing the issue:

```bash
# Delete the failed tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Create the tag again
git tag v1.0.0
git push origin --tags
```

---

## 📊 Build Status

You can check build status at:
```
https://github.com/yourusername/VibeCulling/actions
```

Each platform builds independently, so if one fails, the others may still succeed.

---

## 🎉 After Release

1. **Announce** the release (social media, Discord, etc.)
2. **Monitor** GitHub Issues for bug reports
3. **Update** documentation if needed
4. **Plan** next release features

---

## 💡 Tips

- **Test locally before tagging**: Build on your machine first
- **Use pre-releases for testing**: Tag as `v1.0.0-beta.1` for beta versions
- **Keep a CHANGELOG**: Document what changed in each version
- **Semantic versioning**: Follow semver.org guidelines
- **Backup tags**: Keep a list of release tags in case you need to reference them

---

## 🔄 Workflow Files

Your GitHub Actions workflows:

- `.github/workflows/build-all-platforms.yml` - Main workflow (all 3 platforms)
- `.github/workflows/build-macos-matrix.yml` - macOS only (backup)

You can edit these files to customize the build process.

---

## 📞 Need Help?

- GitHub Actions docs: https://docs.github.com/en/actions
- PyInstaller docs: https://pyinstaller.org/
- This project's issues: https://github.com/yourusername/VibeCulling/issues
