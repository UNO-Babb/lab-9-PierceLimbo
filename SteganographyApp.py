#Lab 9
#Pierce Limbo
#11/4/2025

from PIL import Image
import os

def encode(img, msg):

    if len(msg) > 255:
        raise ValueError("Message too long for 1-byte header. Max 255 characters.")

    pixels = img.load()  
    width, height = img.size
    total_pixels = width * height

    required_pixels = 1 + 3 * len(msg)
    if required_pixels > total_pixels:
        raise ValueError(f"Image too small. Need {required_pixels} pixels, have {total_pixels}.")

    r, g, b = pixels[0, 0]
    pixels[0, 0] = (len(msg), g, b)  

    letterSpot = 0       
    pixel_index = 1       
    letterBinary = ""

    for i in range(len(msg) * 3):
        idx = pixel_index
        x = idx % width
        y = idx // width

        red, green, blue = pixels[x, y]
        redBinary = numberToBinary(red)
        greenBinary = numberToBinary(green)
        blueBinary = numberToBinary(blue)


        if i % 3 == 0:
            letterBinary = numberToBinary(ord(msg[letterSpot]))

            greenBinary = greenBinary[:7] + letterBinary[0]
            blueBinary  = blueBinary[:7]  + letterBinary[1]
        elif i % 3 == 1:
            redBinary   = redBinary[:7]   + letterBinary[2]
            greenBinary = greenBinary[:7] + letterBinary[3]
            blueBinary  = blueBinary[:7]  + letterBinary[4]
        else:
            redBinary   = redBinary[:7]   + letterBinary[5]
            greenBinary = greenBinary[:7] + letterBinary[6]
            blueBinary  = blueBinary[:7]  + letterBinary[7]
            letterSpot += 1  
          
        red   = binaryToNumber(redBinary)
        green = binaryToNumber(greenBinary)
        blue  = binaryToNumber(blueBinary)
        pixels[x, y] = (red, green, blue)

        pixel_index += 1  

    img.save("secretImg.png", "PNG")


def decode(img):
    msg = ""
    pixels = img.load()
    width, height = img.size

    red, green, blue = pixels[0, 0]
    msgLength = red 

    letterBinary = ""
    pixel_index = 1  

    while len(msg) < msgLength:
        x = pixel_index % width
        y = pixel_index // width

        r, g, b = pixels[x, y]
        rB = numberToBinary(r)
        gB = numberToBinary(g)
        bB = numberToBinary(b)

        mod = (pixel_index - 1) % 3 
        if mod == 0:
            letterBinary = gB[7] + bB[7]
        elif mod == 1:
            letterBinary += rB[7] + gB[7] + bB[7]
        else:
            letterBinary += rB[7] + gB[7] + bB[7]
            letterAscii = binaryToNumber(letterBinary)
            msg += chr(letterAscii)
            letterBinary = "" 

        pixel_index += 1

    return msg


# ---------- Helper functions ----------

def numberToBinary(num):
    if not (0 <= num <= 255):
        raise ValueError("numberToBinary expects a value in 0..255")
    bits = []
    n = num
    for _ in range(8):
        bits.append(str(n & 1))
        n >>= 1
    bits.reverse()
    return "".join(bits)

def binaryToNumber(bin_str):
    total = 0
    for c in bin_str:
        total = (total << 1) | (1 if c == '1' else 0)
    return total


def main():
    myImg = Image.open('pki.png').convert('RGB')
    myMsg = "This is a secret message I will hide in an image."
    encode(myImg, myMsg)
    myImg.close()



if __name__ == '__main__':
    main()
