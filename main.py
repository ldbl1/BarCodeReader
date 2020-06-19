from __future__ import print_function
import pyzbar.pyzbar as pyzbar
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import io

def decode(im) : 
  # Find barcodes and QR codes
  decodedObjects = pyzbar.decode(im)

  # Print results
  for obj in decodedObjects:
    print('Type : ', obj.type)
    print('Data : ', obj.data,'\n')
    
  return decodedObjects


# Display barcode and QR code location  
def display(im, decodedObjects):

  # Loop over all decoded objects
  for decodedObject in decodedObjects: 
    points = decodedObject.polygon

    # If the points do not form a quad, find convex hull
    if len(points) > 4 : 
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else : 
      hull = points
    
    # Number of points in the convex hull
    n = len(hull)

    # Draw the convext hull
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

  # Display results 
  cv2.imshow("Results", im)
  cv2.waitKey(0)


class App(tk.Tk):
    def __init__(self):
        super().__init__()  # options=(tk.Menu,))
        self.menubar = tk.Menu()
        self.config(menu=self.menubar)
        self.menubar.add_command(label='paste', command=self.on_paste)

        self.label = tk.Label(self, text="CLIPBOARD image", font=("David", 18),
                              image='', compound='center')
        self.label.grid(row=0, column=0, sticky='w')

    def on_paste(self):
        self.label.configure(image='')
        self.update_idletasks()

        try:
            b = bytearray()
            h = ''
            for c in self.clipboard_get(type='image/png'):
                if c == ' ':
                    try:
                        b.append(int(h, 0))
                    except Exception as e:
                        print('Exception:{}'.format(e))
                    h = ''
                else:
                    h += c

        except tk.TclError as e:
            b = None
            print('TclError:{}'.format(e))
        finally:
            if b is not None:
                with Image.open(io.BytesIO(b)) as img:
                    print('{}'.format(img))
                    self.label.image = ImageTk.PhotoImage(img.resize((100, 100), Image.LANCZOS))
                    self.label.configure(image=self.label.image)
  
# Main 
if __name__ == '__main__':

  # Read image
  im = cv2.imread('zbar-test.jpg')

  decodedObjects = decode(im)
  display(im, decodedObjects)
