# UE4Ubuntu
All tools and assets for a complete UE4 setup on Ubuntu

## Define the UE4 Environment variables


## Install QtCreatorProjectGenerator & Patch UE4 Source
+ Place the `QtCreatorProjectGenerator` folder where you want (ex:
  `/usr/local/`) and create a symlink pointing to the `UE4QtCreator.sh` shell
  script in the `/usr/bin` directory (mandatory for UE4Editor project generation
  ).

      sudo ln -s /usr/bin/ /path/to/UE4QtCreator.sh

+ Copy the `qtpatch.patch` at the root of the `UnrealEngine/` folder.

      cp UE4Ubuntu/QtTools/UnrealEngineQtPatch/qtpatch.patch $UE4_ROOT/

+ Apply the patch and delete it.

      cd $UE4_ROOT
      git am --signoff < qtpatch.patch
      rm qtpatch.patch
      
