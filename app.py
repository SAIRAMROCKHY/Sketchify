import streamlit as st
from PIL import Image
import numpy as np
import cv2
from io import BytesIO

def convert_to_watercolor_sketch(inp_img):
    try:
        img_np = np.array(inp_img)
        img_1 = cv2.edgePreservingFilter(img_np, flags=2, sigma_s=50, sigma_r=0.8)
        img_water_color = cv2.stylization(img_1, sigma_s=100, sigma_r=0.5)
        return img_water_color
    except Exception as e:
        print(f"Error in convert_to_watercolor_sketch: {e}")
        return None

def convert_to_pencil_sketch(inp_img):
    try:
        img_np = np.array(inp_img)
        img_pencil_sketch, _ = cv2.pencilSketch(img_np, sigma_s=50, sigma_r=0.07, shade_factor=0.0825)
        return img_pencil_sketch
    except Exception as e:
        print(f"Error in convert_to_pencil_sketch: {e}")
        return None

def load_image(image):
    img = Image.open(image)
    return img

def main():
    st.title('WEB APPLICATION TO CONVERT IMAGE TO SKETCH')
    st.write("This is an application for converting your image to a Watercolor Sketch or Pencil Sketch")
    st.subheader("Please Upload Your Image")
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        option = st.selectbox('How would you like to convert the image',
                              ('Convert to Watercolor Sketch', 'Convert to Pencil Sketch'))
        if option == 'Convert to Watercolor Sketch':
            image = Image.open(image_file)
            final_sketch = convert_to_watercolor_sketch(image)
            if final_sketch is not None:
                im_pil = Image.fromarray(final_sketch)
                col1, col2 = st.columns(2)
                with col1:
                    st.header("Original Image")
                    st.image(load_image(image_file), width=250)
                with col2:
                    st.header("Watercolor Sketch")
                    st.image(im_pil, width=250)
                    buf = BytesIO()
                    im_pil.save(buf, format='JPEG')
                    byte_im = buf.getvalue()
                    st.download_button(label='Download Image', data=byte_im,
                                       file_name='watercolor_sketch.jpg', mime='image/jpeg')
        elif option == 'Convert to Pencil Sketch':
            image = Image.open(image_file)
            final_sketch = convert_to_pencil_sketch(image)
            if final_sketch is not None:
                im_pil = Image.fromarray(final_sketch)
                col1, col2 = st.columns(2)
                with col1:
                    st.header("Original Image")
                    st.image(load_image(image_file), width=250)
                with col2:
                    st.header("Pencil Sketch")
                    st.image(im_pil, width=250)
                    buf = BytesIO()
                    im_pil.save(buf, format='JPEG')
                    byte_im = buf.getvalue()
                    st.download_button(label='Download Image', data=byte_im,
                                       file_name='pencil_sketch.jpg', mime='image/jpeg')

if __name__ == '__main__':
    main()
