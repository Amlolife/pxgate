"""
Image Analysis Module for Pxgate
Provides offline AI-powered image quality analysis, face detection, and duplicate detection
"""

import cv2
import numpy as np
from pathlib import Path
import logging
from PIL import Image
import imagehash
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Tuple, Optional
import threading
import os
import sys
import json


class ImageQualityAnalyzer:
    """Analyzes image quality using various metrics"""
    
    @staticmethod
    def calculate_sharpness(image_array: np.ndarray) -> float:
        """
        Calculate image sharpness using Laplacian variance
        Higher values = sharper image
        Returns: 0-100 score
        """
        try:
            # Convert to grayscale if needed
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = image_array
            
            # Calculate Laplacian variance
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Normalize to 0-100 scale (empirically determined thresholds)
            # Very sharp images: >1000, Blurry: <100
            score = min(100, (laplacian_var / 10))
            return float(score)
        except Exception as e:
            logging.error(f"Sharpness calculation error: {e}")
            return 0.0

    @staticmethod
    def calculate_roi_sharpness(gray: np.ndarray) -> float:
        """
        Calculate sharpness on a grayscale ROI using Laplacian variance.
        Returns 0-100 score.
        """
        try:
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            score = min(100, (laplacian_var / 10))
            return float(score)
        except Exception:
            return 0.0
    
    @staticmethod
    def calculate_exposure(image_array: np.ndarray) -> Dict[str, float]:
        """
        Analyze exposure quality
        Returns: dict with brightness, contrast, and exposure_score (0-100)
        """
        try:
            # Convert to grayscale
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = image_array
            
            # Calculate brightness (mean)
            brightness = float(np.mean(gray))
            
            # Calculate contrast (std deviation)
            contrast = float(np.std(gray))
            
            # Calculate histogram
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten() / hist.sum()
            
            # Check for clipping (overexposure/underexposure)
            underexposed = np.sum(hist[:10])  # Very dark pixels
            overexposed = np.sum(hist[-10:])  # Very bright pixels
            clipping_penalty = (underexposed + overexposed) * 100
            
            # Ideal brightness is around 128 (middle gray)
            brightness_score = 100 - abs(brightness - 128) / 1.28
            
            # Good contrast is around 50-80
            contrast_score = min(100, contrast * 1.5)
            
            # Combined exposure score
            exposure_score = (brightness_score * 0.4 + contrast_score * 0.4 + 
                            (100 - clipping_penalty) * 0.2)
            
            return {
                'brightness': brightness,
                'contrast': contrast,
                'exposure_score': max(0, min(100, exposure_score)),
                'underexposed': underexposed > 0.1,
                'overexposed': overexposed > 0.1
            }
        except Exception as e:
            logging.error(f"Exposure calculation error: {e}")
            return {'brightness': 0, 'contrast': 0, 'exposure_score': 0, 
                   'underexposed': False, 'overexposed': False}
    
    @staticmethod
    def calculate_noise(image_array: np.ndarray) -> float:
        """
        Estimate image noise level
        Returns: 0-100 score (higher = less noise)
        """
        try:
            # Convert to grayscale
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = image_array
            
            # Resize for faster processing
            h, w = gray.shape
            if h > 1000 or w > 1000:
                scale = 1000 / max(h, w)
                gray = cv2.resize(gray, None, fx=scale, fy=scale)
            
            # Estimate noise using high-frequency content
            # Apply Gaussian blur and subtract from original
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            noise = cv2.absdiff(gray, blurred)
            noise_level = float(np.mean(noise))
            
            # Normalize: low noise = high score
            # Typical noise levels: 0-20 (good to noisy)
            noise_score = max(0, 100 - (noise_level * 5))
            
            return float(noise_score)
        except Exception as e:
            logging.error(f"Noise calculation error: {e}")
            return 0.0
    
    @staticmethod
    def calculate_composition_score(image_array: np.ndarray) -> float:
        """
        Basic composition analysis using rule of thirds
        Returns: 0-100 score
        """
        try:
            # Convert to grayscale
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = image_array
            
            h, w = gray.shape
            
            # Divide into 9 regions (rule of thirds)
            third_h, third_w = h // 3, w // 3
            
            # Calculate interest points (edges)
            edges = cv2.Canny(gray, 50, 150)
            
            # Check edge density in power points (intersections of thirds)
            power_points = [
                (third_w, third_h), (2*third_w, third_h),
                (third_w, 2*third_h), (2*third_w, 2*third_h)
            ]
            
            region_size = min(third_h, third_w) // 4
            interest_score = 0
            
            for px, py in power_points:
                y1, y2 = max(0, py - region_size), min(h, py + region_size)
                x1, x2 = max(0, px - region_size), min(w, px + region_size)
                region = edges[y1:y2, x1:x2]
                interest_score += np.sum(region) / 255
            
            # Normalize
            max_possible = region_size * region_size * 4
            composition_score = (interest_score / max_possible) * 100
            
            return min(100, float(composition_score) * 2)
        except Exception as e:
            logging.error(f"Composition calculation error: {e}")
            return 50.0  # Neutral score on error


