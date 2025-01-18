# Arnold to Renderman Material Converter

This is a simple python script that converts Arnold materials to Renderman materials.

For now, it only works for AiStandardSurface, and some simple nodes like :
- Bump2d
- File
- AiImage
- RemapColor
- RemapValue

# Demo video

[![Demo video](https://img.youtube.com/vi/Kw9gQE1Ob9I/hqdefault.jpg)](https://www.youtube.com/watch?v=Kw9gQE1Ob9I)


# How to install

1. Copy paste the content of [ArnoldToPxrSurface.py](https://github.com/ThomasEscalle/Ai_To_Rm_Mat_Converter/blob/main/ArnoldToPxrSurface.py) in a new script editor in Maya.
2. Select the content of the script and press the "Save Script to Shelf" button in the script editor.
3. A new button will appear in the shelf. You can now click on it to launch the script.

# How to use

1. Select the Arnold material you want to convert (must be an AiStandardSurface)
2. Click on the button in the shelf
