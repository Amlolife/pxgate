# Integration Instructions for AI Features

This document explains how to integrate the new AI analysis features into the main `pxgate.py` file.

---

## Files Added

1. **`image_analyzer.py`** - Core analysis engine
2. **`analysis_integration.py`** - Qt integration and UI components
3. **`AI_FEATURES_GUIDE.md`** - User documentation

---

## Step-by-Step Integration

### Step 1: Add Imports to pxgate.py

Add these imports near the top of `pxgate.py` (around line 48, after existing imports):

```python
# AI Analysis imports
try:
    from analysis_integration import ImageAnalysisManager, AnalysisSettingsDialog, DuplicateViewerDialog
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"AI analysis features not available: {e}")
    ANALYSIS_AVAILABLE = False
```

---

### Step 2: Initialize Analysis Manager in PxgateApp.__init__()

Add this in the `PxgateApp.__init__()` method (around line 4950, after other initializations):

```python
# Initialize AI Analysis Manager
self.analysis_manager = None
if ANALYSIS_AVAILABLE:
    try:
        self.analysis_manager = ImageAnalysisManager(self)
        logging.info("AI Analysis features initialized")
    except Exception as e:
        logging.error(f"Failed to initialize AI analysis: {e}")
        self.analysis_manager = None
```

---

### Step 3: Add Analysis UI Elements

#### A. Add Analysis Button to Control Panel

In the `create_control_panel()` method (around line 5500), add after the "Client Selection" button:

```python
# AI Analysis button
if ANALYSIS_AVAILABLE and self.analysis_manager:
    self.analyze_button = QPushButton("🤖 Analyze Images")
    self.analyze_button.setEnabled(False)
    self.analyze_button.clicked.connect(self.start_image_analysis)
    self.analyze_button.setToolTip("Analyze image quality, faces, and duplicates")
    self.control_layout.addWidget(self.analyze_button)
    
    # Duplicates button
    self.duplicates_button = QPushButton("🔍 Find Duplicates")
    self.duplicates_button.setEnabled(False)
    self.duplicates_button.clicked.connect(self.show_duplicates_dialog)
    self.duplicates_button.setToolTip("View duplicate and similar images")
    self.control_layout.addWidget(self.duplicates_button)
```

#### B. Add Analysis Settings to Settings Dialog

In the `show_settings_popup()` method (around line 9000), add a new section:

```python
# AI Analysis Settings (if available)
if ANALYSIS_AVAILABLE and self.analysis_manager:
    analysis_section = QLabel("🤖 AI Analysis")
    analysis_section.setStyleSheet(TypographySystem.get_section_title_style())
    settings_layout.addWidget(analysis_section)
    
    analysis_settings_button = QPushButton("Configure Analysis Settings")
    analysis_settings_button.clicked.connect(self.show_analysis_settings)
    settings_layout.addWidget(analysis_settings_button)
    
    settings_layout.addSpacing(SpacingSystem.COMFORTABLE)
```

---

### Step 4: Add Analysis Display to File Info Panel

Modify the `update_file_info_display()` method (around line 12000) to include analysis data:

```python
def update_file_info_display(self, image_path):
    """Update file info display with EXIF and analysis data"""
    # ... existing EXIF code ...
    
    # Add AI Analysis section
    if ANALYSIS_AVAILABLE and self.analysis_manager:
        analysis_result = self.analysis_manager.get_analysis(image_path)
        if analysis_result and analysis_result.get('analyzed'):
            info_parts.append("\n📊 Quality Analysis:")
            info_parts.append(f"   Overall Score: {analysis_result['quality_score']:.1f}")
            info_parts.append(f"   Sharpness: {analysis_result['sharpness']:.1f}")
            info_parts.append(f"   Exposure: {analysis_result['exposure']['exposure_score']:.1f}")
            info_parts.append(f"   Noise: {analysis_result['noise_score']:.1f}")
            info_parts.append(f"   Composition: {analysis_result['composition_score']:.1f}")
            
            # Face detection results
            face_data = analysis_result.get('face_data', {})
            if face_data.get('face_count', 0) > 0:
                info_parts.append("\n👤 Face Detection:")
                info_parts.append(f"   Faces: {face_data['face_count']}")
                if face_data.get('has_eyes'):
                    info_parts.append("   Eyes: ✓")
                if face_data.get('has_smile'):
                    info_parts.append("   Smiles: ✓")
    
    # ... rest of existing code ...
```

