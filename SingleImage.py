import pypylon
from matplotlib.pyplot import figure,draw,pause
#
Nblock = 10  # TODO workaround for Basler too many frames error
Nblocks = 100  # arbitrary number of frames to plot

def connect(camdev,camind=0):
    

    cam = pypylon.factory.create_device(camdev[camind])

    cam.open()

    return cam

def simpleloop(cams):

    cam = connect(cams) 

    print('exposure time [millisec]:',cam.properties['ExposureTime']/1e3)
    # cam.properties['ExposureTime'] = 1000

    # cam.properties['DeviceLinkThroughputLimitMode'] = 'On'

    # %% movie
    ax = figure().gca()
    h = ax.imshow(list(cam.grab_images(1))[0])  # TODO workaround for grab_image() broken
    ht = ax.set_title('')
    cam.close()

    for i in range(Nblocks):

        cam = connect(cams,0)

        for j,I in enumerate(cam.grab_images(Nblock)):  # grab_images argument is how many images to yield
            h.set_data(I)
            ht.set_text('Image # {} / {}'.format(i*Nblock+j,Nblocks*Nblock))
            draw(); pause(0.01)

        cam.close()


if __name__ == '__main__':

    print('Basler Pylon API version:',pypylon.pylon_version.version)

    cams = pypylon.factory.find_devices()
    print(cams)

    simpleloop(cams)
