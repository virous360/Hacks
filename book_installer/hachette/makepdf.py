# eggs = r'"c:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"'
import os
# for i in $(seq 1 <NB_PAGES>)
# do
#   sudo wkhtmltopdf --disable-javascript --disable-external-links --enable-local-file-access --zoom 1.7 -L 0 -R 0  "page_$i.html" "pages/page_$i.pdf"
# done
n = 1
for i in range(1,n+1):
    cmd ="wkhtmltopdf --disable-javascript --disable-external-links --enable-local-file-access --zoom 1.7 -L 0 -R 0 output\\page"+str(i)+".xhtml pages/page_"+str(i)+".pdf"
    print(cmd)
    os.system(cmd)
    print(i)