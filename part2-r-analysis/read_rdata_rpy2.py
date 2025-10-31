"""
Alternative method: Use rpy2 to read R data files
This method calls R directly through Python
"""

try:
    from rpy2.robjects import r
    import rpy2.robjects as robjects
    import json
    import pandas as pd
    
    def read_rdata_with_r(filepath):
        """Read .rdata file using rpy2 (calls R directly)"""
        try:
            print(f"Reading {filepath} with R...")
            
            # Load the R data file
            r.load(filepath)
            
            # Get all objects in R environment
            objects = r.ls()
            print(f"\nObjects found in .rdata file: {list(objects)}")
            
            # Extract each object
            for obj_name in objects:
                print(f"\n--- {obj_name} ---")
                r_obj = r[obj_name]
                
                # Try to convert to pandas DataFrame
                try:
                    df = robjects.conversion.rpy2py(r_obj)
                    print(f"Type: DataFrame")
                    print(f"Shape: {df.shape}")
                    print(f"Columns: {list(df.columns)}")
                    print(f"\nFirst few rows:\n{df.head()}")
                    
                    # Save to JSON
                    output_file = f"{obj_name}.json"
                    df.to_json(output_file, orient='records', indent=2)
                    print(f"✓ Saved to {output_file}")
                    
                except Exception as e:
                    print(f"Could not convert {obj_name} to DataFrame: {e}")
                    print(f"Type: {type(r_obj)}")
                    
        except ImportError:
            print("❌ rpy2 not installed. Install with:")
            print("   pip install rpy2")
            print("\nNote: You also need R installed on your system")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    rdata_file = r"C:\Users\lukez\gpt-sentiment\gpt-sentiment-mvp\data\part 3\GL_review_PCW\GL_review_PCW.rdata"
    
    print("=" * 60)
    print("R Data File Reader (using rpy2)")
    print("=" * 60)
    
    read_rdata_with_r(rdata_file)
