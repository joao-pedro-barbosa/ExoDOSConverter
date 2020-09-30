# ExoDOSConverter

a custom converter of the ExoDOS collection v4 to several EmulationStation and/or Linux based distributions format : 
 - Recalbox
 - Batocera
 - Retropie
 - OpenDingux (both SimpleMenu / Esoteric flavours) with mapping for RG350
 - MiSTer (in the future)

## ExoDOS

https://www.retro-exo.com

For those of you for which this name doesn't mean anything, ExoDOS Collection is a collection of DOS games and in my opinion the best one as it includes full, correct configuration for all games.
It is based on Launchbox and Windows only though
There's also an ExoDOSWin3x collection for Windows 3.1 games

Before using this tool, don't forget to install the collection with its `setup.bat`

## The Tool

ExoDOSConverter is a rework with GUI of an old project of mine, and the aim is to fully support ExoDOS v5 and ExoWin3x v2 when they are released.
For now the tool works with current versions of the collection

The aim of this tool is to convert any selection of games of the ExoDOS collection to emulationstation / basic dosbox for linux format, so that in can be used on Retropie on any other like minded distribution.

The conversion should cover the following :
 - conversion of the game to a correct format, including dosbox.cfg and dosbox.bat
 - scrapping of the game metadata, including front boxart and manuals

As the ExoDOSCollection itself uses a lot of `.bat` script and other Windows-only features, this tool will also be windows only.
This might evolve is some workaround are found to fully exploit this on Linux on other OSes

### LINUX INSTALLATION AND EXECUTION :
- eXoDOSConverter requires that python3 is installed (it's developed on 3.8)
- first install Tkinter for python3 if needed : `sudo apt-get install python3-tk`
- directly download sources or clone the repo with :
 ```
 sudo apt install git # optional, only if git is not installed
 git clone https://github.com/Voljega/ExoDOSConverter
 ```
- give execution rights to `ExoDOSConverter.sh` :
```
cd ExoDOSConverter            # change to ExoDOSConverter directory
chmod u+x ExoDOSConverter.sh  # give execution perms (already done in git-cloned version)
```
- If you didn't install the collection beforehand on Windows or with wine by executing `setup.bat`, you'll need to do that or  alternatively:
>Unzip `XODOSMetadata.zip` to the home dir of the collection, this should create a `Images` folder

>Unzip `!DOSmetadata.zip` to the home dir of the collection, this should create a `eXoDOS/Games/!dos folder`

>Unzip `LaunchBox.zip` to the home dir of the collection, this should create a `Metadata` folder

- launch with `./ExoDOSConverter.sh` or `./ExoDOSConverter`

## State of development

For now the tool is in beta stage, it seems to work fine, but some games throw errors when beeing converted.
This will be corrected when possible

Fully supported distributions are Batocera, Recalbox, Retropie and OpenDingux.

Next step is to add MiSTer compatibility

## RG350

For RG350, select the flavor of frontend you are using (either SimpleMenu or Esoteric/GxMenu)
Don't forget to select 'RG350' for the mapper, this will generate the defaut mapping for controls :
 - DPad: directions
 - Select: ESC
 - Start: Enter
 - A: Left Alt
 - B: Space
 - X: Left Control
 - Y: Left Shift
 - L1: n
 - R1: y
 
 Remember that L1 displays the virtual keyboard.
 Power+B activates the mouse on right stick, with L2 and R2 as left and right buttons 

Launch the game by clicking `dosbox.bat` inside the game folder
If the default mappings are practical for the game, modify 'mapper.map' inside the game folder

You can quit dosbox by `Power+Select`

*EDIT Note :* 

The specific nature of dosbox on RG350 doesn't actually allows for custom mapping on a game by game basis, nor does it takes into account the dosbox.cfg for each game.

The only way to do that at the moment seems to modify `dosbox.conf` in `/media/data/local/home/.dosbox/` :

- copy the `mapper.map` of the game into  `/media/data/local/home/.dosbox/`
- edit the line starting with `mapper` and change the mapper name to `mapper.map`
- you can then modify the mapper.map file however you want, but this mapping will be taken into account for all games

I'm still in search of a solution to allow a real custom configuration and mapping for all games on RG350