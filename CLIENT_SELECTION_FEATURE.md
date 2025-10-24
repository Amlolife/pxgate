# 📋 Client Selection Feature

## Overview
A new feature that allows photographers to quickly copy files selected by their clients to a final delivery folder.

## Use Case
1. **Photographer** sorts and sends photos to client
2. **Client** reviews and sends back a list of file numbers/names they want
3. **Photographer** uses this feature to quickly copy those files to a delivery folder

## How to Use

### Step 1: Load Your Images
- Load your photo folder as usual
- The "📋 Client Selection" button will become enabled

### Step 2: Open Client Selection Dialog
- Click the "📋 Client Selection" button in the control panel
- A dialog will appear

### Step 3: Paste File Names
Paste the file numbers or names the client sent you. The feature accepts:
- **Comma-separated**: `IMG_1234, DSC_5678, IMG_1240`
- **Line-separated**:
  ```
  IMG_1234
  DSC_5678
  IMG_1240
  ```
- **Space-separated**: `IMG_1234 DSC_5678 IMG_1240`
- **Mixed formats**: Any combination of the above

### Step 4: Select Destination Folder
- Click "Select Folder..." button
- Choose where you want to copy the selected files
- The folder path will be displayed

### Step 5: Copy Files
- Click "Copy Files" button
- A progress dialog will show the copying process
- When complete, you'll see a summary:
  - Number of files successfully copied
  - Number of files not found
  - List of files that couldn't be found (if any)

## Features

### Smart File Matching
The feature intelligently matches file names:
- Works with or without file extensions
- Case-insensitive matching
- Partial name matching (e.g., "1234" will match "IMG_1234.jpg")

### File Formats Supported
- Copies the exact files from your loaded image list
- Works with JPG, RAW, HEIC, and all other loaded formats
- Preserves original file metadata

### Progress Tracking
- Shows real-time progress during copying
- Can be canceled mid-process
- Reports success/failure for each file

### Error Handling
- Lists files that couldn't be found
- Shows which files were successfully copied
- Continues copying even if some files fail

## Example Workflow

**Client sends you:**
```
Hi! I'd like these photos:
IMG_1234
IMG_1240
DSC_5678
IMG_1299
```

**You:**
1. Open Pxgate with your photo session
2. Click "📋 Client Selection"
3. Copy and paste the client's list
4. Select your "Final Delivery" folder
5. Click "Copy Files"
6. Done! All selected files are copied

## Benefits

✅ **Fast** - No manual searching through folders
✅ **Accurate** - No risk of copying wrong files
✅ **Flexible** - Accepts various input formats
✅ **Safe** - Copies files (doesn't move them)
✅ **Smart** - Finds files even with partial names
✅ **Bilingual** - Works in English and Korean

## Technical Details

- **Operation**: Copy (not move) - original files remain untouched
- **Matching**: Case-insensitive, supports partial matches
- **Performance**: Handles large file lists efficiently
- **Safety**: Validates all inputs before copying

## Translations

The feature is fully translated:
- **Korean**: 클라이언트 선택
- **English**: Client Selection

All dialog text, buttons, and messages are bilingual.

---

**This feature saves photographers hours of manual file sorting!** 🎉