class FaceAnalyzer:
    """Detects and analyzes faces in images"""
    
    def __init__(self):
        """Initialize face detection models"""
        self.face_cascade = None
        self.eye_cascade = None
        self.smile_cascade = None
        self._load_cascades()
    
    def _load_cascades(self):
        """Load Haar Cascade classifiers"""
        try:
            # Try to load pre-trained cascades from OpenCV
            cascade_path = cv2.data.haarcascades
            
            self.face_cascade = cv2.CascadeClassifier(
                cascade_path + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cascade_path + 'haarcascade_eye.xml'
            )
            self.smile_cascade = cv2.CascadeClassifier(
                cascade_path + 'haarcascade_smile.xml'
            )
            
            logging.info("Face detection models loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load face detection models: {e}")
    
    def detect_faces(self, image_array: np.ndarray) -> Dict:
        """
        Detect faces and analyze them
        Returns: dict with face count, eye detection, smile detection
        """
        result = {
            'face_count': 0,
            'faces': [],
            'has_eyes': False,
            'has_smile': False,
            'eyes_open': False,
            'emotion': 'none',
            'face_quality_score': 0
        }
        
        if self.face_cascade is None:
            return result
        
        try:
            # Convert to grayscale
            if len(image_array.shape) == 3:
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = image_array
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            result['face_count'] = len(faces)
            
            if len(faces) == 0:
                return result
            
            # Analyze each face
            eyes_detected = 0
            smiles_detected = 0
            
            for (x, y, w, h) in faces:
                face_roi_gray = gray[y:y+h, x:x+w]
                
                # Detect eyes in face region
                if self.eye_cascade is not None:
                    eyes = self.eye_cascade.detectMultiScale(face_roi_gray)
                    if len(eyes) >= 2:  # At least 2 eyes
                        eyes_detected += 1
                
                # Detect smile in face region
                if self.smile_cascade is not None:
                    smiles = self.smile_cascade.detectMultiScale(
                        face_roi_gray, scaleFactor=1.8, minNeighbors=20
                    )
                    if len(smiles) > 0:
                        smiles_detected += 1
                
                # Calculate face size relative to image
                face_size_ratio = (w * h) / (gray.shape[0] * gray.shape[1])

                # Face ROI sharpness
                face_sharpness = ImageQualityAnalyzer.calculate_roi_sharpness(face_roi_gray)
                
                result['faces'].append({
                    'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h),
                    'size_ratio': float(face_size_ratio),
                    'has_eyes': len(eyes) >= 2 if self.eye_cascade else False,
                    'has_smile': len(smiles) > 0 if self.smile_cascade else False,
                    'eyes_open': len(eyes) >= 2 if self.eye_cascade else False,
                    'face_sharpness': float(face_sharpness)
                })
            
            result['has_eyes'] = eyes_detected > 0
            result['has_smile'] = smiles_detected > 0
            result['eyes_open'] = eyes_detected > 0
            result['emotion'] = 'happy' if smiles_detected > 0 else 'neutral'
            
            # Calculate face quality score
            # Factors: face count (1-3 ideal), eyes detected, proper size
            face_count_score = 100 if 1 <= len(faces) <= 3 else max(0, 100 - abs(len(faces) - 2) * 20)
            eyes_score = (eyes_detected / len(faces)) * 100 if len(faces) > 0 else 0
            # Face sharpness average
            avg_sharp = 0.0
            if len(result['faces']) > 0:
                avg_sharp = float(np.mean([f['face_sharpness'] for f in result['faces']]))
            result['face_quality_score'] = (
                face_count_score * 0.4 + eyes_score * 0.3 + avg_sharp * 0.3
            )
            
            return result
            
        except Exception as e:
            logging.error(f"Face detection error: {e}")
            return result