---

### Step 5: Add Analysis Methods

Add these new methods to the `PxgateApp` class:

```python
def start_image_analysis(self):
    """Start analyzing loaded images"""
    if not self.analysis_manager or not self.image_files:
        return
    
    # Convert Path objects to strings
    image_paths = [str(path) for path in self.image_files]
    
    # Start analysis
    self.analysis_manager.start_analysis(image_paths, show_progress=True)
    
    logging.info(f"Started analysis of {len(image_paths)} images")

def show_duplicates_dialog(self):
    """Show dialog with duplicate images"""
    if not self.analysis_manager:
        return
    
    self.analysis_manager.show_duplicates_dialog()

def show_analysis_settings(self):
    """Show analysis settings dialog"""
    if not self.analysis_manager:
        return
    
    self.analysis_manager.show_settings_dialog()

def update_analysis_display(self, result: dict):
    """Update UI with analysis results (called by analysis manager)"""
    # Refresh file info if this is the current image
    current_path = self.get_current_image_path()
    if current_path == result.get('path'):
        self.update_file_info_display(current_path)

def navigate_to_image_by_path(self, image_path: str):
    """Navigate to a specific image by its path"""
    try:
        image_path_obj = Path(image_path)
        if image_path_obj in self.image_files:
            index = self.image_files.index(image_path_obj)
            self.current_image_index = index
            self.display_image()
            logging.info(f"Navigated to image: {image_path_obj.name}")
        else:
            logging.warning(f"Image not found in current list: {image_path}")
    except Exception as e:
        logging.error(f"Error navigating to image: {e}")
```

---

### Step 6: Auto-Start Analysis on Folder Load

Modify the `load_folder()` method (around line 6000) to auto-start analysis:

```python
def load_folder(self):
    """Load images from folder"""
    # ... existing folder loading code ...
    
    # After successfully loading images:
    if self.image_files:
        # Enable analysis buttons
        if hasattr(self, 'analyze_button'):
            self.analyze_button.setEnabled(True)
        if hasattr(self, 'duplicates_button'):
            self.duplicates_button.setEnabled(False)  # Enable after analysis
        
        # Auto-start analysis if enabled
        if (ANALYSIS_AVAILABLE and self.analysis_manager and 
            self.analysis_manager.settings.get('auto_analyze_on_load', True)):
            # Start analysis after a short delay
            QTimer.singleShot(1000, self.start_image_analysis)
```

---

### Step 7: Add Keyboard Shortcuts

In the `keyPressEvent()` method (around line 13000), add new shortcuts:

```python
def keyPressEvent(self, event):
    # ... existing key handling ...
    
    # AI Analysis shortcuts
    if ANALYSIS_AVAILABLE and self.analysis_manager:
        # Alt+A: Start analysis
        if event.key() == Qt.Key_A and event.modifiers() == Qt.AltModifier:
            self.start_image_analysis()
            event.accept()
            return
        
        # Alt+D: Show duplicates
        if event.key() == Qt.Key_D and event.modifiers() == Qt.AltModifier:
            self.show_duplicates_dialog()
            event.accept()
            return
        
        # Alt+S: Analysis settings
        if event.key() == Qt.Key_S and event.modifiers() == Qt.AltModifier:
            self.show_analysis_settings()
            event.accept()
            return
    
    # ... rest of existing key handling ...
```

---

### Step 8: Add Sorting and Filtering Options

Add these methods for sorting/filtering by quality:

