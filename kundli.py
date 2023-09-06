import os
import json
import datetime
from AstroKundli import GKundli
from PIL import Image, ImageDraw, ImageFont

name = input("Enter Name: ").strip()
year = int(input("Year: "))
month = int(input("Month: "))
day = int(input("Day: "))
hour = int(input("Hour: "))
minute = int(input("Minute: "))
utc = input("UTC: ").strip("+")
latitude = float(input("Latitude: ").strip("E N °"))
longitude = float(input("Longitude: ").strip("E N °"))

navamasa_mfd = {
            "move": [1,4,7,10],
            "fixed": [2,5,8,11],
            "dual": [3,6,9,12]
        }
navamasa_degree = [
    [ 0,   3.2, 6.4, 10  , 13.2, 16.4, 20  ,  23.2, 26.4 ],
    [ 3.2, 6.4, 10,  13.2, 16.4, 20  , 23.2,  26.4, 30   ]
]

def get_moon_chart(lagnaKundli):
    houses = {
        "1":{"sign_num":0, "asc":None, "planets":[]},
        "2":{"sign_num":0, "asc":None, "planets":[]},
        "3":{"sign_num":0, "asc":None, "planets":[]},
        "4":{"sign_num":0, "asc":None, "planets":[]},
        "5":{"sign_num":0, "asc":None, "planets":[]},
        "6":{"sign_num":0, "asc":None, "planets":[]},
        "7":{"sign_num":0, "asc":None, "planets":[]},
        "8":{"sign_num":0, "asc":None, "planets":[]},
        "9":{"sign_num":0, "asc":None, "planets":[]},
        "10":{"sign_num":0, "asc":None, "planets":[]},
        "11":{"sign_num":0, "asc":None, "planets":[]},
        "12":{"sign_num":0, "asc":None, "planets":[]}
    }
    first_house = 0
    for item in lagnaKundli:
        if len(lagnaKundli[item]["planets"]) != 0 and "Mo" in lagnaKundli[item]["planets"]:
            first_house = lagnaKundli[item]["sign_num"]
            break
    
    houses["1"]["sign_num"] = first_house
    for i in range(2,13):
        first_house += 1
        if first_house > 12:
            first_house = 1
        houses[str(i)]["sign_num"] = first_house
        if houses[str(i)]["sign_num"] == lagnaKundli["1"]["sign_num"]:
            houses[str(i)]["asc"] = lagnaKundli["1"]["asc"]
    
    for item in lagnaKundli:
        if len(lagnaKundli[item]["planets"]) != 0:
            for house in houses:
                if houses[house]["sign_num"] == lagnaKundli[item]["sign_num"]:
                    for planet in lagnaKundli[item]["planets"]:
                        houses[house]["planets"].append(planet)
    return houses
    
def get_start_count(sign_num, pos, current_house):
    if sign_num in navamasa_mfd["move"]:
        start_house = current_house
        for i in range(len(navamasa_degree[0])):
            if pos >= navamasa_degree[0][i] and pos <= navamasa_degree[1][i]:
                house_to_count = i+1
                current_house = start_house+house_to_count
                return [start_house+1, house_to_count]
    elif sign_num in navamasa_mfd["fixed"]:
        start_house = 9+current_house if 9+current_house <= 12 else 9+current_house-12 
        for i in range(len(navamasa_degree[0])):
            if pos >= navamasa_degree[0][i] and pos <= navamasa_degree[1][i]:
                house_to_count = i+1
                current_house = start_house+house_to_count
                return [start_house, house_to_count]
    elif sign_num in navamasa_mfd["dual"]:
        start_house = 5+current_house if 5+current_house <= 12 else 5+current_house-12
        for i in range(len(navamasa_degree[0])):
            if pos >= navamasa_degree[0][i] and pos <= navamasa_degree[1][i]:
                house_to_count= i+1
                current_house = start_house+house_to_count
                return [start_house, house_to_count]
        

def navamsaChart(kundli):
    asc = [int(kundli["1"]["sign_num"]),   float(kundli["1"]["asc"][1]
                                                    +kundli["1"]["asc"][2]+"."+kundli["1"]["asc"][4]
                                                    +kundli["1"]["asc"][5]) ]
    houses = {
        "1":{"sign_num":1, "asc":kundli["1"]["asc"], "planets":[]},
        "2":{"sign_num":2, "planets":[]},
        "3":{"sign_num":3, "planets":[]},
        "4":{"sign_num":4, "planets":[]},
        "5":{"sign_num":5, "planets":[]},
        "6":{"sign_num":6, "planets":[]},
        "7":{"sign_num":7, "planets":[]},
        "8":{"sign_num":8, "planets":[]},
        "9":{"sign_num":9, "planets":[]},
        "10":{"sign_num":10, "planets":[]},
        "11":{"sign_num":11, "planets":[]},
        "12":{"sign_num":12, "planets":[]}
    }
    count_house = get_start_count(asc[0], asc[1], 1-1)
    temp = count_house[0]-1
    for _ in range(count_house[1]):
        temp += 1
        if temp > 12:
            temp = 1
    
    for i in range(12):
        houses[str(i+1)]["sign_num"] = kundli[str(temp)]["sign_num"]
        temp += 1
        if temp > 12:
            temp = temp-12
    
    for house in kundli:
        if len(kundli[house]["planets"]) != 0:
            for item in kundli[house]["planets"]:
                count_house = get_start_count(kundli[house]["sign_num"], float(kundli[house]["planets"][item][1]
                                                                                    +kundli[house]["planets"][item][2]+"."+kundli[house]["planets"][item][4]
                                                                                    +kundli[house]["planets"][item][5]   ), int(house)-1)
                temp = count_house[0]-1
                for _ in range(count_house[1]):
                    temp += 1
                    if temp > 12:
                        temp = 1
                
                rashi = kundli[str(temp)]["sign_num"]
                for i in houses:
                    if houses[i]["sign_num"] == rashi:
                        houses[i]["planets"].append(item)
    return houses

