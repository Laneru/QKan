"C:\Program Files\Python311\Scripts\bandit" -r qkan >..\erg_bandit.txt
"C:\Program Files\Python311\Scripts\detect-secrets" scan qkan >..\erg_detect.txt
"C:\Program Files\Python311\Scripts\flake8" qkan >..\erg_flake8.txt