class DuplicateDetector:
    """Detects duplicate and similar images using perceptual hashing"""
    
    def __init__(self, similarity_threshold: int = 5):
        """
        Initialize duplicate detector
        Args:
            similarity_threshold: Hash difference threshold (0-64, lower = more similar)
        """
        self.similarity_threshold = similarity_threshold
        self.image_hashes = {}  # {file_path: hash}
        self.hash_lock = threading.Lock()
    
    def calculate_hash(self, image_path: str) -> Optional[imagehash.ImageHash]:
        """Calculate perceptual hash for an image"""
        try:
            with Image.open(image_path) as img:
                # Use perceptual hash (pHash) for better duplicate detection
                phash = imagehash.phash(img, hash_size=8)
                return phash
        except Exception as e:
            logging.error(f"Hash calculation error for {image_path}: {e}")
            return None
    
    def add_image(self, image_path: str) -> bool:
        """Add an image to the hash database"""
        hash_value = self.calculate_hash(image_path)
        if hash_value:
            with self.hash_lock:
                self.image_hashes[image_path] = hash_value
            return True
        return False
    
    def find_duplicates(self) -> List[List[str]]:
        """
        Find groups of duplicate/similar images
        Returns: List of lists, each containing paths of similar images
        """
        duplicate_groups = []
        processed = set()
        
        with self.hash_lock:
            paths = list(self.image_hashes.keys())
        
        for i, path1 in enumerate(paths):
            if path1 in processed:
                continue
            
            group = [path1]
            hash1 = self.image_hashes[path1]
            
            for path2 in paths[i+1:]:
                if path2 in processed:
                    continue
                
                hash2 = self.image_hashes[path2]
                difference = hash1 - hash2
                
                if difference <= self.similarity_threshold:
                    group.append(path2)
                    processed.add(path2)
            
            if len(group) > 1:
                duplicate_groups.append(group)
                processed.add(path1)
        
        return duplicate_groups
    
    def find_similar_to(self, image_path: str, max_results: int = 10) -> List[Tuple[str, int]]:
        """
        Find images similar to the given image
        Returns: List of (path, similarity_score) tuples, sorted by similarity
        """
        if image_path not in self.image_hashes:
            return []
        
        target_hash = self.image_hashes[image_path]
        similarities = []
        
        with self.hash_lock:
            for path, hash_value in self.image_hashes.items():
                if path == image_path:
                    continue
                
                difference = target_hash - hash_value
                if difference <= self.similarity_threshold * 2:  # Broader search
                    similarity_score = 100 - (difference * 100 / 64)  # Convert to 0-100
                    similarities.append((path, int(similarity_score)))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:max_results]
    
    def clear(self):
        """Clear all stored hashes"""
        with self.hash_lock:
            self.image_hashes.clear()


