1. Find the book IBAN

In my case, it is `9782017092605`

2. Go to the Educadhoc demo for this IBAN

(replace <IBAN> with the book IBAN)
https://demo.educadhoc.fr/reader/textbook/<IBAN>/fxl/Page_1?feature=freemium
  
3. Execute these commands

```sh
  curl "https://exobank.hachette-livre.fr/contents/final/<IBAN>-fxl/OEBPS/Page_[1-<NB_PAGES>].html?interface=postMessage" -o "page_#1.html"   
  curl "https://exobank.hachette-livre.fr/contents/final/<IBAN>-fxl/OEBPS/images/img-[1-<NB_PAGES>]-1.jpg" -o "images/img-#1-1.jpg"  
  curl "https://exobank.hachette-livre.fr/contents/final/<IBAN>-fxl/OEBPS/fonts/font-[0-<NB_FONTS>].otf" -o "fonts/font-#1.otf"  
```

Execute this script to turn the pages into PDFs
```sh 
for i in $(seq 1 <NB_PAGES>)
do
  sudo wkhtmltopdf --disable-javascript --disable-external-links --enable-local-file-access --zoom 1.7 -L 0 -R 0  "page_$i.html" "pages/page_$i.pdf"
done
```
  
Fuse all the pages:

```sh
pdftk page_*.pdf cat output full_book.pdf
```

And compress the resulting file:

```sh
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/prepress -dNOPAUSE -dQUIET -dBATCH -sOutputFile=compressed_book.pdf full_book.pdf      
```