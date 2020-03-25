from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import mysql.connector
import env


mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	passwd = env.password,
	database = "toshiba",
	)

my_cursor = mydb.cursor()
# DELETE TABLE
my_cursor.execute("DROP TABLE IF EXISTS player")

# CREATE TABLE
my_cursor.execute("CREATE TABLE player (name VARCHAR(255), position VARCHAR(255), age INTEGER(10), height INTEGER(10) , weight INTEGER(10) , school VARCHAR(255),user_id INTEGER AUTO_INCREMENT PRIMARY KEY)")


r=requests.get("https://www.toshiba.co.jp/sports/rugby/member/")
soup = BeautifulSoup(r.content, "html.parser")
player_name=[]

positions=["prop","hooker","lock","flanker","no8","scrumhalf","standoff","center","wing","fullback"]
for position in positions:
	posi=soup.select("#"+position)[0]

	for posi_member in posi.select(".member-box"):
		posi_name=posi_member.select("a")[0].text
		player_name.append(posi_name)




driver = webdriver.Chrome("c:/chromedriver.exe")
driver.get("https://www.toshiba.co.jp/sports/rugby/member/")


for name in player_name:
	driver.get("https://www.toshiba.co.jp/sports/rugby/member/")
	driver.find_element_by_link_text(name).click()
	position = driver.find_element_by_class_name('position').text
	age= int(driver.find_element_by_xpath("//tbody/tr[2]/td").text.rstrip("歳"))
	height= int(driver.find_element_by_xpath("//tbody/tr[3]/td").text.rstrip("cm"))
	weight= int(driver.find_element_by_xpath("//tbody/tr[4]/td").text.rstrip("kg"))
	school= driver.find_element_by_xpath("//tbody/tr[7]/td").text

	sqlStuff = "INSERT INTO player (name, position, age, height, weight, school) VALUES (%s,%s,%s,%s,%s,%s)"
	record = (name,position,age,height,weight,school)
	my_cursor.execute(sqlStuff, record)
	mydb.commit()





		
