import urllib.request
from num2words import num2words

link=['https://play-lh.googleusercontent.com/XCXQfaY8FkZidwyjwDbbWA1fvTt4CLrN6Xz9iSNQDDne9Wvt2uZidZUC9-fjyDpXLOA',
'https://play-lh.googleusercontent.com/G1PXN1ou15czZr44yXtVCUccszsBX5Zvm_f9Ax51Q_wduMbVgveHjkecMCzLc55sr6Y',
'https://play-lh.googleusercontent.com/Xul-hqlyeN9PQv9jKXFOhdE-89pdY2xiytSoR_tqzjJJPh6Ar3OyDiXO5luolBRpEgs']

#for download requires name and link
for i in range(len(link)):
    #converts the number of image into words 
    inttoword=num2words(i)
    #adds the extension
    exten='/mnt/c/xampp/htdocs/appimages/' + inttoword +'.png'
    #downloads it using the two things names and links for each image
    urllib.request.urlretrieve(link[i],exten)
    #store in another db column taking the link from localhost
    print(exten)