class ImageAnalysisEngine:
    """Main engine that coordinates all analysis tasks"""
    
    def __init__(self, max_workers: int = 4, similarity_threshold: int = 5):
        """Initialize the analysis engine"""
        self.quality_analyzer = ImageQualityAnalyzer()
        self.face_analyzer = FaceAnalyzer()
        self.duplicate_detector = DuplicateDetector(similarity_threshold=similarity_threshold)
        self.executor = ThreadPoolExecutor(max_workers=max_workers, 
                                          thread_name_prefix="ImageAnalysis")
        self.analysis_cache = {}  # {file_path: analysis_result}
        self.cache_lock = threading.Lock()
        self.CACHE_VERSION = "1.0"
        self.cache_path = self._get_cache_path()
        self._load_cache()
        
        logging.info(f"ImageAnalysisEngine initialized with {max_workers} workers")
    
    def analyze_image(self, image_path: str, include_faces: bool = True) -> Dict:
        """
        Perform complete analysis on an image
        Returns: dict with all analysis results
        """
        # Check cache first (validate mtime and version)
        try:
            current_mtime = os.path.getmtime(image_path)
        except Exception:
            current_mtime = None
        with self.cache_lock:
            cached = self.analysis_cache.get(image_path)
            if cached and isinstance(cached, dict):
                if (
                    cached.get('_cache_version') == self.CACHE_VERSION and
                    cached.get('_mtime') == current_mtime
                ):
                    return cached
        
        result = {
            'path': image_path,
            'analyzed': False,
            'quality_score': 0,
            'sharpness': 0,
            'exposure': {},
            'noise_score': 0,
            'composition_score': 0,
            'face_data': {},
            'overall_score': 0
        }
        
        try:
            # Load image
            image_array = cv2.imread(image_path)
            if image_array is None:
                logging.warning(f"Could not load image: {image_path}")
                return result
            
            # Resize if too large (for performance)
            h, w = image_array.shape[:2]
            if h > 2000 or w > 2000:
                scale = 2000 / max(h, w)
                image_array = cv2.resize(image_array, None, fx=scale, fy=scale)
            
            # Quality analysis
            result['sharpness'] = self.quality_analyzer.calculate_sharpness(image_array)
            result['exposure'] = self.quality_analyzer.calculate_exposure(image_array)
            result['noise_score'] = self.quality_analyzer.calculate_noise(image_array)
            result['composition_score'] = self.quality_analyzer.calculate_composition_score(image_array)
            
            # Face detection (optional, can be slow)
            if include_faces:
                result['face_data'] = self.face_analyzer.detect_faces(image_array)
            
            # Calculate overall quality score with refined weights
            quality_score = (
                result['sharpness'] * 0.40 +
                result['exposure'].get('exposure_score', 0) * 0.25 +
                result['noise_score'] * 0.15 +
                result['composition_score'] * 0.10
            )
            # Face-weighted bonus (presence, eyes open, face sharpness)
            if include_faces and result['face_data'].get('face_count', 0) > 0:
                face_quality = result['face_data'].get('face_quality_score', 0)
                if result['face_data'].get('eyes_open'):
                    face_quality = min(100, face_quality + 10)
                quality_score = min(100, quality_score + face_quality * 0.10)
            
            result['quality_score'] = round(quality_score, 1)
            result['overall_score'] = round(quality_score, 1)
            result['analyzed'] = True
            
            # Add to duplicate detector
            self.duplicate_detector.add_image(image_path)
            
            # Cache result
            with self.cache_lock:
                try:
                    result_copy = dict(result)
                    result_copy['_mtime'] = current_mtime
                    result_copy['_cache_version'] = self.CACHE_VERSION
                    self.analysis_cache[image_path] = result_copy
                except Exception:
                    self.analysis_cache[image_path] = result
            # Persist cache
            try:
                self._save_cache()
            except Exception as e:
                logging.debug(f"Cache save skipped: {e}")
            
            return result
            
        except Exception as e:
            logging.error(f"Image analysis error for {image_path}: {e}")
            return result
    
    def analyze_batch(self, image_paths: List[str], 
                     progress_callback=None) -> Dict[str, Dict]:
        """
        Analyze multiple images in parallel
        Args:
            image_paths: List of image paths to analyze
            progress_callback: Optional callback(current, total) for progress
        Returns: dict mapping path to analysis result
        """
        results = {}
        total = len(image_paths)
        
        futures = []
        for path in image_paths:
            future = self.executor.submit(self.analyze_image, path)
            futures.append((path, future))
        
        for idx, (path, future) in enumerate(futures):
            try:
                result = future.result(timeout=30)  # 30 second timeout per image
                results[path] = result
                
                if progress_callback:
                    progress_callback(idx + 1, total)
                    
            except Exception as e:
                logging.error(f"Batch analysis error for {path}: {e}")
                results[path] = {'path': path, 'analyzed': False, 'error': str(e)}
        
        return results
    
    def get_duplicate_groups(self) -> List[List[str]]:
        """Get groups of duplicate/similar images"""
        return self.duplicate_detector.find_duplicates()
    
    def find_similar_images(self, image_path: str, max_results: int = 10) -> List[Tuple[str, int]]:
        """Find images similar to the given image"""
        return self.duplicate_detector.find_similar_to(image_path, max_results)
    
    def get_cached_analysis(self, image_path: str) -> Optional[Dict]:
        """Get cached analysis result if available"""
        with self.cache_lock:
            return self.analysis_cache.get(image_path)
    
    def clear_cache(self):
        """Clear all cached analysis results"""
        with self.cache_lock:
            self.analysis_cache.clear()
        self.duplicate_detector.clear()
        logging.info("Analysis cache cleared")
        try:
            if os.path.exists(self.cache_path):
                os.remove(self.cache_path)
        except Exception:
            pass
    
    def shutdown(self):
        """Shutdown the analysis engine"""
        self.executor.shutdown(wait=True)
        logging.info("ImageAnalysisEngine shutdown complete")

    # ---------------- Internal cache helpers ----------------
    def _get_cache_path(self) -> str:
        try:
            if getattr(sys, 'frozen', False):
                base_dir = os.path.dirname(sys.executable)
            else:
                base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        except Exception:
            base_dir = os.getcwd()
        return os.path.join(base_dir, 'analysis_cache.json')

    def _load_cache(self):
        try:
            if not os.path.exists(self.cache_path):
                return
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict) or data.get('version') != self.CACHE_VERSION:
                return
            entries = data.get('entries', {})
            if isinstance(entries, dict):
                with self.cache_lock:
                    self.analysis_cache.update(entries)
                logging.info(f"Loaded analysis cache: {len(entries)} entries")
        except Exception as e:
            logging.warning(f"Failed to load analysis cache: {e}")

    def _save_cache(self):
        try:
            with self.cache_lock:
                data = {
                    'version': self.CACHE_VERSION,
                    'entries': self.analysis_cache
                }
            tmp_path = self.cache_path + '.tmp'
            with open(tmp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
            os.replace(tmp_path, self.cache_path)
        except Exception as e:
            logging.debug(f"Failed to save analysis cache: {e}")


# Convenience function for quick analysis
def quick_analyze(image_path: str) -> Dict:
    """Quick analysis of a single image (no caching)"""
    engine = ImageAnalysisEngine(max_workers=1)
    result = engine.analyze_image(image_path)
    engine.shutdown()
    return result
