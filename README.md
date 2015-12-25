# Multilayer EXR importer plugin for GIMP

This plugin imports multilayer EXR images into GIMP. Please note that 
layers contained in the EXR image will be converted to tga format and 
therefore reduced to 8bit/channel. So, don't use this plugin if you want 
to import high-range images into the gimp, but simply for importing 
multi-layer images such as exported by blender.
 
for this plugin to work, you also need the djv tools (djv-info and 
djv-convert) installed and correctly running on your system 
( http://djv.sourceforge.net )

Check http://yorik.uncreated.net/guestblog.php?2011=67 for 
example and instructions.
