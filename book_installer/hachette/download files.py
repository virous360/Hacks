import wget
# from makepdf import xhtml_to_pdf
# from pywebcopy import save_webpage
# setup
Iban = "9782401058729"
# page_max = 327
page_max = 324
output_path = "D:\\me\\books\\book_installer\\hachette\\output"  # temp


# img_p1 = "https://exobank.hachette-livre.fr/contents/final/"+Iban+"-fxl/OEBPS/images/img-"
# # img_p2 = "-1.jpg"
# out_img = "images/img-"+i+"-1.jpg"
# "https://exobank.hachette-livre.fr/contents/final/<IBAN>-fxl/OEBPS/fonts/font-[0-<NB_FONTS>].otf" -o "fonts/font-#1.otf"
# font_p1 = "https://exobank.hachette-livre.fr/contents/final/"+Iban+"-fxl/OEBPS/fonts/font-"
# font_p2 = ".otf"
# def url(num: int):
#     return website_p1 + str(num) + website_p2


# print(url(1))
for i in range(1, page_max+1):
  website = "https://exobank.hachette-livre.fr/contents/final/" +\
    Iban+"-fxl/OEBPS/page"+str(i)+".xhtml?interface=postMessage"
  image = "https://exobank.hachette-livre.fr/contents/final/" +\
    Iban+"-fxl/OEBPS/images/img-"+str(i)+"-1.jpg"
  font = "https://exobank.hachette-livre.fr/contents/final/" +\
    Iban+"-fxl/OEBPS/fonts/font-"+str(i)+".otf"
  wget.download(website, output_path)
  wget.download(image, output_path+"\\images\\")
  wget.download(font, output_path+"\\fonts\\")
  # xhtml_to_pdf(output_path + "\\page" + str(i)+".xhtml", i)
  print("done page "+str(i))
