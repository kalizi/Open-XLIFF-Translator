# Open XLIFF Translator

Open XLIFF Translator is a Python library for translating XLIFF files from WPML using [HelsinkiNLP](https://huggingface.co/Helsinki-NLP) from [HuggingFace](https://huggingface.co/). 

![Open XLIFF Translator Logo](image.webp)

## Example Usage

To use Open XLIFF Translator, simply install the dependencies using pip:

```bash
pip install -r requirements.txt
```

If you have a CUDA-enabled GPU, you can also install the GPU version of the dependencies:

```bash
pip install -r requirements-gpu.txt
```

Then, you can call the `main.py` script to translate your XLIFF files from the command line:

```bash
python main.py <input_dir> <output_dir> [--translator <translator>] [--verbose]
```

By default, the library uses the HelsinkiNLP model from HuggingFace to perform the translation. 

If your XLIFF Files are into `inputs` and want to output in the `translated`, the command will be:

```bash
python main.py inputs translated
```

## External Links

- [HelsinkiNLP](https://huggingface.co/Helsinki-NLP)
- [WPML](https://wpml.org/)
- [XLIFF](https://en.wikipedia.org/wiki/XLIFF)

## Issues

If you encounter any issues while using Open XLIFF Translator, please feel free to submit an issue using the [GitHub Issue Tracker](https://github.com/kalizi/Open-XLIFF-Translator/issues).

Any feedback and/or contributions are welcome!
