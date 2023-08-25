import os
import json
import datetime
import GKundli
from PIL import Image, ImageDraw, ImageFont

name = input("Enter Name: ")
year = int(input("Year: "))
month = int(input("Month: "))
day = int(input("Day: "))
hour = int(input("Hour: "))
minute = int(input("Minute: "))
utc = input("UTC: ")
latitude = float(input("Latitude: "))
longitude = float(input("Longitude: "))


def write_to_image(kundli, image_pos, kundli_img, output, mode):
    if mode == 0:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"LagnaKundli-"+name+"-"+time+".png")
    elif mode == 1:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"Transit-"+name+"-"+time+".png")
    elif mode == 2:
        out = "{0}/{1}/{2}".format(output,name+"-"+time,"Navamasa-"+name+"-"+time+".png")
    
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
    
    if mode == 1:
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
    kundli = GKundli.GKundli(year, month, day, hour, minute, utc, latitude, longitude).Bkundli()
    transit = GKundli.GKundli(year, month, day, hour, minute, utc, latitude, longitude).transit_kundli(kundli)
    write_to_image(kundli, image_pos, "Kundli-Design.png", output, 0)
    write_to_image(transit, image_pos, "Kundli-Design.png", output, 1)
    write_to_file(output+"/"+name+"-"+time+"/"+time+".txt", kundli, 0)
    write_to_file(output+"/"+name+"-"+time+"/"+time+".txt", transit, 1)
