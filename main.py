import subprocess
import sys

def run(script):
    print(f"\n=== RUN: {script} ===")
    subprocess.check_call([sys.executable, f"scripts/{script}"])

if __name__ == "__main__":
    run("bronze_ingestion.py")
    run("create_silver_sql.py")
    run("create_gold_sql.py")
    print("\n✅ Pipeline terminée. Importe silver/ et gold/ dans phpMyAdmin.")
