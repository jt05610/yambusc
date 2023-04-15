pyinstaller --onefile -n yambusc src/yambusc/cli.py
chmod +x dist/yambusc
cp -r src/templates ~/scripts/lib/yambusc
cp dist/yambusc ~/scripts/bin