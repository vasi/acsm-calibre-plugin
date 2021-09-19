#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Calibre plugin for ACSM files.


from calibre.customize import FileTypePlugin        # type: ignore
__version__ = '0.0.1'

PLUGIN_NAME = "DeACSM"
PLUGIN_VERSION_TUPLE = tuple([int(x) for x in __version__.split(".")])
PLUGIN_VERSION = ".".join([str(x)for x in PLUGIN_VERSION_TUPLE])

import os
import traceback

from calibre.utils.config import config_dir         # type: ignore
from calibre.constants import iswindows, isosx      # type: ignore



class DeACSM(FileTypePlugin):
    name                        = PLUGIN_NAME
    description                 = "Takes an Adobe ACSM file and converts that into a useable EPUB file"
    supported_platforms         = ['linux']
    author                      = "Leseratte10"
    version                     = PLUGIN_VERSION_TUPLE
    minimum_calibre_version     = (5, 0, 0)
    file_types                  = set(['acsm'])
    on_import                   = True
    on_preprocess               = True
    priority                    = 2000

    def initialize(self):
        """
        Dynamic modules can't be imported/loaded from a zipfile.
        So this routine will extract the appropriate
        library for the target OS and copy it to the 'alfcrypto' subdirectory of
        calibre's configuration directory. That 'alfcrypto' directory is then
        inserted into the syspath (as the very first entry) in the run function
        so the CDLL stuff will work in the alfcrypto.py script.
        The extraction only happens once per version of the plugin
        Also perform upgrade of preferences once per version
        """
        try:
            self.pluginsdir = os.path.join(config_dir,"plugins")
            if not os.path.exists(self.pluginsdir):
                os.mkdir(self.pluginsdir)
            self.maindir = os.path.join(self.pluginsdir,"DeACSM")
            if not os.path.exists(self.maindir):
                os.mkdir(self.maindir)

            # only continue if we've never run this version of the plugin before
            self.verdir = os.path.join(self.maindir,PLUGIN_VERSION)
            if not os.path.exists(self.verdir):
                if iswindows:
                    print("Windows not supported yet")
                    return
                elif isosx:
                    print("Mac not supported yet")
                    return
                else:
                    names = ["acsmdownloader", "adept_activate", "libgourou.so", "libzip.so.4"]
                    
                lib_dict = self.load_resources(names)
                print("{0} v{1}: Copying needed library files from plugin's zip".format(PLUGIN_NAME, PLUGIN_VERSION))

                for entry, data in lib_dict.items():
                    file_path = os.path.join(self.alfdir, entry)
                    try:
                        os.remove(file_path)
                    except:
                        pass

                    try:
                        open(file_path,'wb').write(data)
                    except:
                        print("{0} v{1}: Exception when copying needed library files".format(PLUGIN_NAME, PLUGIN_VERSION))
                        traceback.print_exc()
                        pass

                # mark that this version has been initialized
                os.mkdir(self.verdir)
        except Exception as e:
            traceback.print_exc()
            raise

    def is_customizable(self):
        return True

    def config_widget(self):
        import calibre_plugins.deacsm.config as config   # type: ignore
        return config.ConfigWidget(self.plugin_path)

    def save_settings(self, config_widget):
        config_widget.save_settings()

    def run(self, path_to_ebook: str):
        # This code gets called by Calibre with a path to the new book file. 
        # We need to check if it's an ACSM file

        print("{0} v{1}: Trying to parse file {2}".format(PLUGIN_NAME, PLUGIN_VERSION, os.path.basename(path_to_ebook)))

        print("{0} v{1}: Failed, return original ...".format(PLUGIN_NAME, PLUGIN_VERSION))
        return path_to_ebook



