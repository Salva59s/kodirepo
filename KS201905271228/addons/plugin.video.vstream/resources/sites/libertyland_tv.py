#-*- coding: utf-8 -*-
#Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
#from resources.lib.util import cUtil
from resources.lib.comaddon import progress, VSlog
import re

SITE_IDENTIFIER = 'libertyland_tv'
SITE_NAME = 'Libertyland'
SITE_DESC = 'Les films et séries récentes en streaming et en téléchargement'

URL_MAIN = 'https://libertyvf.com/'

URL_SEARCH = (URL_MAIN + 'v2/recherche/', 'showMovies')
URL_SEARCH_MOVIES = ('', 'showMovies')
URL_SEARCH_SERIES = ('', 'showMovies')

FUNCTION_SEARCH = 'showMovies'

MOVIE_NEWS = (URL_MAIN + 'films/nouveautes/', 'showMovies')
MOVIE_VIEWS = (URL_MAIN + 'films/plus-vus-mois/', 'showMovies')
MOVIE_NOTES = (URL_MAIN + 'films/les-mieux-notes/', 'showMovies')
MOVIE_GENRES = (True, 'showMovieGenres')
MOVIE_ANNEES = (True, 'showMovieAnnees')
MOVIE_VOSTFR = (URL_MAIN + 'films/films-vostfr/', 'showMovies')

