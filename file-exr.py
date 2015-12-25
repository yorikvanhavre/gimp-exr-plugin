#!/usr/bin/env python
import os, tempfile, sys, subprocess
from gimpfu import *

__author__="Yorik van Havre - http://yorik.uncreated.net"

'''
This plugin imports multilayer EXR images into GIMP. Please note that layers
contained in the EXR image will be converted to tga format and therefore reduced
to 8bit/channel. So, don't use this plugin if you want to import high-range images
into the gimp, but simply for importing multi-layer images such as exported by blender.

for this plugin to work, you also need the djv tools (djv-info and djv-convert) installed
and correctly running on your system ( http://djv.sourceforge.net )
'''

def load_exr(filename,raw_filename):

    # pre-run checks.
    if subprocess.call(["djv_info"]) != 0:
        pdb.gimp_message("error: djv is not installed on this system. See http://djv.sourceforge.net")
        #exit()
    if not os.path.exists(filename):
        pdb.gimp_message("error: file not found")
        #exit()
    
    # getting RGBA layers
    layInfo = str(subprocess.check_output(["djv_info", filename])).split("\n")
    layers = []
    for lay in layInfo:
        if "RGBA" in lay:
            nr = lay.split()[0].strip(".")
            layers.append(nr)

    # extracting layers
    tempDir = tempfile.mkdtemp()
    for lay in layers:
        subprocess.call(["djv_convert", filename, '-layer',lay,os.path.join(tempDir,lay+'.tga')])

    # creating the GIMP image
    newpath = os.path.join(tempDir,layers[0]+".tga")
    img = pdb.gimp_file_load(newpath,0)
    base = pdb.gimp_image_new(img.width,img.height,0)
    for l in layers:
        img = pdb.gimp_file_load_layer(base,os.path.join(tempDir,l+".tga"))
        pdb.gimp_image_add_layer(base,img,-1)
        os.remove(os.path.join(tempDir,l+".tga"))
    os.rmdir(tempDir)
    return base
    
#def register_handlers():
def register_load_handlers():
    gimp.register_load_handler('file-exr-load', 'exr', '')
    # gimp.register_save_handler('file-exr-save', 'exr', '')
    #TODO: should we set mime association on save as well?
    pdb['gimp-register-file-handler-mime']('file-exr-load', 'image/openexr') 
    # pdb['gimp-register-thumbnail-loader']('file-exr-load', 'file-exr-load-thumb')

register(
    'file-exr-load', #name
    'load a multilayer exr (.exr) file', #description
    'load a multilayer exr (.exr) file',
    'Yorik van Havre', #author
    'Yorik van Havre', #copyright
    '2011', #year
    'OpenEXR',
    None, #image type
    [   #input args. Format (type, name, description, default [, extra])
        (PF_STRING, 'filename', 'The name of the file to load', None),
        (PF_STRING, 'raw-filename', 'The name entered', None),
    ], 
    [(PF_IMAGE, 'image', 'Output image')], #results. Format (type, name, description) 
    load_exr, #callback
    on_query = register_load_handlers, 
    menu = "<Load>",
)

main()
