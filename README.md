If you do changes, make sure you save it and run the following command in and ide like visual studio code

python -m PyInstaller --onefile --windowed --name "CircleAttention" circle_attention.py

Here's what each flag does:

- `--onefile` — bundles everything into a single `.exe` file
- `--windowed` — hides the console window so only the game window shows
- `--name "CircleAttention"` — sets the output filename

The resulting `.exe` ends up in the `dist` folder.
