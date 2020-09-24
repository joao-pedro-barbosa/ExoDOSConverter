import os,shutil, subprocess, sys, traceback
from confconverter import ConfConverter
from metadatahandler import MetadataHandler

# Main Converter
class ExoDOSConverter():
    
    def __init__(self,games, cache,collectionDir,gamesDosDir,outputDir, conversionType, useGenreSubFolders,logger) :
        self.games = games
        self.cache = cache
        self.exoDosDir = os.path.join(collectionDir,'eXoDOS')
        self.logger = logger
        self.gamesDosDir = gamesDosDir
        self.outputDir = outputDir
        self.conversionType = conversionType
        self.useGenreSubFolders = useGenreSubFolders
        self.metadataHandler = MetadataHandler(collectionDir, self.cache,self.logger)
        self.confConverter = ConfConverter(self.games, self.exoDosDir, self.outputDir, self.useGenreSubFolders, self.conversionType, self.logger)
    
    # Loops on all games to convert them
    def convertGames(self) :
        self.logger.log("Loading metadatas...")
        self.metadataHandler.parseXmlMetadata()
        self.logger.log("")
        if not os.path.exists(os.path.join(self.outputDir,'downloaded_images')) :
            os.mkdir(os.path.join(self.outputDir,'downloaded_images'))
        if not os.path.exists(os.path.join(self.outputDir,'manuals')) :
            os.mkdir(os.path.join(self.outputDir,'manuals'))
        
        gamelist = self.metadataHandler.initXml(self.outputDir)
        
        count = 1;
        total = len(self.games)
        errors = dict()
        
        for game in self.games :
            try:
                self.convertGame(game, gamelist, total, count)                
            except:
                self.logger.log('Error %s while converting game %s' %(sys.exc_info()[0],game))
                excInfo = traceback.format_exc()                
                errors[game] =excInfo
                
            count = count + 1
        
        self.metadataHandler.writeXml(self.outputDir, gamelist)
        self.logger.log('\n<--------- Finished Process --------->')
        
        if len(errors.keys())>0 :
            self.logger.log('\n<--------- Errors rundown --------->')
            self.logger.log('%i errors were found during process' %len(errors.keys()))
            self.logger.log('See error log in your outputDir')
            logFile = open(os.path.join(self.outputDir,'error_log.txt'),'w')
            for key in list(errors.keys()) :
                logFile.write("Found error when processing %s" %key+" :\n")
                logFile.write(errors.get(key))
                logFile.write("\n")
            logFile.close()
        elif os.path.exists(os.path.join(self.outputDir,'error_log.txt')) :
            # Delete log from previous runs
            os.remove(os.path.join(self.outputDir,'error_log.txt'))
            
            
    # Full conversion for a given game    
    def convertGame(self, game, gamelist, total, count) :
        #TODO See if it is still mandatory as we could retrieve that from self.metadataHandler.processGame now
        genre = self.metadataHandler.buildGenre(self.metadataHandler.metadatas.get(game))
        self.logger.log(">>> %i/%i >>> %s: starting conversion" %(count,total,game))
        self.metadataHandler.processGame(game,gamelist,genre, self.outputDir, self.useGenreSubFolders, self.conversionType)
        
        dest = os.path.join(self.outputDir,genre,game+".pc") if self.useGenreSubFolders else os.path.join(self.outputDir,game+".pc")
        #TODO needs rework to handle or not genre folder
        if not os.path.exists(dest):            
            if not os.path.exists(os.path.join(self.exoDosDir,"Games",game)):
                self.logger.log("  needs installation...")
                #automatic F and N to validate answers to exo's install.bat, might want to allow other values in the future
                subprocess.call("cmd /C (echo Y&echo F&echo N) | Install.bat", cwd=os.path.join(self.gamesDosDir,game), shell=False)
                self.logger.log("  installed")
            else :
                self.logger.log("  already installed")
            
            self.copyGameFiles(game,dest)    
            self.confConverter.process(game,dest,genre)
        else :
            self.logger.log("  already converted in output folder")
        
        self.logger.log("")      
        
    # Copy game files and game dosbox.conf to output dir    
    def copyGameFiles(self,game,gameOutputDir):
        dest = os.path.join(gameOutputDir,game)
        self.logger.log("  copy game data")        
        # Copy game files in game.pc/game
        shutil.copytree(os.path.join(self.exoDosDir,"Games",game),dest)
        self.logger.log("  copy dosbox conf")
         # Copy dosbox.conf in game.pc
        shutil.copy2(os.path.join(self.exoDosDir,"Games","!dos",game,"dosbox.conf"),os.path.join(dest,"dosbox.conf"))
        
