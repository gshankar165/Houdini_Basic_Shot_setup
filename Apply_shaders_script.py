import sys
import os

sys.path.append("/drive/common_funcs_path")
import Show_common_funcs.Show_common_funcs as com_func
import Show_common_funcs.Show_logic_funcs as log_func
#reload(com_func)
#reload(log_func)

print log_func.material_import()
print log_func.material_connect_logic()
print log_func.set_netbox()
