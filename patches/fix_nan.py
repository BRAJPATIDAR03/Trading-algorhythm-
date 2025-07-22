import os
import shutil

def fix_pandas_ta():
    try:
        import pandas_ta
        pkg_path = os.path.dirname(pandas_ta.__file__)
        
        # Files to patch
        files = {
            'momentum/squeeze_pro.py': [
                ('from numpy import NaN as npNaN', 'from numpy import nan as npNaN'),
                ('NaN', 'nan')
            ]
        }
        
        for file_name, replacements in files.items():
            file_path = os.path.join(pkg_path, file_name)
            backup_path = file_path + '.backup'
            
            # Create backup
            if not os.path.exists(backup_path):
                shutil.copy2(file_path, backup_path)
            
            # Apply patches
            with open(file_path, 'r') as f:
                content = f.read()
            
            for old, new in replacements:
                content = content.replace(old, new)
            
            with open(file_path, 'w') as f:
                f.write(content)
        
        print("Successfully patched pandas-ta")
        
    except Exception as e:
        print(f"Error patching pandas-ta: {e}")

if __name__ == "__main__":
    fix_pandas_ta()