import requests
# import wget
import json
import os

headers = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NDBhZDlkNTkzN2MzYjNiY2ZjNDU5YzUiLCJ0cmFja2luZ0lkIjoiNmM3N2NlMmUtY2FmMC00ODkwLWEzOTUtYjBhMDYyNjg3MWNlIiwicHJvZmlsZVR5cGUiOiJzdHVkZW50IiwiY3JlYXRlZEF0IjoiMjAyNC0wOC0xNFQxOTo1MTo1My4wMDBaIiwiaWF0IjoxNzIzNjY1MTEzLCJleHAiOjE3MjM2NzIzMTN9.MbVCZcWVDl0TX9eK18ePmrPMgM9nTN8X7HPhACW3Y4A"
}

def down_pdf(url : str,path:str) -> None :
    r = requests.get(url)
    with open(path,"wb") as f:
        f.write(r.content)

def down_list_of_chp(slug : str) -> str:
    url = f"https://www.schoolmouv.fr/eleves/api/resources/cours/{slug}/fiche-de-cours/pdf"
    return requests.get(url, headers=headers).text

def extract_data_json(data_unfiltered : str) -> dict[str,list[str]]:
    data = json.loads(data_unfiltered)
    #[0]["sheets"]
    # closed file
    # print(data)
    chp = {}
    for chapter_blob in data :
        code_friendly_name = chapter_blob["name"].replace(" ", "-").replace("<", "").replace(">","").replace(":","").replace('"',"").replace("/","").replace("\\","").replace("|","").replace("?","").replace("*","")
        chp[code_friendly_name] = []
        sheets = chapter_blob["sheets"]
        for notion in sheets :
            #verification (availability)
            resource_types = []
            for resource in notion["resources_list"]:
                if resource["is_published"] :
                    resource_types.append(resource["resource_type"])
                else : 
                    print(f"cant add {notion["slug"]} : is not published yet")

            if resource_types.count("Fiche de cours") >= 1 :
                chp[code_friendly_name].append(notion["slug"])
            # else: 
                # print(f"cant add {chapter_blob["slug"]} : resource cour is missing")    
    return chp

def get_json(chapter_index_id) -> str:
    url = f"https://www.schoolmouv.fr/eleves/api/chapters-indexes/{chapter_index_id}/chapters"
    return requests.get(url, headers=headers).text

def get_ID(subject_id):
    url = f"https://www.schoolmouv.fr/eleves/api/menus/{subject_id}"
    r = requests.get(url, headers=headers).text
    # print(r)
    data = json.loads(r)["list"]
    id = []
    for menu in data :
        if menu["name"] == "Programme":
            id.append(menu["chapterIndexId"])
    return id

def get_subject_id(class_id) -> list[dict[str,str]] :
    with open("matieres.json", "r") as f:
        data = json.loads(f.read())["subjects"]
    valid = []
    for subject in data:
        if subject["degree_id"] == class_id:
            Usefull_data = {
                "slug" : subject["slug"],
                "subject_id" : subject["id"],
                "chapter_indexes_list" : subject["chapter_indexes_list"]
            }
            valid.append(Usefull_data)
    return valid

def get_class_id() -> tuple[str,int]:
    class_chosen = int(input("\n1. seconde\n2. 1ere\n3. terminal\n:"))
    if class_chosen == 1 :
        return ("5cd020daafd5f7d98fa4ca91",1)
    elif class_chosen == 2 :
        return ("5cd020dbafd5f7d98fa4ca92",2)
    else :
        return ("5cd020dbafd5f7d98fa4ca93",3)

def main():
    with open("done.json", "r") as s :
        done = json.loads(s.read())
    # ask = True
    DOWNLOAD_LOCATION = "./"
    # rip 
    class_input = get_class_id()
    class_id = class_input[0]
    if class_input[1] == 1 :
        os.makedirs("seconde",exist_ok=True)
        DOWNLOAD_LOCATION += "seconde/"
        print("You chose : seconde")
    elif class_input[1] == 2:
        os.makedirs("premiere",exist_ok=True)
        DOWNLOAD_LOCATION += "premiere/"
        print("You chose : premiere")
    else :
        os.makedirs("terminal",exist_ok=True)
        DOWNLOAD_LOCATION += "terminal/"
        print("You chose : terminal")
    # print(DOWNLOAD_LOCATION)
    print("-"*32)
    subject_id = get_subject_id(class_id)
    
    for subject in subject_id :
        if done[DOWNLOAD_LOCATION].count(subject["slug"]) == 0 :
            print("-"*32)
            print(f"Subject : {subject["slug"]}")
            # print(f"Subject_id : {subject["subject_id"]}")
            # chapters = subject["chapter_indexes_list"]
            chapters = get_ID(subject["subject_id"])
            if len(chapters) != 0 :
                print(f"getting list of chapters : {chapters}")
                raw = get_json(chapters[0])
                filtered = extract_data_json(raw)
                print(filtered)
                if filtered != [] :
                    # print("not emmpty!!")
                    for chp in filtered:
                        for pdf in filtered[chp] : 
                            if os.path.exists(f"{DOWNLOAD_LOCATION}{subject["slug"]}/{chp}/{pdf[:92]}.pdf"):
                                print(f"file already exits (skipping) : {chp}/{pdf}")
                            else:   
                                print(f"Downloading : {subject["slug"]} -> {chp} -> {pdf}")
                                url = down_list_of_chp(pdf)
                                os.makedirs(f"{DOWNLOAD_LOCATION}{subject["slug"]}/{chp}/",exist_ok=True)
                                down_pdf(url, f"{DOWNLOAD_LOCATION}{subject["slug"]}/{chp}/{pdf[:92]}.pdf")
                                print("Done!")
            with open("done.json", "w") as s :
                done[DOWNLOAD_LOCATION].append(subject["slug"])
                s.write(json.dumps(done))
        else  :
            print(f"{subject['slug']} is already done (skipping)")

        
    # print(subject_id)

# down_pdf("https://www.learningcontainer.com/wp-content/uploads/2019/09/sample-pdf-file.pdf","./premiere/sample-pdf.pdf")
main()
# get_ID("5cd020dbafd5f7d98fa4ca93")