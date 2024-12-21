#p37
from rembg import remove
from PIL import Image
import easygui as eg
import time
from pixellib.instance import instance_segmentation
import cv2
import numpy as np

print("*"*50)
print("\nImageCraft\n")
print("*"*50)

while True:
    print("\nEnter 1:- Remove Background", "\nEnter 2:- Change Background", "\nEnter 3:- Image Segmentation", "\nEnter 4:- Exit")
    print("*"*25)
    option = int(input("Enter the option: "))
        
    if option == 1:
        print("*"*25)
        print("Select the Image")
        time.sleep(3)

        input_path = eg.fileopenbox(title='Select image file')
        input_img = Image.open(input_path)
        input_img.show()

        output = remove(input_img)
        print("Select the Folder for the Output and save in .png format")
        time.sleep(3)

        output_path = eg.filesavebox(title='Save file to..')
        #print(output_path)
        #output.save(output_path, format="PNG")
        try:
            output.save(output_path)
            print("Image saved successfully.")
        except Exception as e:
            print("Error while saving the image:", e)
        output.show()
        result = "Background removal function will be executed."
        print(result)
        print("*"*25)
        

    elif option == 2:
        print("*"*25)
        print("Select the Image")
        time.sleep(3)

        input_path = eg.fileopenbox(title='Select image file')       
        input_img = Image.open(input_path)
        input_img.show()

        output = remove(input_img)
        print("Select the Background Image")
        time.sleep(3)

        new_bgm_path = eg.fileopenbox(title='Select new image file') 
        new_bgm = Image.open(new_bgm_path)
        new_bgm.show()
        new_bgm = new_bgm.resize((input_img.width , input_img.height))
        new_bgm.paste(output, (0,0), output)

        print("Select the Folder for the Output and save in .png format")
        time.sleep(3)
        output_path = eg.filesavebox(title='Save file to..')

        #new_bgm.save(output_path, format="PNG")
        try:
            new_bgm.save(output_path)
            print("Image saved successfully.")
        except Exception as e:
            print("Error while saving the image:", e)
        new_bgm.show()
        result = "Background change function will be executed."
        print(result)
        print("*"*25)


    elif option == 3:
        print("*"*25)
        # Load the instance segmentation model
        segmenter = instance_segmentation()
        segmenter.load_model("D:/HARINI/Python/img_seg/mask_rcnn_coco.h5")

        # Perform inference on a new image
        # # Load the image for visualization
        print("*"*25)
        print("Select the Image")
        time.sleep(3)
        

        input_path = eg.fileopenbox(title='Select image file')
        input_img = cv2.imread(input_path)
        result = segmenter.segmentImage(input_path)

        # Get masks and class IDs
        masks = result[0]['masks']
        class_ids = result[0]['class_ids']

        test_point = None

        #clicked = False  # Flag to track if mouse click has occurred
        # # Function to handle mouse click events
        def mouse_click(event, x, y, flags, param):
            global test_point  # Use nonlocal to modify the test_point from outer scope
            if event == cv2.EVENT_LBUTTONDOWN:
                test_point = (x, y)
                print(f"Mouse clicked at ({x}, {y})")
                #clicked = True

        contours = []
        for i in range(masks.shape[-1]):
            mask = masks[:, :, i]
            contour, _ = cv2.findContours(mask.astype('uint8'), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours.append(contour)

        # Create a window to display the image
        cv2.namedWindow('Image')

        # Set the mouse callback function for the window
        cv2.setMouseCallback('Image', mouse_click)

        # Display the image and wait for a key press
        cv2.imshow('Image', input_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Loop through the contours and check if the point is inside
        instance_found = False
        con = None
        #if clicked:

        for i, contour in enumerate(contours):
            result = cv2.pointPolygonTest(contour[0], test_point, False)
            #print(f"Point is {'inside' if result > 0 else 'outside'} the contour {i + 1}")

            if result > 0:
                print(f"Mouse click inside contour {i + 1}")
                con = contour[0]  # Use [0] to extract the contour
        
                # Create a binary mask for the specific contour
                mask_contour = np.zeros_like(masks[:, :, 0], dtype=np.uint8)
                #cv2.drawContours(mask_contour, [con], -1, 255, thickness=cv2.FILLED)  # Use -1 for all contours
                cv2.fillPoly(mask_contour, [con], 255)  # Fill the contour with white
        
                # Invert the mask to get the background
                background_mask = np.logical_not(mask_contour)
        
                # Apply the background mask to the image
                #print("1.remove the segments \n 2. to reomve the background")
                #op=int(input("ebter the option:"))

                while True:
                    print("1.Remove the Segments \n2.To Reomve the Background")
                    op=int(input("Enter the option:"))

                    if op == 1:
                        background_img = cv2.bitwise_and(input_img, input_img, mask=background_mask.astype(np.uint8) * 255)
                        print("Save file in .png format")
                        time.sleep(3)
                        output_path = eg.filesavebox(title='Save file to..')
                        cv2.imwrite(output_path, background_img)
                        #print(f"Output image saved as {output_path}")
                        cv2.imshow("Background Image", background_img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        instance_found = True
                        print("*"*25)
                        break

                    elif op == 2:
                        instance_img = cv2.bitwise_and(input_img, input_img, mask=mask_contour.astype(np.uint8) * 255)
                        print("Save file in .png format")
                        time.sleep(3)
                        output_path = eg.filesavebox(title='Save file to..')
                        cv2.imwrite(output_path, instance_img)
                        #print(f"Output image saved as {output_path}")
                        cv2.imshow("Instance Image", instance_img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                        instance_found = True
                        print("*"*25)
                        break 

                    else:
                        print("Enter the above option") 
                        print("*"*25)

        if not instance_found:
            all_contours_mask = np.zeros_like(masks[:, :, 0], dtype=np.uint8)
            for contour in contours:
                con = contour[0]
                mask_contour = np.zeros_like(masks[:, :, 0], dtype=np.uint8)
                cv2.drawContours(mask_contour, [con], -1, 255, thickness=cv2.FILLED)
                all_contours_mask = cv2.bitwise_or(all_contours_mask, mask_contour)

            segment_mask = np.logical_not(all_contours_mask)

            image_with_instances_removed = cv2.bitwise_and(input_img, input_img, mask=segment_mask.astype(np.uint8) * 255)

            print("save file in png format")
            output_path = eg.filesavebox(title='Save file to..')
            cv2.imwrite(output_path, image_with_instances_removed)
            #print(f"Output image saved as {output_path}")
            cv2.imshow("Image with Instances Removed", image_with_instances_removed)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


    elif option == 4 :
        print("*"*25)
        print("THANK YOU!!!")
        print("VISIT AGAIN")
        print("*"*25)
        break
        
    else:
        print("*"*25)
        result = "Select an option from the Above."
        print(result)
        print("*"*25)