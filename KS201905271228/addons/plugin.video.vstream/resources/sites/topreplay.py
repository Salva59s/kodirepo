#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

import re

SITE_IDENTIFIER = 'topreplay'
SITE_NAME = 'TopReplay'
SITE_DESC = 'Replay TV'

URL_MAIN = 'http://www.topreplay.tv'
URL_SEARCH = (URL_MAIN + '/index.php?do=search&subaction=search&story=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '/index.php?do=search&subaction=search&story=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'

REPLAYTV_GENRES = (True, 'showGenre')
REPLAYTV_NEWS = (URL_MAIN + '/videos/', 'showMovies')
REPLAYTV_REPLAYTV = ('http://' , 'load')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_NEWS[1], 'Nouveautés', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', URL_MAIN)
    oGui.addDir(SITE_IDENTIFIER, 'showListe', 'Liste des émissions', 'replay.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', REPLAYTV_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, REPLAYTV_GENRES[1], 'Genres', 'replay.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()
    #nextpage recherche non pris en compte volontairement a voir plus tard ou pas (multiple de 37)
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_SEARCH[0] + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenre():
    oGui = cGui()
    oParser = cParser()
    oRequestHandler = cRequestHandler(URL_MAIN)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<\/span>.+?par genre<\/h3>(.+?)<li class="active">'
    aResult = re.search(sPattern, sHtmlContent, re.DOTALL)
    if (aResult):
        sHtmlContent = aResult.group(1)
        sPattern = '<li><a href="([^"]+)">([^<]+)<\/a><\/li>'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            total = len(aResult[1])
            progress_ = progress().VScreate(SITE_NAME)
            for aEntry in aResult[1]:
                progress_.VSupdate(progress_, total)
                if progress_.iscanceled():
                    break

                sTitle = aEntry[1]
                if 'Film' in sTitle:
                    continue
                sUrl = URL_MAIN + aEntry[0]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle , 'replay.png', oOutputParameterHandler)

            progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showListe():
    oGui = cGui()
    oRequestHandler = cRequestHandler(URL_MAIN + '/listing-emissions.html')
    sHtmlContent = oRequestHandler.request()

    oParser = cParser()
    sHtmlContent = oParser.abParse(sHtmlContent, '<div class="other-title">', 'class="clearfix">')

    sPattern = '<li><a href="(.+?)">(.+?)<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl = URL_MAIN + aEntry[0]
            sTitle = aEntry[1]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle , 'replay.png', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
      sUrl = sSearch.replace(" ", "+")
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="img-short"><img src="([^"]+)".+?<a href="([^"]+)">([^<]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)
        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sThumb = aEntry[0]
            if sThumb.startswith('/imgg='):
                sThumb = 'http://' + sThumb.replace('/imgg=','')
            elif sThumb.startswith('/uploads'):
                sThumb = URL_MAIN + sThumb
                
            sUrl = aEntry[1]
            sTitle = aEntry[2]

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'replay.png', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    oParser = cParser()
    sPattern = '<li><a href="([^"]+)">Suivant<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def checkforHoster(sHosterUrl):
    #principal hoster les autres avec que des videos hs non mis
    code = re.search('\/(.+?)=([^"]+)', sHosterUrl)
    if not 'php?link' in code.group(1):
        if 'openload' in sHosterUrl:
            return 'https://openload.co/embed/' + code.group(2)
        elif 'netu' in sHosterUrl:
            return 'http://hqq.tv/player/embed_player.php?vid=' + code.group(2)
        elif 'allvid' in sHosterUrl:
            return 'http://allvid.ch/embed-' + code.group(2) + '.html'
        elif 'easyvid' in sHosterUrl:
            return 'http://easyvid.org/embed-' + code.group(2) + '.html'
        elif 'rutube' in sHosterUrl:
            return 'http://rutube.ru/play/embed/' + code.group(2)
        elif 'vidlox' in sHosterUrl:
            return 'https://vidlox.tv/' + code.group(2)
        elif 'streammoe' in sHosterUrl:
            return 'https://stream.moe/embed-' + code.group(2) + '.html'
        elif 'playernaut' in sHosterUrl or 'raptu' in sHosterUrl:
            return 'https://www.raptu.com/embed/' + code.group(2)
        elif 'rapidvideo' in sHosterUrl:
            return 'https://www.rapidvideo.com/e/' + code.group(2)
        elif 'dailymotion' in sHosterUrl:
            return 'http://www.dailymotion.com/embed/video/' + code.group(2)
        elif 'filez' in sHosterUrl:
            return 'http://filez.tv/embed/u=' + code.group(2)
        elif 'mixloads' in sHosterUrl:
            return 'https://mixloads.com/embed-' + code.group(2) + '.html'
        elif 'youwatch' in sHosterUrl:
            return 'http://www.youwatch.org/embed-' + code.group(2) + '.html'
        elif 'exashare' in sHosterUrl:
            return 'http://exashare.com/embed-' + code.group(2) + '.html'
        elif 'estream' in sHosterUrl:
            return 'https://estream.to/' + code.group(2) + '.html'
        elif 'gounlimited' in sHosterUrl:
            return 'https://gounlimited.to/embed-' + code.group(2) + '.html'  
        elif 'uptostream' in sHosterUrl:
            return 'https://uptostream.com/' + code.group(2)
        elif 'mail.ru' in sHosterUrl:
            code = re.search('\/mail\.ru.+?embed\/([^"]+)',sHosterUrl)
            if code:
                return 'http://my.mail.ru/video/embed/' + code.group(1)
    else:
        if 'uptobox' in sHosterUrl:
            code = re.search('/plyr/.+?//uptobox.com/([^"]+)', sHosterUrl)
            if code:
                return 'https://uptobox.com/' + code.group(1)

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    #integrale saison
    sPattern = '<div class="img-short"><img src="([^"]+)".+?<a href="([^"]+)">([^<]+)<\/a>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sThumb = aEntry[0]
            sUrl = aEntry[1]
            sTitle = aEntry[2]


            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMisc(SITE_IDENTIFIER, 'showHosters', sTitle, 'replay.png', sThumb, '', oOutputParameterHandler)
    else:
        #1
        sPattern = '<option value="([^"]+)"'
        aResult1 = re.findall(sPattern, sHtmlContent)
        #2
        sPattern = '<iframe.+?src="([^"]+)" style=".+?".+?<\/iframe>'
        aResult2 = re.findall(sPattern, sHtmlContent)

        aResult = []
        aResult = list(set(aResult1 + aResult2)) #pas de doublons

        if (aResult):
            for aEntry in aResult:
                sHosterUrl = checkforHoster(str(aEntry))

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
