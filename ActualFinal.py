import PIL
import matplotlib.pyplot as plt # single use of plt is commented out
import os.path  
import PIL.ImageDraw            

def frame(original_image, color, frame_width):
    """Places a frame around a PIL.Image and adds text
    
    original_image must be a PIL.Image
    Returns a new PIL.Image with frame, where
    0 < frame_width < 1
    is the frame width as a portion of the shorter dimension of original_image
    """
    #set the width of the frame
    #sets things needed to add frame and text in certain spots
    width, height = original_image.size
    thickness = int(frame_width * min(width, height)) # thickness in pixels
    half_mid = int(width/4)
    down = int(height* 0.9)
    ###
    #create a mask
    ###
    
    #start with alpha = 0 mask
    r, g, b =color
    frame_mask = PIL.Image.new('RGBA', (width, height), (0,0,0,0))
    drawing_layer = PIL.ImageDraw.Draw(frame_mask)
    
    #draw 2 rectangles that make up a frame like border on two sides
    drawing_layer.rectangle((0,0,width,thickness), fill=(255,215,0,255))
    drawing_layer.rectangle((0,0,thickness,height), fill=(255,215,0,255))
    #draw triange in corner to change up the "traditional" frame style
    drawing_layer.polygon(((0,0),(0,thickness*3),(thickness*3,0)), fill=(255,215,0,255))
    #adds text to the image with font style "AdobeClean-It" and size 50 pixels using truetype attribute
    #places font at xy coordinate that is 1/4 across the image horizontally and 9/10 of the way down the image vertically
    text = "Family Name"
    font = PIL.ImageFont.truetype("AdobeClean-It.ttf",50)
    drawing_layer.text((half_mid, down), text, fill=(255,215,0,255), font=font)
   
    # Make the new image
    result = original_image.copy()
    result.paste(frame_mask, (0,0), mask=frame_mask)
    return result
    
def get_images(directory=None):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors tying to open non-images
    return image_list, file_list

def frame_all_images(directory=None, color=(255,0,0), width=0.10):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and frame and text.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    # Load all the images
    image_list, file_list = get_images(directory)  
    
    # Go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        print n
        filename, filetype = file_list[n].split('.')
        
        # Frame and add text to images

        new_image = frame(image_list[n], color, width) 
        
        # Save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename + '.png')
        new_image.save(new_image_filename)    