

if __name__ == '__main__':
#    latitud = 41.644059
    latitud = abs(-0.969922)

#    retval = grados + minutos / 60 + segundos / 3600
        
    grados = int(latitud)
    latitud -= grados
    minutos = int(latitud * 60)
    latitud -= minutos / 60
    segundos = int(round(latitud * 3600, 0))
    
    
    print("%d %d %d %f" % (grados, minutos, segundos, latitud))
    
    s = '{:03d}{:02d}{:02d}'.format(grados, minutos, segundos)
    print(s)