def write_to_image(kundli, image_pos, kundli_img, output, mode):
    if mode == 0:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"LagnaKundli-"+name+"-"+time+".png")
    elif mode == 1:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"Transit-"+name+"-"+time+".png")
    elif mode == 2:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"Navamasa-"+name+"-"+time+".png")
    elif mode == 3:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"Moon-"+name+"-"+time+".png")
    
    img = Image.open(kundli_img)
    font_sign   = ImageFont.truetype("arial.ttf", 24)
    font_planet = ImageFont.truetype("arial.ttf", 26)
    draw = ImageDraw.Draw(img)
    house = 1
    if mode == 0:
        for item in image_pos:
            draw.text(image_pos[item]["sign_pos"], str(kundli[str(house)]["sign_num"]), (0,0,0), font=font_sign)
            temp = 0
            if house == 1 and len(kundli[str(house)]["asc"]) != 0:
                draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), "Asc", (0,0,0), font=font_planet)
                temp += 30
            if len(kundli[str(house)]["planets"]) != 0:
                for planet in kundli[str(house)]["planets"]:
                    draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), planet, (0,0,0), font=font_planet)
                    temp += 30
            house += 1
    elif mode == 1:
        for item in image_pos:
            draw.text(image_pos[item]["sign_pos"], str(kundli[str(house)]["sign_num"]), (0,0,0), font=font_sign)
            temp = 0
            if kundli[str(house)]["asc"] != None:
                draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), "Asc", (0,0,0), font=font_planet)
                temp += 30
            if len(kundli[str(house)]["planets"]) != 0:
                for planet in kundli[str(house)]["planets"]:
                    draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), planet, (0,0,0), font=font_planet)
                    temp += 30
            house += 1
    elif mode == 2:
        for item in image_pos:
            draw.text(image_pos[item]["sign_pos"], str(kundli[str(house)]["sign_num"]), (0,0,0), font=font_sign)
            temp = 0
            if house == 1 and len(kundli[str(house)]["asc"]) != 0:
                draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), "Asc", (0,0,0), font=font_planet)
                temp += 30
            if len(kundli[str(house)]["planets"]) != 0:
                for planet in kundli[str(house)]["planets"]:
                    draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), planet, (0,0,0), font=font_planet)
                    temp += 30
            house += 1
    elif mode == 3:
        for item in image_pos:
            draw.text(image_pos[item]["sign_pos"], str(kundli[str(house)]["sign_num"]), (0,0,0), font=font_sign)
            temp = 0
            if kundli[str(house)]["asc"] != None:
                draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), "Asc", (0,0,0), font=font_planet)
                temp += 30
            if len(kundli[str(house)]["planets"]) != 0:
                for planet in kundli[str(house)]["planets"]:
                    draw.text((image_pos[item]["planet_pos"][0], image_pos[item]["planet_pos"][1]+temp), planet, (0,0,0), font=font_planet)
                    temp += 30
            house += 1
    img.save(out)
    print("[*]Saved: ", out)

def write_to_file(filename, kundli, mode):
    if mode == 0:
        with open(filename, "a") as opn:
            opn.write("Birth Kundli\n")
            opn.write("---------------------\n")
            for house in kundli:
                if house == "1" and len(kundli[house]["asc"]) != 0:
                    opn.write("Asc: "+kundli[house]["asc"].strip("+>")+"\n")
                
                if len(kundli[house]["planets"]) != 0:
                    for planet in kundli[house]["planets"]:
                        opn.write(planet+": "+kundli[house]["planets"][planet].strip("+")+"\n")
            
            opn.write("\n")
    elif mode == 1:
        with open(filename, "a") as opn:
            opn.write("transit Kundli\n")
            opn.write("---------------------\n")
            for house in kundli:
                if kundli[house]["asc"] != None:
                    opn.write("Asc: "+kundli[house]["asc"].strip("+>")+"\n")
                if len(kundli[house]["planets"]) != 0:
                    for planet in kundli[house]["planets"]:
                        opn.write(planet+": "+kundli[house]["planets"][planet].strip("+")+"\n")
            
            opn.write("\n")
if __name__ == "__main__":
    output = "output"
    if not os.path.exists(output):
        os.mkdir(output)
    time = datetime.datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    name = name.replace(" ", "-")
    if not os.path.exists(output+"/"+name+"-"+time):
        os.mkdir(output+"/"+name+"-"+time) 
    
    image_pos = None
    with open("img_pos.json", "r") as opn:
        image_pos = json.load(opn)
    kundli  = GKundli.GKundli(year, month, day, hour, minute, utc, latitude, longitude).lagnaChart()
    navamsa = navamsaChart(kundli)
    moon    = get_moon_chart(kundli)
    transit = GKundli.GKundli(year, month, day, hour, minute, utc, latitude, longitude).transitChart(kundli)

    write_to_image(kundli, image_pos, "Kundli-Design.png", output, 0)
    write_to_image(transit, image_pos, "Kundli-Design.png", output, 1)
    write_to_image(navamsa, image_pos, "Kundli-Design.png", output, 2)
    write_to_image(moon, image_pos, "Kundli-Design.png", output, 3)

    write_to_file(output+"/"+name+"-"+time+"/"+time+".txt", kundli, 0)
    write_to_file(output+"/"+name+"-"+time+"/"+time+".txt", transit, 1)
