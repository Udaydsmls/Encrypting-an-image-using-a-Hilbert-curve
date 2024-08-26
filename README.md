# Securing-Images-from-Cryptotext-using-DWT-and-Hilbert-Curve

## The idea behind the project is to convert an image file to text file using a Hilbert curve while also removing any steganography from the image.

### An illustration of how the Hilbert curve is used to encrypt the image.

![image](https://github.com/user-attachments/assets/80217da6-aa8c-460f-aba1-9415a35c8d14)

![image](https://github.com/user-attachments/assets/77a4c2f9-8053-4533-a513-00fd423f6bc1)

### With this method, we now convert the image into a text file. The contents of the text file would be as shown.
![image](https://github.com/user-attachments/assets/fb380b9b-2ee1-448a-b4b0-fd5f5768a64a)
Obviously, the text file doesn't make much sense and does a pretty good job of hiding the image.

### There is also a function to remove any steganography from the image; this is done using DWT.
The only issue with this is that it works best on black-and-white images. If applied to a color image, it would lose the red spectrum.

### Decrypting the image from the text file
It is as simple as encrypting the image. The only parameters you need are the original dimensions of the image and the key used in the encryption process.


## Developing Further on this Concept
1) Currently, the key only works by rotating the pixels of the image, making it look blurry but not hiding anything. This can be improved by implementing a better method to shuffle the image pixels.
2) There are many space-filling curves similar to the Hilbert curve that can be implemented.
3) Currently, the image is converted to a plain text file, and that’s it. However, there may be a way to further encrypt the text file.
