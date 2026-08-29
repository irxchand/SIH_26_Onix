import cv2
import numpy as np

def get_lung_contours_svg(image_path: str, scale_x: float = 1.0, scale_y: float = 1.0) -> dict:
    """
    Extracts simulated lung contours using OpenCV thresholding 
    and returns them as SVG path strings.
    """
    try:
        # Read grayscale
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")

        # Resize to standard width for consistent processing
        target_w = 200
        h, w = img.shape
        target_h = int(h * (target_w / w))
        img_small = cv2.resize(img, (target_w, target_h))

        # Otsu thresholding
        blur = cv2.GaussianBlur(img_small, (5,5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Clear borders to prevent edge contours
        thresh[0:5, :] = 0
        thresh[-5:, :] = 0
        thresh[:, 0:5] = 0
        thresh[:, -5:] = 0

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Take top 2 largest contours (lungs)
        top_2 = contours[:2]
        
        # Determine left and right based on centroid X
        left_lung = None
        right_lung = None
        
        if len(top_2) == 2:
            M0 = cv2.moments(top_2[0])
            M1 = cv2.moments(top_2[1])
            cx0 = int(M0['m10']/M0['m00']) if M0['m00'] != 0 else 0
            cx1 = int(M1['m10']/M1['m00']) if M1['m00'] != 0 else 0
            
            if cx0 < cx1:
                # Patient's right is on the left side of image (radiological convention)
                right_lung = top_2[0] 
                left_lung = top_2[1]
            else:
                right_lung = top_2[1]
                left_lung = top_2[0]
        elif len(top_2) == 1:
            left_lung = top_2[0]
            right_lung = top_2[0] # Fallback
            
        def contour_to_svg(cnt):
            if cnt is None or len(cnt) == 0:
                return ""
            # Downsample contour for cleaner SVG
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            
            path = []
            for i, pt in enumerate(approx):
                # Scale back to percentage 0-100 to map onto the Next.js SVG
                x_pct = (pt[0][0] / target_w) * 100 * scale_x
                y_pct = (pt[0][1] / target_h) * 100 * scale_y
                
                # Round for cleaner strings
                x_pct = round(x_pct, 2)
                y_pct = round(y_pct, 2)

                if i == 0:
                    path.append(f"M {x_pct} {y_pct}")
                else:
                    path.append(f"L {x_pct} {y_pct}")
            path.append("Z")
            return " ".join(path)

        return {
            "leftLung": contour_to_svg(left_lung),
            "rightLung": contour_to_svg(right_lung)
        }
    except Exception as e:
        print(f"Segmentation Error: {e}")
        # Fallback empty paths
        return {"leftLung": "", "rightLung": ""}

import os

def get_montgomery_mask_contours(study_id: str) -> dict:
    """Reads manual mask images from Montgomery dataset and returns SVG contours."""
    left_path = f"data/datasets/montgomery/MontgomerySet/ManualMask/leftMask/{study_id}.png"
    right_path = f"data/datasets/montgomery/MontgomerySet/ManualMask/rightMask/{study_id}.png"
    
    if not os.path.exists(left_path) or not os.path.exists(right_path):
        return None
        
    left_img = cv2.imread(left_path, cv2.IMREAD_GRAYSCALE)
    right_img = cv2.imread(right_path, cv2.IMREAD_GRAYSCALE)
    
    if left_img is None or right_img is None:
        return None
        
    # Find contours on masks (which are binary)
    left_contours, _ = cv2.findContours(left_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    right_contours, _ = cv2.findContours(right_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    left_cnt = sorted(left_contours, key=cv2.contourArea, reverse=True)[0] if left_contours else None
    right_cnt = sorted(right_contours, key=cv2.contourArea, reverse=True)[0] if right_contours else None
    
    h, w = left_img.shape
    
    def mask_contour_to_svg(cnt):
        if cnt is None or len(cnt) == 0:
            return ""
        # Downsample slightly
        epsilon = 0.005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        path = []
        for i, pt in enumerate(approx):
            x_pct = (pt[0][0] / w) * 100
            y_pct = (pt[0][1] / h) * 100
            
            x_pct = round(x_pct, 2)
            y_pct = round(y_pct, 2)
            
            if i == 0:
                path.append(f"M {x_pct} {y_pct}")
            else:
                path.append(f"L {x_pct} {y_pct}")
        path.append("Z")
        return " ".join(path)
        
    # In Montgomery, leftMask file is the patient's left lung (right side of image)
    # rightMask file is the patient's right lung (left side of image)
    return {
        "leftLung": mask_contour_to_svg(left_cnt),
        "rightLung": mask_contour_to_svg(right_cnt)
    }
