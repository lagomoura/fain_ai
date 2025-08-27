import cv2
import numpy as np
import random
from typing import List, Tuple, Dict, Any


class VisualEffects:
    """Enhanced visual effects for better gaming experience."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.screen_shake = 0.0
        self.screen_shake_intensity = 0.0
        self.color_grading = 1.0  # Normal color intensity
        
    def apply_screen_shake(self, frame: np.ndarray, intensity: float = 0.0) -> np.ndarray:
        """Apply screen shake effect for explosions and impacts."""
        if intensity <= 0:
            return frame
            
        # Calculate shake offset
        shake_x = random.uniform(-intensity, intensity)
        shake_y = random.uniform(-intensity, intensity)
        
        # Create transformation matrix
        M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
        
        # Apply shake transformation
        height, width = frame.shape[:2]
        frame = cv2.warpAffine(frame, M, (width, height))
        
        return frame
    
    def apply_explosion_flash(self, frame: np.ndarray, color: Tuple[int, int, int], intensity: float = 0.3) -> np.ndarray:
        """Apply explosion flash effect with color grading."""
        overlay = frame.copy()
        overlay[:] = color
        
        # Apply flash with intensity
        cv2.addWeighted(overlay, intensity, frame, 1 - intensity, 0, frame)
        
        # Add screen shake for explosion
        self.screen_shake_intensity = intensity * 15.0
        
        return frame
    
    def apply_danger_pulse(self, frame: np.ndarray, danger_level: float) -> np.ndarray:
        """Apply pulsing effect when many bombs are on screen."""
        if danger_level < 0.5:
            return frame
            
        # Calculate pulse intensity based on danger level
        pulse = np.sin(danger_level * 10) * 0.1 * danger_level
        
        # Apply subtle color shift
        overlay = frame.copy()
        overlay[:] = (0, 0, int(50 * pulse))  # Subtle blue tint
        
        cv2.addWeighted(overlay, abs(pulse), frame, 1 - abs(pulse), 0, frame)
        
        return frame
    
    def create_trail_effect(self, frame: np.ndarray, x: int, y: int, color: Tuple[int, int, int], 
                           trail_length: int = 5) -> np.ndarray:
        """Create motion trail effect for fast-moving objects."""
        overlay = frame.copy()
        
        for i in range(trail_length):
            alpha = (trail_length - i) / trail_length * 0.3
            trail_y = y + i * 3
            
            if 0 <= trail_y < self.height:
                cv2.circle(overlay, (x, int(trail_y)), 2, color, -1)
        
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        return frame
    
    def apply_vignette(self, frame: np.ndarray, intensity: float = 0.2) -> np.ndarray:
        """Apply subtle vignette effect for cinematic look."""
        height, width = frame.shape[:2]
        
        # Create vignette mask
        Y, X = np.ogrid[:height, :width]
        center_x, center_y = width // 2, height // 2
        radius = min(width, height) // 2
        
        # Calculate distance from center
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
        
        # Create smooth vignette
        vignette = 1 - (dist_from_center / radius) * intensity
        vignette = np.clip(vignette, 0, 1)
        
        # Apply vignette to all channels
        for c in range(3):
            frame[:, :, c] = frame[:, :, c] * vignette
            
        return frame
    
    def create_power_up_aura(self, frame: np.ndarray, x: int, y: int, radius: int, 
                            color: Tuple[int, int, int], intensity: float = 0.5) -> np.ndarray:
        """Create power-up aura effect around special objects."""
        overlay = frame.copy()
        
        # Create multiple concentric circles for aura effect
        for i in range(3):
            current_radius = radius + i * 5
            alpha = intensity * (1 - i / 3)
            
            cv2.circle(overlay, (x, y), current_radius, color, 2)
            
        cv2.addWeighted(overlay, intensity * 0.3, frame, 1 - intensity * 0.3, 0, frame)
        return frame
    
    def apply_motion_blur(self, frame: np.ndarray, blur_strength: float = 0.1) -> np.ndarray:
        """Apply subtle motion blur for dynamic movement."""
        if blur_strength <= 0:
            return frame
            
        # Create motion blur kernel
        kernel_size = max(3, int(blur_strength * 10))
        if kernel_size % 2 == 0:
            kernel_size += 1
            
        # Apply horizontal motion blur
        kernel = np.zeros((kernel_size, kernel_size))
        kernel[kernel_size // 2, :] = 1.0 / kernel_size
        
        blurred = cv2.filter2D(frame, -1, kernel)
        
        # Blend with original
        cv2.addWeighted(blurred, blur_strength, frame, 1 - blur_strength, 0, frame)
        
        return frame
    
    def create_score_flash(self, frame: np.ndarray, score: int, color: Tuple[int, int, int]) -> np.ndarray:
        """Create score flash effect when points are earned."""
        overlay = frame.copy()
        
        # Create score text overlay
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2.0
        thickness = 3
        
        text = f"+{score}"
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        
        # Center the text
        x = (self.width - text_size[0]) // 2
        y = (self.height + text_size[1]) // 2
        
        # Draw text with outline
        cv2.putText(overlay, text, (x, y), font, font_scale, (0, 0, 0), thickness + 2)
        cv2.putText(overlay, text, (x, y), font, font_scale, color, thickness)
        
        # Blend with original
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        return frame
    
    def update_effects(self, dt: float):
        """Update effect timers and states."""
        # Update screen shake
        if self.screen_shake_intensity > 0:
            self.screen_shake_intensity -= dt * 20.0  # Decay rate
            self.screen_shake_intensity = max(0, self.screen_shake_intensity)
            
        # Update color grading
        self.color_grading = 1.0 + np.sin(dt * 2) * 0.05  # Subtle breathing effect

