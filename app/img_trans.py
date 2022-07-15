import base64

def image_encoder(image_path: str) -> str: #enocde video or image to string
    img = open(image_path,"rb")
    img_encode = base64.b64encode(img.read())
    img.close()
    img_string = img_encode.decode('utf-8')
    return img_string

def image_decoder(encoded_image: str, save_path: str = "write.png"): #decode string from encoder
    img_encode = encoded_image.encode('utf-8')
    img = base64.b64decode(img_encode)
    out = open(save_path,"wb")
    out.write(img)
    out.close()



if __name__ == '__main__':
    print("Testing file image encoder and decoder...")

    img_str = image_encoder("frontend\static\images\demo-ieda\Macbook\Apple-flow.MOV")
    image_decoder(img_str,'write.mp4')

    #img_str = image_encoder("frontend\static\images\logo.jpg")
    #image_decoder(img_str)

    '''
    img = open("frontend\static\images\logo.jpg","rb")
    #print(len(img.read()))

    img_encode = base64.b64encode(img.read())
    img.close()
    print(type(img_encode))
    print(len(img_encode))

    img_string_encode = img_encode.decode('utf-8')
    print(type(img_string_encode))
    print(len(img_string_encode))

    img_string_decode = img_string_encode.encode('utf-8')
    print(type(img_string_decode))
    print(len(img_string_decode))

    img_decode = base64.b64decode(img_string_decode)
    print(type(img_decode))
    print(len(img_decode))

    out = open("write.jpg","wb")
    out.write(img_decode)
    out.close()
    '''