```python
def sort_by_quality(self, reverse=True):
    """Sort images by quality score"""
    if not self.analysis_manager or not self.image_files:
        return
    
    # Convert to strings for sorting
    paths_str = [str(p) for p in self.image_files]
    sorted_paths = self.analysis_manager.get_sorted_by_quality(paths_str, reverse)
    
    # Convert back to Path objects
    self.image_files = [Path(p) for p in sorted_paths]
    self.current_image_index = 0
    self.display_image()
    
    logging.info(f"Sorted by quality ({'high to low' if reverse else 'low to high'})")

def toggle_quality_filter(self):
    """Toggle quality-based filtering"""
    if not self.analysis_manager:
        return
    
    current = self.analysis_manager.settings['enable_quality_filter']
    self.analysis_manager.settings['enable_quality_filter'] = not current
    
    # Refresh image list
    self.refresh_folder()
    
    status = "enabled" if not current else "disabled"
    logging.info(f"Quality filter {status}")
```

---

### Step 9: Update State Saving/Loading

Modify `save_state()` and `load_state()` to include analysis settings:

```python
def save_state(self):
    # ... existing state saving ...
    
    # Save analysis settings
    if ANALYSIS_AVAILABLE and self.analysis_manager:
        state['analysis_settings'] = self.analysis_manager.settings
    
    # ... rest of save code ...

def load_state(self):
    # ... existing state loading ...
    
    # Load analysis settings
    if ANALYSIS_AVAILABLE and self.analysis_manager:
        if 'analysis_settings' in state:
            self.analysis_manager.settings.update(state['analysis_settings'])
    
    # ... rest of load code ...
```

---

### Step 10: Add Cleanup on Exit

In the `closeEvent()` method (around line 16000):

```python
def closeEvent(self, event):
    # ... existing cleanup ...
    
    # Stop analysis and cleanup
    if ANALYSIS_AVAILABLE and self.analysis_manager:
        self.analysis_manager.stop_analysis()
        self.analysis_manager.clear_results()
    
    # ... rest of cleanup ...
```

---

## Testing Checklist

After integration, test these features:

- [ ] Analysis starts automatically when loading folder
- [ ] Progress dialog shows during analysis
- [ ] Quality scores appear in file info panel
- [ ] Face detection results display correctly
- [ ] Duplicate detection finds similar images
- [ ] Duplicate dialog shows groups correctly
- [ ] Double-clicking duplicate group navigates to image
- [ ] Analysis settings dialog works
- [ ] Keyboard shortcuts (Alt+A, Alt+D, Alt+S) work
- [ ] Sorting by quality works
- [ ] Quality filtering works
- [ ] Settings are saved/loaded correctly
- [ ] Analysis stops cleanly on app exit

---

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install opencv-python imagehash
```

### Performance Issues

If analysis is too slow:
1. Disable face detection in settings
2. Reduce number of images loaded
3. Increase analysis worker threads in `ImageAnalysisEngine`

### UI Not Updating

If analysis results don't show:
1. Check that `update_analysis_display()` is being called
2. Verify `update_file_info_display()` includes analysis section
3. Check logs for errors

---

## Optional Enhancements

### Add Menu Items

Create a new "Analysis" menu:

```python
# In create_menus() or similar
analysis_menu = self.menuBar().addMenu("Analysis")

analyze_action = QAction("Analyze Images", self)
analyze_action.setShortcut("Alt+A")
analyze_action.triggered.connect(self.start_image_analysis)
analysis_menu.addAction(analyze_action)

duplicates_action = QAction("Find Duplicates", self)
duplicates_action.setShortcut("Alt+D")
duplicates_action.triggered.connect(self.show_duplicates_dialog)
analysis_menu.addAction(duplicates_action)

settings_action = QAction("Analysis Settings", self)
settings_action.setShortcut("Alt+S")
settings_action.triggered.connect(self.show_analysis_settings)
analysis_menu.addAction(settings_action)
```

### Add Visual Indicators

Show quality score badge on thumbnails:

```python
# In grid view rendering
if ANALYSIS_AVAILABLE and self.analysis_manager:
    result = self.analysis_manager.get_analysis(image_path)
    if result and result.get('analyzed'):
        score = result['quality_score']
        # Draw score badge on thumbnail
        # (implementation depends on your thumbnail rendering)
```

---

## Complete!

After following these steps, your Pxgate application will have full AI-powered analysis capabilities!

For user documentation, refer to `AI_FEATURES_GUIDE.md`.
