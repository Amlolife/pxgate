"""
Integration module for connecting ImageAnalysisEngine to Pxgate
Handles background analysis, UI updates, and user interactions
"""

from PySide6.QtCore import QObject, Signal, QThread, QTimer, Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QProgressBar, QListWidget, QListWidgetItem,
                              QCheckBox, QSpinBox, QGroupBox, QTextEdit, QMessageBox)
from PySide6.QtGui import QFont, QColor
from shiboken6 import isValid
import logging
from pathlib import Path
from typing import List, Dict, Optional
import time

try:
    from image_analyzer import ImageAnalysisEngine
    ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Image analysis not available: {e}")
    ANALYSIS_AVAILABLE = False


class AnalysisWorker(QObject):
    """Worker thread for background image analysis"""
    
    progress = Signal(int, int)  # current, total
    image_analyzed = Signal(str, dict)  # path, result
    batch_complete = Signal(dict, list)  # all results, duplicate_groups
    error = Signal(str)  # error message
    
    def __init__(self, image_paths: List[str], include_faces: bool = True, similarity_threshold: int = 5):
        super().__init__()
        self.image_paths = image_paths
        self.include_faces = include_faces
        self.is_running = True
        self.engine = None
        self.similarity_threshold = similarity_threshold
    
    def run(self):
        """Run the analysis in background"""
        logging.info("=== AnalysisWorker.run() STARTED - NEW VERSION ===")
        if not ANALYSIS_AVAILABLE:
            self.error.emit("Image analysis libraries not available")
            return
        
        try:
            # Initialize engine
            self.engine = ImageAnalysisEngine(max_workers=2, similarity_threshold=self.similarity_threshold)
            
            results = {}
            total = len(self.image_paths)
            
            for idx, path in enumerate(self.image_paths):
                if not self.is_running:
                    break
                
                try:
                    result = self.engine.analyze_image(path, self.include_faces)
                    results[path] = result
                    self.image_analyzed.emit(path, result)
                    self.progress.emit(idx + 1, total)
                except Exception as e:
                    logging.error(f"Analysis error for {path}: {e}")
                    self.error.emit(f"Error analyzing {Path(path).name}: {str(e)}")
            
            if self.is_running:
                # Find duplicates in worker thread (before emitting signal)
                duplicate_groups = []
                if self.engine:
                    try:
                        duplicate_groups = self.engine.get_duplicate_groups()
                        logging.info(f"Found {len(duplicate_groups)} duplicate groups")
                    except Exception as e:
                        logging.error(f"Duplicate detection error: {e}")
                
                # DON'T shutdown here - let it happen naturally when thread exits
                # The engine will be cleaned up by Python's garbage collector
                logging.info(f"Analysis complete, about to emit signal with {len(results)} results")
                
                # Emit completion signal with a COPY of results to avoid threading issues
                try:
                    # Create a shallow copy to avoid any reference issues
                    results_copy = dict(results)
                    logging.info(f"Created results copy, emitting signal...")
                    self.batch_complete.emit(results_copy, duplicate_groups)
                    logging.info("batch_complete signal emitted successfully")
                except Exception as e:
                    logging.error(f"Error emitting batch_complete signal: {e}", exc_info=True)
            
        except Exception as e:
            logging.error(f"Analysis worker error: {e}")
            self.error.emit(str(e))
    
    def stop(self):
        """Stop the analysis"""
        self.is_running = False


