# UE4Ubuntu
All tools and assets for a complete UE4 setup on Ubuntu.

## Install QtCreator
From terminal,

      sudo apt-get install qtcreator

or from Ubuntu Software Center, search for and install the *qtcreator* app directly.

## Define UE4 Environment variables
`UE4_ROOT` : path to the UnrealEngine root source directory,  
`UE4_BIN` : path to the Linux binaries (UE4Editor, UnrealHeaderTool, UnrealPak...),  
`UE4_UBT` : path to the UnrealBuildTool launcher script,  
`UE4Editor` : alias for UE4Editor launcher (walkaround resolving relative path asset dependencies).

+ In the *terminal*,
      cd
      gedit .bashrc
+ then in *gedit*, replace */path/to* by your UnrealEngine source path (ex: */home/tomato/unreal_source*).
      export UE4_ROOT='/path/to/UnrealEngine'
      export UE4_BIN='/path/to/UnrealEngine/Engine/Binaries/Linux'
      export UE4_UBT='/path/to/UnrealEngine/Engine/Build/BatchFiles/Linux/Build.sh'
      alias UE4Editor='cd $UE4_BIN && ./UE4Editor'



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
