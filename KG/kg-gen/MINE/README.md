# Running MINE

To run MINE:
1. Change `"YOUR_OPENAI_KEY"` to your actual key in [`evaluation.py`](evaluation.py).
2. Use your KG generator to generate a KG from each of the essays found in [`essays.json`](essay.json). The KGs should be JSON files structured in the same way as [`example.json`](example.json).
3. Name these KGs `1.json`, `2.json`, ..., `106.json` in order and place them in the `KGs/` folder in this directory.
4. Run `python evaluation.py`.
5. Look for the files `1_result.json`,..., `106_result.json` in the `KGs/` folder.