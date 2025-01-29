status='global'

def modify_global_status():
    global status  # Declare `status` as global
    # original_status = status  # Save the original value of `status`
    status = "python"  # Modify the global `status`
    print("Inside modify_global_status:", status)
    # status = original_status  # Restore the original value of `status`

modify_global_status()
print("Final status:", status)