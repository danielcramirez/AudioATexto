from PyInstaller.utils.hooks import collect_data_files

# Collect imblearn data files including VERSION.txt
datas = collect_data_files('imblearn')