class AnalysisProgressDialog(QDialog):
    """Dialog showing analysis progress"""
    
    def __init__(self, total_images: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analyzing Images")
        self.setModal(False)  # Non-modal to prevent blocking
        self.setMinimumWidth(500)
        
        # Prevent closing with X button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        
        layout = QVBoxLayout(self)
        
        # Info label
        self.info_label = QLabel("Analyzing image quality, faces, and duplicates...")
        layout.addWidget(self.info_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(total_images)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Starting analysis...")
        layout.addWidget(self.status_label)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        
        self.start_time = time.time()
    
    def update_progress(self, current: int, total: int):
        """Update progress display"""
        self.progress_bar.setValue(current)
        
        # Calculate ETA
        elapsed = time.time() - self.start_time
        if current > 0:
            avg_time = elapsed / current
            remaining = (total - current) * avg_time
            eta_str = f"{int(remaining)}s"
        else:
            eta_str = "calculating..."
        
        # Show percentage
        percentage = int((current / total) * 100) if total > 0 else 0
        
        self.status_label.setText(
            f"Analyzed {current} of {total} images ({percentage}%, ETA: {eta_str})"
        )


class DuplicateViewerDialog(QDialog):
    """Dialog for viewing and managing duplicate images"""
    
    def __init__(self, duplicate_groups: List[List[str]], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Duplicate & Similar Images")
        self.setMinimumSize(700, 500)
        self.duplicate_groups = duplicate_groups
        self.parent_app = parent
        
        layout = QVBoxLayout(self)
        
        # Info
        info_text = f"Found {len(duplicate_groups)} groups of similar images"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(info_label)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)
        
        # Populate list
        for idx, group in enumerate(duplicate_groups):
            group_text = f"Group {idx + 1} ({len(group)} images):\n"
            for path in group:
                group_text += f"  • {Path(path).name}\n"
            
            item = QListWidgetItem(group_text)
            item.setData(1, group)  # Store group data
            self.list_widget.addItem(item)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.view_button = QPushButton("View Selected Group")
        self.view_button.clicked.connect(self.view_selected_group)
        button_layout.addWidget(self.view_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def on_item_double_clicked(self, item):
        """Handle double-click on duplicate group"""
        self.view_selected_group()
    
    def view_selected_group(self):
        """Navigate to first image in selected group"""
        current_item = self.list_widget.currentItem()
        if not current_item:
            return
        
        group = current_item.data(1)
        if group and len(group) > 0:
            first_image = group[0]
            # Try to navigate to this image in the main app
            if self.parent_app and hasattr(self.parent_app, 'navigate_to_image_by_path'):
                self.parent_app.navigate_to_image_by_path(first_image)
                self.accept()


class AnalysisSettingsDialog(QDialog):
    """Dialog for configuring analysis settings"""
    
    def __init__(self, current_settings: Dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analysis Settings")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Quality threshold
        quality_group = QGroupBox("Quality Filtering")
        quality_layout = QVBoxLayout()
        
        self.enable_quality_filter = QCheckBox("Enable quality-based filtering")
        self.enable_quality_filter.setChecked(current_settings.get('enable_quality_filter', False))
        quality_layout.addWidget(self.enable_quality_filter)
        
        threshold_layout = QHBoxLayout()
        threshold_layout.addWidget(QLabel("Minimum quality score:"))
        self.quality_threshold = QSpinBox()
        self.quality_threshold.setRange(0, 100)
        self.quality_threshold.setValue(current_settings.get('quality_threshold', 50))
        threshold_layout.addWidget(self.quality_threshold)
        quality_layout.addLayout(threshold_layout)
        
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)
        
        # Face detection
        face_group = QGroupBox("Face Detection")
        face_layout = QVBoxLayout()
        
        self.enable_face_detection = QCheckBox("Enable face detection (slower)")
        self.enable_face_detection.setChecked(current_settings.get('enable_face_detection', True))
        face_layout.addWidget(self.enable_face_detection)
        
        self.prioritize_faces = QCheckBox("Prioritize images with faces")
        self.prioritize_faces.setChecked(current_settings.get('prioritize_faces', False))
        face_layout.addWidget(self.prioritize_faces)
        
        face_group.setLayout(face_layout)
        layout.addWidget(face_group)
        
        # Duplicate detection
        dup_group = QGroupBox("Duplicate Detection")
        dup_layout = QVBoxLayout()
        
        sensitivity_layout = QHBoxLayout()
        sensitivity_layout.addWidget(QLabel("Similarity threshold:"))
        self.similarity_threshold = QSpinBox()
        self.similarity_threshold.setRange(0, 20)
        self.similarity_threshold.setValue(current_settings.get('similarity_threshold', 5))
        self.similarity_threshold.setToolTip("Lower = more strict (0-20)")
        sensitivity_layout.addWidget(self.similarity_threshold)
        dup_layout.addLayout(sensitivity_layout)
        
        dup_group.setLayout(dup_layout)
        layout.addWidget(dup_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
    
    def get_settings(self) -> Dict:
        """Get current settings from dialog"""
        return {
            'enable_quality_filter': self.enable_quality_filter.isChecked(),
            'quality_threshold': self.quality_threshold.value(),
            'enable_face_detection': self.enable_face_detection.isChecked(),
            'prioritize_faces': self.prioritize_faces.isChecked(),
            'similarity_threshold': self.similarity_threshold.value()
        }


class ImageAnalysisManager:
    """Manager class to integrate analysis into main application"""
    
    def __init__(self, parent_app):
        """
        Initialize the analysis manager
        Args:
            parent_app: Reference to main PxgateApp instance
        """
        self.app = parent_app
        self.analysis_results = {}  # {path: result_dict}
        self.worker = None
        self.worker_thread = None
        self.progress_dialog = None
        self.duplicate_groups = []
        self.duplicate_viewer_dialog = None
        
        # Default settings
        self.settings = {
            'enable_quality_filter': False,
            'quality_threshold': 50,
            'enable_face_detection': True,
            'prioritize_faces': False,
            'similarity_threshold': 5,
            'auto_analyze_on_load': False  # Changed to False - users click button to analyze
        }
        
        logging.info("ImageAnalysisManager initialized")
    
    def is_available(self) -> bool:
        """Check if analysis features are available"""
        return ANALYSIS_AVAILABLE
    
    def start_analysis(self, image_paths: List[str], show_progress: bool = True):
        """Start analyzing images in background"""
        if not ANALYSIS_AVAILABLE:
            logging.warning("Analysis not available - missing dependencies")
            return
        
        if not image_paths:
            return
        
        # Stop any existing analysis
        self.stop_analysis()
        
        # Create worker and thread
        self.worker = AnalysisWorker(
            image_paths,
            include_faces=self.settings['enable_face_detection'],
            similarity_threshold=self.settings.get('similarity_threshold', 5)
        )
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals with Qt.QueuedConnection to ensure async processing
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.on_progress, Qt.QueuedConnection)
        self.worker.image_analyzed.connect(self.on_image_analyzed, Qt.QueuedConnection)
        self.worker.batch_complete.connect(self.on_batch_complete, Qt.QueuedConnection)
        self.worker.error.connect(self.on_error, Qt.QueuedConnection)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        
        # Show progress dialog
        if show_progress:
            self.progress_dialog = AnalysisProgressDialog(len(image_paths), self.app)
            self.progress_dialog.rejected.connect(self.stop_analysis)
            self.progress_dialog.show()
        
        # Start analysis
        self.worker_thread.start()
        logging.info(f"Started analysis of {len(image_paths)} images")
    
    def stop_analysis(self):
        """Stop ongoing analysis"""
        if self.worker:
            self.worker.stop()
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.quit()
            self.worker_thread.wait(3000)  # Wait up to 3 seconds
        
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
    
    def on_progress(self, current: int, total: int):
        """Handle progress update"""
        if self.progress_dialog:
            self.progress_dialog.update_progress(current, total)
    
    def on_image_analyzed(self, path: str, result: Dict):
        """Handle single image analysis complete"""
        self.analysis_results[path] = result
        
        # Update UI if this is the current image
        if hasattr(self.app, 'get_current_image_path'):
            current_path = self.app.get_current_image_path()
            if current_path == path:
                self.update_current_image_info(result)
    
    def on_batch_complete(self, results: Dict, duplicate_groups: List[List[str]] = None):
        """Handle batch analysis complete"""
        logging.info(f"on_batch_complete called with {len(results)} results")
        try:
            self.duplicate_groups = duplicate_groups or []
            logging.info(f"Duplicate groups count: {len(self.duplicate_groups)}")
        except Exception:
            self.duplicate_groups = []
        
        try:
            # Close dialog asynchronously to avoid re-entrancy/crash
            logging.info("About to close progress dialog (async)...")
            if self.progress_dialog:
                dlg = self.progress_dialog
                self.progress_dialog = None  # detach reference first
                from PySide6.QtCore import QTimer
                QTimer.singleShot(0, lambda d=dlg: self._async_close_dialog(d))
                logging.info("Progress dialog scheduled for async close")
            else:
                logging.info("No progress dialog to close")
            
            # Detach engine reference to allow GC; avoid explicit shutdown here
            logging.info("Detaching engine reference (no explicit shutdown)")
            if self.worker and hasattr(self.worker, 'engine'):
                try:
                    self.worker.engine = None
                except Exception:
                    pass
            
            # Clean up thread
            logging.info("About to quit worker thread...")
            if self.worker_thread:
                self.worker_thread.quit()
                logging.info("Worker thread quit signal sent")
            else:
                logging.info("No worker thread to quit")
            
            # Process results immediately (we're already on main thread via QueuedConnection)
            logging.info("About to call _finish_analysis...")
            self._finish_analysis(results)
            logging.info("_finish_analysis completed")
            try:
                from PySide6.QtCore import QTimer
                QTimer.singleShot(0, self._maybe_show_duplicates)
            except Exception as e:
                logging.error(f"Failed to schedule duplicate viewer: {e}")
            
        except Exception as e:
            logging.error(f"CRITICAL ERROR in on_batch_complete: {e}", exc_info=True)
    
    def _finish_analysis(self, results: Dict):
        """Finish analysis processing (called after dialog closes)"""
        try:
            logging.info("_finish_analysis: Updating analysis results...")
            self.analysis_results.update(results)
            
            logging.info(f"Analysis complete: {len(results)} images analyzed")
            
            # Avoid showing message boxes to prevent UI reentrancy/crashes
            # Update current image display
            logging.info("_finish_analysis: About to update current image info...")
            if hasattr(self.app, 'get_current_image_path'):
                current_path = self.app.get_current_image_path()
                if current_path and current_path in self.analysis_results:
                    try:
                        self.update_current_image_info(self.analysis_results[current_path])
                        logging.info("Current image info updated")
                    except Exception as e:
                        logging.error(f"Error updating current image info: {e}", exc_info=True)
            
            logging.info("_finish_analysis: COMPLETED SUCCESSFULLY")
        except Exception as e:
            logging.error(f"CRITICAL ERROR in _finish_analysis: {e}", exc_info=True)

    def _async_close_dialog(self, dlg: QDialog):
        """Safely close and delete the progress dialog on the UI event loop."""
        try:
            if dlg is None or not isValid(dlg):
                logging.info("Progress dialog already invalid; skip close")
                return
            try:
                dlg.rejected.disconnect(self.stop_analysis)
            except Exception:
                pass
            try:
                if hasattr(dlg, 'cancel_button'):
                    dlg.cancel_button.setEnabled(False)
            except Exception:
                pass
            try:
                dlg.hide()
            except Exception:
                pass
            try:
                dlg.deleteLater()
            except Exception:
                pass
            logging.info("Progress dialog closed asynchronously")
        except Exception as e:
            logging.error(f"Error during async dialog close: {e}")

    def _maybe_show_duplicates(self):
        try:
            logging.info("_maybe_show_duplicates called")
            if not getattr(self, 'duplicate_groups', None):
                logging.info("No duplicate groups to show")
                return
            if self.duplicate_viewer_dialog and self.duplicate_viewer_dialog.isVisible():
                return
            from PySide6.QtCore import QTimer
            def _show():
                try:
                    self.duplicate_viewer_dialog = DuplicateViewerDialog(self.duplicate_groups, parent=self.app)
                    self.duplicate_viewer_dialog.setModal(False)
                    try:
                        self.duplicate_viewer_dialog.raise_()
                        self.duplicate_viewer_dialog.activateWindow()
                    except Exception:
                        pass
                    self.duplicate_viewer_dialog.show()
                    logging.info(f"Duplicate viewer opened with {len(self.duplicate_groups)} groups")
                except Exception as e:
                    logging.error(f"Error while showing duplicate viewer: {e}", exc_info=True)
            QTimer.singleShot(50, _show)
        except Exception as e:
            logging.error(f"Error opening duplicate viewer: {e}", exc_info=True)
    
    def on_error(self, error_msg: str):
        """Handle analysis error"""
        logging.error(f"Analysis error: {error_msg}")
        if self.progress_dialog:
            self.progress_dialog.close()
    
    def update_current_image_info(self, result: Dict):
        """Update the file info display with analysis results"""
        if not result.get('analyzed'):
            return
        
        # This will be called to update the UI with analysis data
        # The actual UI update will be implemented in the main app
        if hasattr(self.app, 'update_analysis_display'):
            self.app.update_analysis_display(result)
    
    def get_analysis(self, image_path: str) -> Optional[Dict]:
        """Get analysis result for an image"""
        return self.analysis_results.get(image_path)
    
    def show_duplicates_dialog(self):
        """Show dialog with duplicate images"""
        if not self.worker or not hasattr(self.worker, 'engine') or not self.worker.engine:
            QMessageBox.information(
                self.app,
                "No Analysis",
                "Please analyze images first before checking for duplicates."
            )
            return
        
        duplicate_groups = self.worker.engine.get_duplicate_groups()
        if not duplicate_groups:
            QMessageBox.information(
                self.app,
                "No Duplicates",
                "No duplicate or similar images found."
            )
            return
        
        dialog = DuplicateViewerDialog(duplicate_groups, self.app)
        dialog.exec()
    
    def show_settings_dialog(self):
        """Show analysis settings dialog"""
        dialog = AnalysisSettingsDialog(self.settings, self.app)
        if dialog.exec():
            self.settings = dialog.get_settings()
            logging.info(f"Analysis settings updated: {self.settings}")
    
    def get_filtered_image_list(self, image_paths: List[str]) -> List[str]:
        """Filter images based on quality threshold"""
        if not self.settings['enable_quality_filter']:
            return image_paths
        
        threshold = self.settings['quality_threshold']
        filtered = []
        
        for path in image_paths:
            result = self.analysis_results.get(path)
            if result and result.get('analyzed'):
                if result.get('quality_score', 0) >= threshold:
                    filtered.append(path)
            else:
                # Include unanalyzed images
                filtered.append(path)
        
        return filtered
    
    def get_sorted_by_quality(self, image_paths: List[str], reverse: bool = True) -> List[str]:
        """Sort images by quality score"""
        def get_score(path):
            result = self.analysis_results.get(path)
            if result and result.get('analyzed'):
                return result.get('quality_score', 0)
            return 0
        
        return sorted(image_paths, key=get_score, reverse=reverse)
    
    def clear_results(self):
        """Clear all analysis results"""
        self.analysis_results.clear()
        logging.info("Analysis results cleared")
