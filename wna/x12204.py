

def mifunc1(v1, *args, **kwargs):
    print(v1)
    print(args)
    print(kwargs)
    
def mifunc2(v1, **kwargs):
    print(v1)
    print(kwargs)


if __name__ == '__main__':
    
    kw = {}
    vv = 'paicod_contains'
    kw[vv] = 'ES'
    vv = 'painom_startswith'
    kw[vv] = 'FR'    
    
    mifunc1(1, 2, 3, 4, **kw)
    
    
    
##    latitud = 41.644059
#    latitud = abs(-0.969922)
#
##    retval = grados + minutos / 60 + segundos / 3600
#        
#    grados = int(latitud)
#    latitud -= grados
#    minutos = int(latitud * 60)
#    latitud -= minutos / 60
#    segundos = int(round(latitud * 3600, 0))
#    
#    
#    print("%d %d %d %f" % (grados, minutos, segundos, latitud))
#    
#    s = '{:03d}{:02d}{:02d}'.format(grados, minutos, segundos)
#    print(s)