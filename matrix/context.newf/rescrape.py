import sys
import xbmc

if __name__ == '__main__':
    item = sys.listitem
    message = item.getLabel()
    path = item.getPath()

    path = path.replace('getSources', 'getSources&newf_reload=true')
    path = path.replace('smartPlay', 'getSources&newf_reload=true')

    xbmc.executebuiltin('PlayMedia(%s)' % path)
