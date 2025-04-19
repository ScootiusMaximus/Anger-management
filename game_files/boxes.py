from game_files.textbox import *

chewy = "fonts/Chewy/Chewy-Regular.ttf"

titlebox = NiceTextbox(None,"ANGER MANAGEMENT",pygame.font.Font(chewy,90),(0,0),tags=["menu"])
splashbox = NiceTextbox(None,"Be kind to your spacebar!",pygame.font.Font(chewy,20),(0,0),tags=["menu"])
playbox = NiceTextbox(None,"BEGIN ANGER",pygame.font.Font(chewy,50),(0,0),tags=["menu"])
scorebox = NiceTextbox(None,"",pygame.font.Font(chewy,40),(0,0),tags=["ingame"])
togglesidebar = NiceTextbox(None,">",pygame.font.Font(chewy,80),(0,0),tags=["ingame"])
indevbox = NiceTextbox(None,"In development!",pygame.font.Font(chewy,30),(0,0),tags=["menu","ingame"],textcol=(0,0,50))
debug = NiceTextbox(None,"debug:",pygame.font.Font(chewy,30),(0,0),tags=[])

valuebox = NiceTextbox(None,"",pygame.font.Font(chewy,40),(0,0),tags=[])
ratebox = NiceTextbox(None,"",pygame.font.Font(chewy,40),(0,0),tags=[])
speedbox = NiceTextbox(None,"",pygame.font.Font(chewy,40),(0,0),tags=[])
upgradevaluebox = NiceTextbox(None,"",pygame.font.Font(chewy,25),(0,0),tags=[])
upgraderatebox = NiceTextbox(None,"",pygame.font.Font(chewy,25),(0,0),tags=[])
upgradespeedbox = NiceTextbox(None,"",pygame.font.Font(chewy,25),(0,0),tags=[])

boxes = [titlebox,splashbox,playbox,scorebox,togglesidebar,valuebox,
         ratebox,speedbox,upgradevaluebox,upgraderatebox,upgradespeedbox,
         indevbox,debug]

def reposition_boxes(width,height):
    titlebox.move_to((width*0.5,height*0.1))
    splashbox.move_to((width*0.5,height*0.2))
    playbox.move_to((width*0.5,height*0.5))
    scorebox.move_to((width*0.5,height*0.2))
    togglesidebar.move_to((width*0.75,height*0.1))
    indevbox.move_to((width*0.1,height*0.05))
    debug.move_to((width*0.5,height*0.03))

    valuebox.move_to((width*0.9,height*0.3))
    upgradevaluebox.move_to((width * 0.9, height * 0.4))
    ratebox.move_to((width*0.9,height*0.5))
    upgraderatebox.move_to((width*0.9,height*0.6))
    speedbox.move_to((width*0.9,height*0.7))
    upgradespeedbox.move_to((width*0.9,height*0.8))