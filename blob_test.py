"""
Prototyping for phone tracking with specific color-based markers.

@author: Elias Gabriel and Duncan Mazza
@revision: v1.1
"""
import cv2
import cam_classes as cl

if __name__ == "__main__":
    camera = cl.CamReader()
    while True:
        frame = camera.get_frame()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
