#!/usr/bin/env python
"""
Setup wizard for NewBot

Helps users configure NewBot for first-time use
"""

import os
import sys
from pathlib import Path
import shutil

def setup_wizard():
    """Interactive setup wizard"""
    
    print("=" * 70)
    print("NewBot Setup Wizard")
    print("=" * 70)
    print()
    print("This wizard will help you set up NewBot for first-time use.")
    print()
    
    # Step 1: Check Python version
    print("Step 1: Checking Python version...")
    python_version = sys.version_info
    if python_version < (3, 8):
        print(f"  ✗ Error: Python 3.8+ required (you have {python_version.major}.{python_version.minor})")
        sys.exit(1)
    print(f"  ✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    print()
    
    # Step 2: Create directories
    print("Step 2: Creating directories...")
    dirs_to_create = ['logs', 'backups']
    for dir_name in dirs_to_create:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"  ✓ Created {dir_name}/")
        else:
            print(f"  - {dir_name}/ already exists")
    print()
    
    # Step 3: Create config file
    print("Step 3: Creating configuration file...")
    config_file = Path('config.yaml')
    example_file = Path('config.yaml.example')
    
    if not example_file.exists():
        print(f"  ✗ Error: {example_file} not found!")
        print("  This file should be included with NewBot.")
        return
    
    if config_file.exists():
        print("  - config.yaml already exists")
        response = input("  Do you want to overwrite it? (y/N): ").strip().lower()
        if response != 'y':
            print("  Keeping existing config.yaml")
        else:
            shutil.copy(example_file, config_file)
            print("  ✓ Created config.yaml from template")
    else:
        shutil.copy(example_file, config_file)
        print("  ✓ Created config.yaml from template")
    print()
    
    # Step 4: Create .env file
    print("Step 4: Creating environment file...")
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if not env_example.exists():
        print(f"  ✗ Warning: {env_example} not found!")
        print("  You'll need to create .env manually with your credentials.")
    elif env_file.exists():
        print("  - .env already exists")
    else:
        shutil.copy(env_example, env_file)
        print("  ✓ Created .env from template")
        print("  ⚠ Remember to add your API keys to .env file!")
    print()
    
    # Step 5: Check dependencies
    print("Step 5: Checking dependencies...")
    print("  Attempting to import required packages...")
    
    required_packages = [
        ('dotenv', 'python-dotenv'),
        ('yaml', 'pyyaml'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('cryptography', 'cryptography'),
    ]
    
    missing_packages = []
    for module_name, package_name in required_packages:
        try:
            __import__(module_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} (missing)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print()
        print("  Missing packages detected!")
        print("  Install them with:")
        print(f"    pip install {' '.join(missing_packages)}")
        print()
        print("  Or install all dependencies:")
        print("    pip install -r requirements.txt")
        print()
    print()
    
    # Step 6: Trading mode selection
    print("Step 6: Select trading mode...")
    print("  1. Paper Trading (Recommended for beginners)")
    print("  2. Live Trading (Use with caution!)")
    print()
    
    mode_choice = input("  Select mode (1 or 2, default: 1): ").strip()
    mode = 'paper' if mode_choice != '2' else 'live'
    print(f"  Selected: {mode.upper()} mode")
    print()
    
    # Step 7: Broker selection
    print("Step 7: Select broker...")
    print("  1. Mock Broker (Safe testing, no real money)")
    print("  2. Binance (Requires API keys)")
    print("  3. Other (Manual configuration needed)")
    print()
    
    broker_choice = input("  Select broker (1, 2, or 3, default: 1): ").strip()
    broker_map = {'1': 'mock', '2': 'binance', '3': 'manual'}
    broker = broker_map.get(broker_choice, 'mock')
    print(f"  Selected: {broker.upper()}")
    print()
    
    # Update config file if chosen
    if broker in ['mock', 'binance']:
        try:
            # Check if yaml is available
            try:
                import yaml
            except ImportError:
                print("  ⚠ Cannot update config: pyyaml not installed")
                print("  Please install dependencies: pip install -r requirements.txt")
                print()
                return
            
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            config['trading']['mode'] = mode
            config['broker']['name'] = broker
            
            with open(config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            print("  ✓ Configuration updated")
            print()
        except Exception as e:
            print(f"  ⚠ Could not update config: {e}")
            print("  Please edit config.yaml manually")
            print()
    
    # Step 8: Summary
    print("=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print()
    print("Configuration Summary:")
    print(f"  Trading Mode: {mode.upper()}")
    print(f"  Broker: {broker.upper()}")
    print()
    
    print("Next Steps:")
    print()
    
    if missing_packages:
        print("1. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        print()
    
    if broker == 'binance':
        print("2. Add your Binance API credentials to .env:")
        print("   BROKER_API_KEY=your_key_here")
        print("   BROKER_API_SECRET=your_secret_here")
        print()
        print("3. Make sure sandbox mode is enabled for testing!")
        print("   Edit config.yaml and set broker.sandbox: true")
        print()
    
    print("To test your setup:")
    print("  python test_modules.py")
    print()
    
    print("To run the demo:")
    print("  python demo.py")
    print()
    
    print("To start the bot:")
    print("  python bot.py")
    print()
    
    print("⚠  IMPORTANT SAFETY REMINDERS:")
    print("  - Always start with paper trading or sandbox mode")
    print("  - Never invest more than you can afford to lose")
    print("  - Test thoroughly before using real money")
    print("  - Monitor your bot regularly")
    print("  - Keep your API keys secure")
    print()
    
    print("=" * 70)
    print("Good luck with your trading! 🚀")
    print("=" * 70)
    print()

if __name__ == "__main__":
    try:
        setup_wizard()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nSetup error: {e}")
        sys.exit(1)
