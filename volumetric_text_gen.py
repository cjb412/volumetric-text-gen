# Enable Blender functionality in python
import bpy
import os
import sys
import errno

FONT_TYPES = ('.ttf', '.otf')

def pre_save_cleanup():
    for to_clean in [bpy.data.curves, bpy.data.fonts]:
        for block in to_clean:
            if(block.users == 0):
                to_clean.remove(block)



def main(directory = None):
    if directory == None:
        directory = os.getcwd();
    
    if not os.path.isfile(directory + "\\chars.txt"):
        print("Failed to locate 'chars.txt' character file. This is a required dependency. "
              "Either specify the pathname for the dependency folder through an argment "
              "or run the program from the dependency folder itself.")
        os.system('pause')
        exit(1)
    if not os.path.isdir(directory + "\\fonts"):
        print("Failed to locate 'fonts' input file. This is a required dependency. "
              "Either specify the pathname for the dependency folder through an argment "
              "or run the program from the dependency folder itself.")
        os.system('pause')
        exit(1)

    # Get characters to enmesh
    f = open("C:\\Users\\cdfcb\\Desktop\\FONTS\\chars.txt", "r")
    # Remove all whitespace and duplicate characters
    chars = sorted(set([*"".join(f.read().split())]))
    
    # Retrieve fonts
    fonts = [[font.split('.')[0], (f'{directory}\\fonts\\{font}')] for font in os.listdir(directory + '\\fonts') if font.endswith(FONT_TYPES)]

    # Ensure output file exists
    if not os.path.exists(f'{directory}\\output'):
        os.makedirs(f'{directory}\\output')

    success_count = 0

    for [font_name, path] in fonts:
        # Create new file
        bpy.ops.wm.read_factory_settings(use_empty=True)


        # Try loading font
        fnt = None
        try:
            fnt = bpy.data.fonts.load(filepath=path)
        except:
            print(f'There was an error loading the font {font_name}. This font will be skipped.')
            continue
        
        # Generate meshes for text
        for char in chars:
            # Generate text object
            bpy.ops.object.text_add()
            text = bpy.context.active_object
            
            # Rename text and configure location/alignment
            text.name = char
            text.data.body = char
            text.data.font = fnt
            text.data.align_x = text.data.align_y = 'CENTER'
            text.data.extrude = 0.5
            bpy.ops.transform.translate(value=(0, 0, 0.5), release_confirm=True)
            
            # Convert to mesh
            bpy.ops.object.convert(target='MESH')

        pre_save_cleanup()
        # Save output
        try:
            bpy.ops.wm.save_as_mainfile(filepath=f'{directory}\\output\\{font_name}.blend')
            success_count = success_count + 1
        except:
            print(f'There was an error saving the font {font_name}. This font will be skipped.')

    return success_count

if __name__ == "__main__":
    done = main("C:\\Users\\cdfcb\\Desktop\\FONTS")
    print(f'Successfully prepared meshes for {done} fonts.')
    os.system('pause')
    exit(0)