SERIE_SERIES = (URL_MAIN + 'series/', 'showMovies')
SERIE_GENRES = (True, 'showSerieGenres')
SERIE_ANNEES = (True, 'showSerieAnnees')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'typeSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_VIEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_VIEWS[1], 'Films (Les plus vus)', 'views.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NOTES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NOTES[1], 'Films (Les mieux notés)', 'notes.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_SERIES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_SERIES[1], 'Séries', 'series.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_GENRES[1], 'Séries (Genres)', 'genres.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', SERIE_ANNEES[0])
    oGui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def typeSearch():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sCat', '1')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Films', 'films.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('sCat', '2')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Séries', 'series.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'films/genre/action.html'] )
    liste.append( ['Animation', URL_MAIN + 'films/genre/animation.html'] )
    liste.append( ['Arts martiaux', URL_MAIN + 'films/genre/arts-martiaux.html'] )
    liste.append( ['Aventure', URL_MAIN + 'films/genre/aventure.html'] )
    liste.append( ['Biographie', URL_MAIN + 'films/genre/biographie.html'] )
    liste.append( ['Comédie', URL_MAIN + 'films/genre/comedie.html'] )
    liste.append( ['Crime', URL_MAIN + 'films/genre/crime.html'] )
    liste.append( ['Drame', URL_MAIN + 'films/genre/drame.html'] )
    liste.append( ['Espionnage', URL_MAIN + 'films/genre/espionnage.html'] )
    liste.append( ['Fantastique', URL_MAIN + 'films/genre/fantastique.html'] )
    liste.append( ['Guerre', URL_MAIN + 'films/genre/guerre.html'] )
    liste.append( ['Histoire', URL_MAIN + 'films/genre/histoire.html'] )
    liste.append( ['Horreur', URL_MAIN + 'films/genre/horreur.html'] )
    liste.append( ['Musical', URL_MAIN + 'films/genre/musical.html'] )
    liste.append( ['Policier', URL_MAIN + 'films/genre/policier.html'] )
    liste.append( ['Romance', URL_MAIN + 'films/genre/romance.html'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'films/genre/science-fiction.html'] )
    liste.append( ['Sport', URL_MAIN + 'films/genre/sport.html'] )
    liste.append( ['Thriller', URL_MAIN + 'films/genre/thriller.html'] )
    liste.append( ['Western', URL_MAIN + 'films/genre/western.html'] )
    #la suite fonctionnent mais n'est pas répertorié dans le moteur de genre du site
    liste.append( ['Biopic', URL_MAIN + 'films/genre/biopic.html'] )
    liste.append( ['Comédie Dramatique', URL_MAIN + 'films/genre/comedie-dramatique.html'] )
    liste.append( ['Comédie Musicale', URL_MAIN + 'films/genre/comedie-musicale.html'] )
    liste.append( ['Famille', URL_MAIN + 'films/genre/famille.html'] )
    liste.append( ['Historique', URL_MAIN + 'films/genre/historique.html'] )
    liste.append( ['Judiciaire', URL_MAIN + 'films/genre/judiciaire.html'] )
    liste.append( ['Médical', URL_MAIN + 'films/genre/medical.html'] )
    liste.append( ['Péplum', URL_MAIN + 'films/genre/peplum.html'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'series/genre/action/'] )
    liste.append( ['Animé', URL_MAIN + 'series/genre/anime/'] )
    liste.append( ['Aventure', URL_MAIN + 'series/genre/aventure/'] )
    liste.append( ['Comédie', URL_MAIN + 'series/genre/comedie/'] )
    liste.append( ['DC Comics', URL_MAIN + 'series/genre/dc-comics/'] )
    liste.append( ['Documentaire', URL_MAIN + 'series/genre/documentaire/'] )
    liste.append( ['Drama', URL_MAIN + 'series/genre/drama/'] )
    liste.append( ['Drame', URL_MAIN + 'series/genre/drame/'] )
    liste.append( ['Emission TV', URL_MAIN + 'series/genre/emission-tv/'] )
    liste.append( ['Epouvante-Horreur', URL_MAIN + 'series/genre/epouvante-horreur/'] )
    liste.append( ['Fantastique', URL_MAIN + 'series/genre/fantastique/'] )
    liste.append( ['Gore', URL_MAIN + 'series/genre/gore/'] )
    liste.append( ['Guerre', URL_MAIN + 'series/genre/guerre/'] )
    liste.append( ['Historique', URL_MAIN + 'series/genre/historique/'] )
    liste.append( ['Mystère', URL_MAIN + 'series/genre/mystere/'] )
    liste.append( ['Policier', URL_MAIN + 'series/genre/policier/'] )
    liste.append( ['Romance', URL_MAIN + 'series/genre/romance/'] )
    liste.append( ['Science-Fiction', URL_MAIN + 'series/genre/science-fiction/'] )
    liste.append( ['Série TV', URL_MAIN + 'series/genre/serie-tv/'] )
    liste.append( ['Thriller', URL_MAIN + 'series/genre/thriller/'] )
    liste.append( ['Télé-réalité', URL_MAIN + 'series/genre/tele-realite/'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1914, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'films/annee/' + Year + '.html')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showSerieAnnees():
    oGui = cGui()

    for i in reversed (xrange(1989, 2019)):
        Year = str(i)
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', URL_MAIN + 'v2/series/annee/' + Year + '/')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', Year, 'annees.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()

    if sSearch:

        scategorie = ''
        sUrl = ''

        sCat = oInputParameterHandler.getValue('sCat')

        if (sCat == '2'):#serie
            scategorie = 'series'
        elif (sCat == '1'):#film
            scategorie = 'films'
        else:#tout le reste
            scategorie = 'films'

        sUrl = URL_MAIN + 'v2/recherche/'

        oRequestHandler = cRequestHandler(sUrl)
        #oRequestHandler.addHeaderEntry('Referer', 'https://libertyvf.com/v2/recherche/')
        oRequestHandler.setRequestType(cRequestHandler.REQUEST_TYPE_POST)
        oRequestHandler.addParameters('categorie', scategorie)
        oRequestHandler.addParameters('mot_search', sSearch)
        sHtmlContent = oRequestHandler.request()

        sPattern = '<h2 class="heading">\s*<a href="([^<>"]+)">([^<]+)<\/a>.+?<img class="img-responsive" *src="(.+?)"'

    else:
        sUrl = oInputParameterHandler.getValue('siteUrl')

        oRequestHandler = cRequestHandler(sUrl)
        sHtmlContent = oRequestHandler.request()

        if '/series' in sUrl:
            sPattern = '<div class="divstreaming".+?href="([^"]+)"><strong>([^<]+)<\/strong>.+?<img class="img-responsive".+?src="(.+?)"'
        else:
            sPattern = '<h2 class="heading"> *<a href="[^<>"]+?">([^<]+)<\/a>.+?<img class="img-responsive" *src="([^<]+)" *alt.+?(?:<font color="#00CC00">(.+?)<\/font>.+?)*<div class="divstreaming"> *<a href="([^<>"]+?)">'



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

            if sSearch or '/series' in sUrl:
                sTitle = aEntry[1].replace('Regarder ', '').replace('en Streaming', '')
                sUrl2 = aEntry[0]
                sThumb = aEntry[2]
                sQual = ''
            else:
                sTitle = aEntry[0]
                sThumb = aEntry[1]
                sUrl2 = aEntry[3]

                sQual = aEntry[2]
                if sQual:
                    sQual = sQual.decode("utf-8").replace(u' qualit\u00E9', '').replace('et ', '/').replace(' ', '')
                    sQual = sQual.replace('Bonne', 'MQ').replace('Haute', 'HQ').replace('Mauvaise', 'SD').encode("utf-8")

            sTitle = sTitle.decode("utf-8").replace(u'T\u00E9l\u00E9charger ', '')
            sTitle = sTitle.encode("utf-8")

            sDisplayTitle = ('%s [%s]') % (sTitle, sQual)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)

            if '/series/' in sUrl or '/series/' in sUrl2:
                oGui.addTV(SITE_IDENTIFIER, 'showSaisons', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)
            else:
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sDisplayTitle, '', sThumb, '', oOutputParameterHandler)

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
    sPattern = '<li><a href="([^<>"]+?)" class="next">Suivant &#187;<\/a><\/li>'
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return aResult[1][0]

    return False

