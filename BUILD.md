# Build & Release Guide

## 🚀 Automated Builds (GitHub Actions)

This project uses GitHub Actions to automatically build for all platforms.

### Trigger a Build

#### Option 1: Create a Release Tag (Recommended)

```bash
# Commit your changes
git add .
git commit -m "Release version 1.0.0"

# Create and push a version tag
git tag v1.0.0
git push origin main --tags
```

This will automatically:
1. ✅ Build Windows executable
2. ✅ Build macOS Intel app
3. ✅ Build macOS Apple Silicon app
4. ✅ Create a GitHub Release
5. ✅ Upload all three builds to the release

#### Option 2: Manual Trigger

1. Go to your GitHub repository
2. Click **Actions** tab
3. Select **Build All Platforms** workflow
4. Click **Run workflow** button
5. Select branch and click **Run workflow**

This will build all platforms but **won't create a release** (artifacts only).

---

## 📦 Build Outputs

After the workflow completes, you'll get:

### If triggered by tag (v*):
- **GitHub Release** with three downloadable files:
  - `Pxgate-Windows.zip` (~300 MB)
  - `Pxgate-macOS-Intel.zip` (~350 MB)
  - `Pxgate-macOS-AppleSilicon.zip` (~320 MB)

### If manually triggered:
- **Artifacts** available in the Actions tab (30-day retention)

---

## 🛠️ Local Build Instructions

### Windows

```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Build
pyinstaller pxgate.spec --noconfirm --clean

# Output: dist\pxgate\pxgate.exe
```

### macOS Intel

```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Build
pyinstaller pxgate-mac.spec --target-arch x86_64 --noconfirm --clean

# Output: dist/Pxgate.app
```

### macOS Apple Silicon

```bash
# Install dependencies
pip install -r requirements.txt pyinstaller

# Build
pyinstaller pxgate-mac.spec --target-arch arm64 --noconfirm --clean

# Output: dist/Pxgate.app
```

---

## 📋 Release Checklist

Before creating a release:

- [ ] Update version in `version.txt`
- [ ] Update version in `version_info.txt` (Windows)
- [ ] Test the app locally on Windows
- [ ] Update CHANGELOG.md (if exists)
- [ ] Commit all changes
- [ ] Create and push version tag
- [ ] Wait for GitHub Actions to complete
- [ ] Verify all three builds in the release
- [ ] Test downloaded builds on each platform

---

## 🔍 Troubleshooting

### Build fails on GitHub Actions

**Check the logs:**
1. Go to Actions tab
2. Click on the failed workflow run
3. Click on the failed job
4. Expand the failed step to see error details

**Common issues:**
- Missing dependencies: Update `requirements.txt`
- Python version mismatch: Ensure Python 3.11 is specified
- Spec file errors: Test locally first

### macOS Gatekeeper Warning

Users will see: *"Pxgate.app can't be opened because it is from an unidentified developer"*

**Solution:**
1. Right-click on `Pxgate.app`
2. Select "Open"
3. Click "Open" in the dialog

**To avoid (requires Apple Developer account - $99/year):**
```bash
# Sign the app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  dist/Pxgate.app

# Notarize (optional, for smoother user experience)
xcrun notarytool submit Pxgate.zip \
  --apple-id your@email.com \
  --team-id TEAMID \
  --password app-specific-password
```

---

## 📊 Build Matrix

| Platform | Runner | Python | Architecture | Output |
|----------|--------|--------|--------------|--------|
| Windows | `windows-latest` | 3.11 | x64 | `pxgate.exe` |
| macOS Intel | `macos-13` | 3.11 | x86_64 | `Pxgate.app` |
| macOS ARM | `macos-14` | 3.11 | arm64 | `Pxgate.app` |

---

## 🎯 Version Numbering

Use semantic versioning: `vMAJOR.MINOR.PATCH`

Examples:
- `v1.0.0` - First stable release
- `v1.1.0` - New features added
- `v1.1.1` - Bug fixes
- `v2.0.0` - Breaking changes

---

## 📝 Notes

- **Build time**: ~5-10 minutes per platform
- **Artifact retention**: 30 days (configurable in workflow)
- **Release notes**: Auto-generated from commits
- **No code signing**: Users must right-click → Open on macOS first time
- **All dependencies bundled**: No Python installation required for end users
