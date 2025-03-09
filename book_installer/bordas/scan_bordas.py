# Test 0.01
# Ali Naim 
# 14/3/2024

import os
import sys
import re
import requests
######################SETUP########################
SCRIPTFULLNAME = os.path.realpath(sys.argv[0])
SCRIPTPATH = os.path.dirname(SCRIPTFULLNAME)
SCRIPTNAME = os.path.basename(SCRIPTFULLNAME)
################CHANGE THIS########################
BOOKPRECAT = 1
BOOKCAT = 9
BOOKID = 8573 
BORDAS_FILLING = "2edc59852fc64cc6b917bba10061dde7bc3ed8afcf34d211f1023c3d8d708eb90a393ae50e221a32"
###################EXAMPLE#########################
# https://biblio.editions-bordas.fr/epubs/web/1e9ca049e22eec903fd69d44827b99fd4b02031c172447d04b15b5c5b8bd5b50ebe82fb331b24d5f/BORDAS/bibliomanuels/distrib_gp/1/4/3013/online/OEBPS/chapter_1/
# BOOKPRECAT = 1
# bookcat = 4
# bookid = 3013
###################################################
#https://biblio.editions-bordas.fr/epubs/web/2edc59852fc64cc6b917bba10061dde7bc3ed8afcf34d211f1023c3d8d708eb90a393ae50e221a32/BORDAS/bibliomanuels/distrib_gp/1/9/8573/online/OEBPS/Chapter_001/Images/05_04738822_PROF.jpg

def save_contents (contents : str ,file_name : str) -> None:
    with open(file_name, "w") as f :
        f.write(contents)
def error (msg : str) -> None :
    print(msg)
    exit()
def download_image(url :str, filepath : str) -> None:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"Image downloaded successfully: {filepath.split("/")[-1]}")
        else:
            print(f"Failed to download image: {url}")
    except Exception as e:
        print(f"Error downloading image: {e}")

def process_book(book_pre_cat: int, book_cat: int, book_id:int, book_filling: str, contents :str):
    print(f" -> Found book #{book_id}")
    book_dir = f"{SCRIPTPATH}/{book_pre_cat}_{book_cat}_{book_id}"
    
    print(f" -> Storage folder: {book_dir}")
    os.makedirs(book_dir, exist_ok=True)

    title_match = re.search(r'<dc:title id="title1">(.*?)</dc:title>', contents)
    if title_match:
        BOOK_TITLE = title_match.group(1)
    else:
        error("failed to get book title... out...")
    print(f"book title : {BOOK_TITLE}")

    identifier_match = re.search(r'<dc:identifier.*?>(.*?)</dc:identifier>', contents)
    if identifier_match:
        BOOK_IDENTIFIER = identifier_match.group(1)
    else:
        error("failed to get identifier... out...")
    print(f"book identifier : {BOOK_IDENTIFIER}")

    jpg_matches = list(re.findall(r'href="(.*?)/Page_(.*?)\.jpg"', contents))
    page_urls = [url[0] + "/Page_" + url[1] + ".jpg" for url in jpg_matches]
    print(f"Page List (len) : {len(page_urls)}")
    print("Content processed successfully.")


    os.makedirs(book_dir+"/Pages", exist_ok=True)
    
    for i,page in enumerate(page_urls):
        path = f"{book_dir}/Pages/Page{i}.jpg"
        link = f"https://biblio.editions-bordas.fr/epubs/web/{book_filling}/BORDAS/bibliomanuels/distrib_gp/{book_pre_cat}/{book_cat}/{book_id}/online/OEBPS/{page}"
        download_image(link,path)
def main():
    print(f"Scanning {BOOKID}")
    contents = f"https://biblio.editions-bordas.fr/epubs/web/{BORDAS_FILLING}/BORDAS/bibliomanuels/distrib_gp/{BOOKPRECAT}/{BOOKCAT}/{BOOKID}/online/OEBPS/content.opf"
    print(contents)
    res = requests.get(contents)
    if res.status_code == 200 :
        try :
            save_contents(res.text, "content.opf") # type: ignore
        except:
            print("cant save contents")
            # print(f"{res.content : 10}")
        process_book(BOOKPRECAT, BOOKCAT, BOOKID, BORDAS_FILLING,res.text)
    else : 
        print("BOOK NOT FOUND!!")
        print(res.status_code)
        print(contents)

if __name__ == "__main__":
    main()
