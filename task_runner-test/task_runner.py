from pywheels.task_runner import execute_python_script


def main():
    
    python_script = r"""
print(1 + 1, end = "")
"""

    run_script_result = execute_python_script(python_script)
    
    print(f"success: {run_script_result['success']}")
    print(f"stdout: {run_script_result['stdout']}")


if __name__ == "__main__":
    
    main()