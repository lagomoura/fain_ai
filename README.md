# AR Catcher - Enhanced Gaming Experience

An augmented reality hand gesture game where players catch falling objects using their hands through a camera.

## 🎮 Enhanced Features

### **More Bombs & Challenge**
- **Increased bomb spawn rate**: Starts at 40% and increases to 70% over time
- **Multiple bomb types with unique sprites**:
  - **Regular Bomb** (`bomb.png`): -2 points, standard explosion
  - **Mega Bomb** (`bomb2.png`): -3 points, bigger explosion, slower movement
  - **Cluster Bomb** (`cluster.png`): -1 point, faster movement, smaller size

### **Power-Up System**
- **Shield Power-Up** (`shield.png`): Protects players from bombs for 8 seconds
- **Golden Fruit** (`goldFruit.png`): Rare item that gives 3x points and extends combo
- **Combo System**: Chain catches to build multipliers up to 5x

### **Visual Enhancements**
- **Glow Effects**: Special objects have distinctive glows
- **Explosion Particles**: Dynamic particle effects for different bomb types
- **Enhanced UI**: Power-up indicators, combo displays, and game time
- **Screen Flash**: Different colors for different bomb explosions

### **Gameplay Improvements**
- **Dynamic Difficulty**: Bomb spawn rate increases every 30 seconds
- **Faster Spawning**: Objects spawn every 0.8 seconds for more action
- **Higher Goal**: Win condition increased to 15 points for longer games
- **Pause Function**: Press 'P' to pause/resume the game

## 🎯 How to Play

1. **Setup**: Ensure your camera is working and positioned
2. **Controls**: 
   - Move your hands in front of the camera
   - Catch fruits for points
   - Avoid bombs (they reduce your score)
   - Collect power-ups for advantages
3. **Keys**:
   - `P`: Pause/Resume game
   - `Q`: Quit game

## 🚀 Getting Started

```bash
# Navigate to the project directory
cd fain_ai/ar_catcher

# Test sprite loading (optional but recommended)
python test_sprites.py

# Run the game
python game.py
```

## 🎨 Object Types

| Object | Points | Effect | Special | Sprite |
|--------|--------|--------|---------|---------|
| 🍎 Apple | +1 | Basic fruit | None | apple.png |
| 🍊 Orange | +1 | Basic fruit | Larger size | orange.png |
| ⚡ Pokeball | +2 | Bonus fruit | None | pokeball.png |
| 💣 Bomb | -2 | Explosion | Red flash | bomb.png |
| 💥 Mega Bomb | -3 | Big explosion | Red flash, screen shake | bomb2.png |
| 💥 Cluster Bomb | -1 | Fast explosion | Yellow flash | cluster.png |
| 🌟 Golden Fruit | +3 | Bonus points | Combo multiplier | goldFruit.png |
| 🛡️ Shield | 0 | Protection | Blocks bombs for 8s | shield.png |

## 🔧 Technical Features

- **Hand Tracking**: Uses MediaPipe for accurate hand detection
- **Real-time Processing**: Optimized for smooth gameplay
- **Particle System**: Dynamic explosion and effect particles
- **Power-up Management**: Timer-based power-up system
- **Difficulty Scaling**: Progressive challenge increase

## 📱 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- Pillow (PIL)
- NumPy
- Working webcam

## 🖼️ Required Sprite Files

The following sprite files must be present in the `assets/sprites/` directory:
- `apple.png` - Apple fruit sprite
- `orange.png` - Orange fruit sprite  
- `pokeball.png` - Pokeball bonus sprite
- `bomb.png` - Regular bomb sprite
- `bomb2.png` - Mega bomb sprite
- `cluster.png` - Cluster bomb sprite
- `goldFruit.png` - Golden fruit sprite
- `shield.png` - Shield power-up sprite

## 🎮 Tips for High Scores

1. **Build Combos**: Chain fruit catches to maximize points
2. **Use Shields Wisely**: Save shields for when many bombs are on screen
3. **Watch the Timer**: Bomb spawn rate increases over time
4. **Stay Active**: More movement = more chances to catch objects
5. **Coordinate**: In 2-player mode, communicate to avoid collisions

## 🚀 Future Enhancements

- Sound effects and music
- More power-up types
- Level-based progression
- Achievement system
- Multiplayer networking
- Customizable difficulty settings

---

**Enjoy the enhanced AR Catcher experience with more bombs, power-ups, and visual effects!** 🎉

