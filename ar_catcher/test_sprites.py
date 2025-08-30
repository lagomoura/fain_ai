#!/usr/bin/env python3
"""
Test script to verify all sprite files can be loaded correctly.
"""

def test_sprite_loading():
    """Test if all required sprites can be loaded."""
    try:
        print("Testing sprite loading...")
        
        from ar_catcher.sprite_manager import SpriteManager
        
        # List of required sprites
        required_sprites = [
            "apple",
            "orange", 
            "pokeball",
            "bomb",
            "bomb2",
            "cluster",
            "goldFruit",
            "shield"
        ]
        
        print(f"Found {len(required_sprites)} required sprites")
        
        # Test loading each sprite
        for sprite_name in required_sprites:
            try:
                sprite_bgr, alpha = SpriteManager.get(sprite_name, 50)  # 50x50 size
                print(f"✓ {sprite_name}.png loaded successfully")
            except Exception as e:
                print(f"❌ Failed to load {sprite_name}.png: {e}")
                return False
        
        print("\n🎉 All sprites loaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Sprite loading error: {e}")
        return False

def test_object_types():
    """Test if all object types can be created with correct sprites."""
    try:
        print("\nTesting object type creation...")
        
        from ar_catcher.objects import ObjectType, GameObject
        
        # Test creating each object type
        test_objects = [
            ObjectType.APPLE,
            ObjectType.ORANGE,
            ObjectType.POKEBALL,
            ObjectType.BOMB,
            ObjectType.MEGA_BOMB,
            ObjectType.CLUSTER_BOMB,
            ObjectType.GOLDEN_FRUIT,
            ObjectType.SHIELD
        ]
        
        for obj_type in test_objects:
            try:
                # Create a test object
                obj = GameObject(
                    x=100, y=100, radius=obj_type.value[1],
                    velocity_y=100, sprite_name=obj_type.value[0],
                    object_type=obj_type, score_value=obj_type.value[2]
                )
                print(f"✓ {obj_type.name} created with sprite: {obj.sprite_name}")
            except Exception as e:
                print(f"❌ Failed to create {obj_type.name}: {e}")
                return False
        
        print("\n🎉 All object types created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Object type creation error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 AR Catcher Sprite Test")
    print("=" * 40)
    
    # Test sprite loading
    sprites_ok = test_sprite_loading()
    
    if sprites_ok:
        # Test object creation
        objects_ok = test_object_types()
        
        if objects_ok:
            print("\n🎮 All sprite tests passed! The game is ready with new sprites.")
            print("\nNew sprite mapping:")
            print("  - Shield: shield.png")
            print("  - Golden Fruit: goldFruit.png") 
            print("  - Normal Bomb: bomb.png")
            print("  - Mega Bomb: bomb2.png")
            print("  - Cluster Bomb: cluster.png")
        else:
            print("\n⚠️  Object type tests failed. Check the errors above.")
    else:
        print("\n⚠️  Sprite loading tests failed. Check the errors above.")