def ReformatUrl(link):
    if '/v2/mangas' in link:
        return link
    if '/telecharger/' in link:
        return link.replace('telecharger', 'streaming')
    if '-telecharger-' in link:
        f = link.split('/')[-1]
        return '/'.join(link.split('/')[:-1]) + '/streaming/' + f.replace('-telecharger', '')
    if ('/v2/' in link) and ('/streaming/' in link):
        return link.replace('/v2/', '/')
    if '/v2/' in link:
        return link.replace('/v2/', '/streaming/')
    return link

def showSaisons():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')

    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '(?:<h2 class="heading-small">(Saison .+?)<)|(?:<li><a title=".+? \| (.+?)" class="num_episode" href="(.+?)">.+?<\/a><\/li>)'
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

            if aEntry[0]:
                oGui.addText(SITE_IDENTIFIER, '[COLOR red]' + aEntry[0] + '[/COLOR]')
            else:
                ePisode = aEntry[1].replace(',', '')
                sTitle = sMovieTitle + ' ' + ePisode
                sUrl = aEntry[2]

                oOutputParameterHandler = cOutputParameterHandler()
                oOutputParameterHandler.addParameter('siteUrl', sUrl)
                oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
                oOutputParameterHandler.addParameter('sThumb', sThumb)
                oGui.addMovie(SITE_IDENTIFIER, 'showLinks', sTitle, '', sThumb, '', oOutputParameterHandler)

        progress_.VSclose(progress_)

    oGui.setEndOfDirectory()

def showLinks():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    #refomatage url
    sUrl = ReformatUrl(sUrl)

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    if '/films' in sUrl:
        sType = 'films'
    elif 'saison' in sUrl or 'episode' in sUrl:
        sType = 'series'

    sUrl2 = sUrl.rsplit('/', 1)[1]
    idMov = re.sub('-.+', '', sUrl2)

    sPattern = '<div title="(.+?)".+?streaming="(.+?)" heberger="(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if 'VF' in aEntry[0]:
                sLang = 'VF'
            elif 'VOSTFR' in aEntry[0]:
                sLang = 'VOSTFR'
            else:
                sLang = 'VO'

            idHeb = aEntry[1]
            sHost = aEntry[2].capitalize()
            sTitle = ('%s (%s) [COLOR coral]%s[/COLOR]') % (sMovieTitle, sLang, sHost)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oOutputParameterHandler.addParameter('sType', sType)
            oOutputParameterHandler.addParameter('idMov', idMov)
            oOutputParameterHandler.addParameter('idHeb', idHeb)
            oGui.addLink(SITE_IDENTIFIER, 'showHosters', sTitle, sThumb, '', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    sType = oInputParameterHandler.getValue('sType')
    idHeb = oInputParameterHandler.getValue('idHeb')

    #film
    if (oInputParameterHandler.exist('idMov')):
        idMov = oInputParameterHandler.getValue('idMov')
        pdata = 'id=' + idHeb + '&id_movie=' + idMov + '&type=' + sType
        pUrl = 'https://libertyvf.org/v2/video.php'
    else:
        #serie pas d'idmov
        pdata = 'id=' + idHeb + '&type=' + sType
        pUrl = 'https://libertyvf.org/v2/video.php'

    oRequest = cRequestHandler(pUrl)
    oRequest.setRequestType(1)
    oRequest.addHeaderEntry('Referer', sUrl)
    oRequest.addParametersLine(pdata)
    sHtmlContent = oRequest.request()
    sHtmlContent = sHtmlContent.replace('\\', '')

    sPattern = '<iframe.+?src="(.+?)".+?"qualite":"(.+?)"'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == True):
        for aEntry in aResult[1]:

            sHosterUrl = aEntry[0]
            if sHosterUrl.startswith('//'):
                sHosterUrl = 'http:' + sHosterUrl

            sQual = aEntry[1]

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                sDisplayTitle = ('%s [%s]') % (sMovieTitle, sQual)
                oHoster.setDisplayName(sDisplayTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    else:
        #au cas ou pas de qualité
        sPattern = '<iframe.+?src="(.+?)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        if (aResult[0] == True):
            for aEntry in aResult[1]:
                sHosterUrl = aEntry
                if sHosterUrl.startswith('//'):
                    sHosterUrl = 'http:' + sHosterUrl

                oHoster = cHosterGui().checkHoster(sHosterUrl)
                if (oHoster != False):
                    oHoster.setDisplayName(sMovieTitle)
                    oHoster.setFileName(sMovieTitle)
                    cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
