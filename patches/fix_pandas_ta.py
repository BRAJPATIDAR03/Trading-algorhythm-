import os
import shutil

def patch_pandas_ta():
    """Patch pandas-ta package for compatibility"""
    try:
        import pandas_ta
        pkg_path = os.path.dirname(pandas_ta.__file__)
        
        # Backup the original file
        squeeze_pro_path = os.path.join(pkg_path, 'momentum', 'squeeze_pro.py')
        backup_path = squeeze_pro_path + '.backup'
        
        if not os.path.exists(backup_path):
            shutil.copy2(squeeze_pro_path, backup_path)
        
        # Read and modify the file
        with open(squeeze_pro_path, 'r') as f:
            content = f.read()
        
        # Replace problematic imports
        replacements = [
            ('from numpy import NaN as npNaN', 'from numpy import nan as npNaN'),
            ('NaN', 'nan'),
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Write back
        with open(squeeze_pro_path, 'w') as f:
            f.write(content)
            
        print("Successfully patched pandas-ta")
        
    except Exception as e:
        print(f"Error patching pandas-ta: {e}")

if __name__ == "__main__":
    patch_pandas_ta()