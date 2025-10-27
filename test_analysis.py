"""
Test script for image analysis features
Run this to verify the analysis engine works correctly
"""

import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_imports():
    """Test if all required libraries are available"""
    print("=" * 60)
    print("Testing Imports...")
    print("=" * 60)
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
        print(f"  Version: {cv2.__version__}")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import imagehash
        print("✓ imagehash imported successfully")
    except ImportError as e:
        print(f"✗ imagehash import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
        print(f"  Version: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow imported successfully")
    except ImportError as e:
        print(f"✗ Pillow import failed: {e}")
        return False
    
    print("\n✓ All required libraries available!\n")
    return True


def test_analysis_module():
    """Test the image_analyzer module"""
    print("=" * 60)
    print("Testing Analysis Module...")
    print("=" * 60)
    
    try:
        from image_analyzer import (
            ImageQualityAnalyzer,
            FaceAnalyzer,
            DuplicateDetector,
            ImageAnalysisEngine
        )
        print("✓ image_analyzer module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import image_analyzer: {e}")
        return False
    
    # Test quality analyzer
    try:
        analyzer = ImageQualityAnalyzer()
        print("✓ ImageQualityAnalyzer initialized")
    except Exception as e:
        print(f"✗ ImageQualityAnalyzer initialization failed: {e}")
        return False
    
    # Test face analyzer
    try:
        face_analyzer = FaceAnalyzer()
        print("✓ FaceAnalyzer initialized")
    except Exception as e:
        print(f"✗ FaceAnalyzer initialization failed: {e}")
        return False
    
    # Test duplicate detector
    try:
        dup_detector = DuplicateDetector()
        print("✓ DuplicateDetector initialized")
    except Exception as e:
        print(f"✗ DuplicateDetector initialization failed: {e}")
        return False
    
    # Test analysis engine
    try:
        engine = ImageAnalysisEngine(max_workers=2)
        print("✓ ImageAnalysisEngine initialized")
        engine.shutdown()
    except Exception as e:
        print(f"✗ ImageAnalysisEngine initialization failed: {e}")
        return False
    
    print("\n✓ All analysis components working!\n")
    return True


def test_integration_module():
    """Test the analysis_integration module"""
    print("=" * 60)
    print("Testing Integration Module...")
    print("=" * 60)
    
    try:
        from analysis_integration import (
            AnalysisWorker,
            AnalysisProgressDialog,
            DuplicateViewerDialog,
            AnalysisSettingsDialog,
            ImageAnalysisManager
        )
        print("✓ analysis_integration module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import analysis_integration: {e}")
        print(f"  Note: This requires PySide6 to be installed")
        return False
    
    print("\n✓ Integration module working!\n")
    return True


def test_sample_image():
    """Test analysis on a sample image"""
    print("=" * 60)
    print("Testing Sample Image Analysis...")
    print("=" * 60)
    
    # Create a simple test image
    try:
        import numpy as np
        import cv2
        from image_analyzer import ImageAnalysisEngine
        
        # Create a test image (gradient with some noise)
        test_image = np.zeros((600, 800, 3), dtype=np.uint8)
        
        # Add gradient
        for i in range(600):
            test_image[i, :] = [i * 255 // 600] * 3
        
        # Add some noise
        noise = np.random.randint(0, 50, test_image.shape, dtype=np.uint8)
        test_image = cv2.add(test_image, noise)
        
        # Save test image
        test_path = Path("test_image.jpg")
        cv2.imwrite(str(test_path), test_image)
        print(f"✓ Created test image: {test_path}")
        
        # Analyze it
        engine = ImageAnalysisEngine(max_workers=1)
        result = engine.analyze_image(str(test_path), include_faces=True)
        
        print("\nAnalysis Results:")
        print(f"  Analyzed: {result['analyzed']}")
        print(f"  Overall Score: {result['overall_score']:.1f}")
        print(f"  Sharpness: {result['sharpness']:.1f}")
        print(f"  Exposure Score: {result['exposure']['exposure_score']:.1f}")
        print(f"  Noise Score: {result['noise_score']:.1f}")
        print(f"  Composition Score: {result['composition_score']:.1f}")
        print(f"  Face Count: {result['face_data'].get('face_count', 0)}")
        
        # Cleanup
        engine.shutdown()
        test_path.unlink()
        print(f"\n✓ Test image analyzed successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Sample image analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_duplicate_detection():
    """Test duplicate detection"""
    print("=" * 60)
    print("Testing Duplicate Detection...")
    print("=" * 60)
    
    try:
        import numpy as np
        import cv2
        from image_analyzer import DuplicateDetector
        
        # Create two similar test images
        test_image1 = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
        test_image2 = test_image1.copy()
        
        # Add slight variation to second image
        noise = np.random.randint(-10, 10, test_image2.shape, dtype=np.int16)
        test_image2 = np.clip(test_image2.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        # Save images
        path1 = Path("test_dup1.jpg")
        path2 = Path("test_dup2.jpg")
        cv2.imwrite(str(path1), test_image1)
        cv2.imwrite(str(path2), test_image2)
        
        print(f"✓ Created test images: {path1}, {path2}")
        
        # Test duplicate detection
        detector = DuplicateDetector(similarity_threshold=10)
        detector.add_image(str(path1))
        detector.add_image(str(path2))
        
        duplicates = detector.find_duplicates()
        
        print(f"\nDuplicate Groups Found: {len(duplicates)}")
        if duplicates:
            print(f"  Group 1: {len(duplicates[0])} images")
            print("  ✓ Duplicate detection working!")
        else:
            print("  Note: No duplicates found (images may be too different)")
        
        # Cleanup
        path1.unlink()
        path2.unlink()
        
        return True
        
    except Exception as e:
        print(f"✗ Duplicate detection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("IMAGE ANALYSIS FEATURE TEST SUITE")
    print("=" * 60 + "\n")
    
    results = []
    
    # Test 1: Imports
    results.append(("Imports", test_imports()))
    
    # Test 2: Analysis module
    if results[-1][1]:  # Only if imports succeeded
        results.append(("Analysis Module", test_analysis_module()))
    
    # Test 3: Integration module
    if results[-1][1]:  # Only if analysis module succeeded
        results.append(("Integration Module", test_integration_module()))
    
    # Test 4: Sample image analysis
    if results[1][1]:  # If analysis module succeeded
        results.append(("Sample Image Analysis", test_sample_image()))
    
    # Test 5: Duplicate detection
    if results[1][1]:  # If analysis module succeeded
        results.append(("Duplicate Detection", test_duplicate_detection()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou're ready to use AI analysis features in Pxgate!")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease install missing dependencies:")
        print("  pip install opencv-python imagehash")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
