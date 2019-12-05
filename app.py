import pymysql
import json
import random as r

db_user = "root"
db_pass = "123456"
db_name = "eatout"
socket_path="xxxxxxxx:us-central1:mysqldb"


def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [5]
    for n in uuid_format:
        for i in range(0,n):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
    return random_string

def user_input():
    try:
        f_name = input("Enter File name to upload User Detail and Feedback Data      ")
        with open(f_name, 'r') as json_file:
            line = json_file.readline()
            count = 1
            while line:
                input_user = json.loads(line)
                pno = str(input_user["pno"])
                rows_count = cursor.execute("""SELECT id FROM UserDetails WHERE phonenumber='%s'""" % (pno))
                records = cursor.fetchall()
                for i in records:
                    ud_id = i[0]
                if rows_count:
                    user_update(input_user)
                    user_feedback(input_user, ud_id)
                else:
                    ud_id = generate_uuid()
                    user_details(input_user, ud_id)
                    user_feedback(input_user, ud_id)
                print(str(count) + " Record Successfully Inserted/Updated")
                count = count + 1
                line = json_file.readline()

    except Exception as e:
        print(e)


def user_update(input_json):
    try:

        pno = str(input_json["pno"])
        us_name = str(input_json["name"])
        us_eid = str(input_json["emailid"])
        us_selfdob = str(input_json["selfdob"])
        us_spdob = str(input_json["spousedob"])
        us_ma = str(input_json["anniversary"])

        cursor.execute(
            """update UserDetails set Name = '%s' , Emailid='%s', Birthday='%s', SpouseBirthday='%s', Anniversary='%s' where phonenumber='%s'""" % (
            us_name, us_eid, us_selfdob, us_spdob, us_ma, pno,))

        db_conn.commit()
        print("User Record Updated successfully ")
    except Exception as e:
        print(e)


def user_details(input_json=None, ud_id=None):
    try:
        # input_json = input()
        # input_json = json.loads(input_json)
        user_id = ud_id
        ud_rname = str(input_json["name"])
        ud_pn = str(input_json["pno"])
        ud_eid = str(input_json["emailid"])
        ud_selfdob = str(input_json["selfdob"])
        ud_spdob = str(input_json["spousedob"])
        ud_ma = str(input_json["anniversary"])
        cursor.execute("""INSERT into UserDetails VALUES ("%s", "%s", "%s", "%s", "%s","%s","%s")""" % (
        user_id, ud_rname, ud_pn, ud_eid, ud_selfdob, ud_spdob, ud_ma))
        db_conn.commit()
        print("User Detail Record Insertion Successful")

    except Exception as e:
        print(e)


def user_feedback(input_json=None, us_id=None):
    try:
        fb_dov = str(input_json["dateofvisit"])
        fb_resid = str(input_json["restid"])
        fb_fq = str(input_json["foodquality"])
        fb_sq = str(input_json["servicequality"])
        fb_amb = str(input_json["ambience"])
        fb_music = str(input_json["music"])
        fb_vfm = str(input_json["valueformoney"])
        fb_clean = str(input_json["cleanliness"])
        fb_fv = str(input_json["foodvariety"])

        cursor.execute("""INSERT INTO UserFeedback (`UserId`, `VisitDate`, `RestaurantId`, `FoodQuality`,`ServiceQuality`,`Ambience`,`LiveMusic`,`ValueForMoney`,`Cleanliness`,`FoodVariety`) VALUES
         ("%s", "%s", "%s", "%s", "%s","%s","%s","%s","%s","%s")""" % (
        us_id, fb_dov, fb_resid, fb_fq, fb_sq, fb_amb, fb_music, fb_vfm, fb_clean, fb_fv))
        db_conn.commit()

        print("Feedback Record Insertion Successful")

    except Exception as e:
        print(e)


def register_restaurant():
    try:
        f_name = input("Enter File name to upload Restaurant Data      ")
        with open(f_name, 'r') as json_file:
            line = json_file.readline()
            count = 1
            while line:
                input_json1 = json.loads(line)
                uid = generate_uuid()
                r_rname = str(input_json1["name"])
                r_cuisine = str(input_json1["cuisine"])
                r_region = str(input_json1["region"])
                r_location = str(input_json1["location"])
                cursor.execute("""INSERT INTO Restaurant VALUES ("%s", "%s", "%s", "%s", "%s")""" % (
                uid, r_rname, r_cuisine, r_region, r_location))
                db_conn.commit()
                print("Record No - " + str(count) + "  Insertion Successful for Restaurant name -- " + r_rname)
                count = count + 1
                line = json_file.readline()

    except Exception as e:
        print(e)


def delete_restaurant():
    try:
        f_name = input("Enter File name to Delete Restaurant Data      ")
        with open(f_name, 'r') as json_file:
            line = json_file.readline()
            while line:
                input_json1 = json.loads(line)
                restid = str(input_json1["id"])
                data = (restid,)
                query = "delete from Restaurant where id= %s"
                rows_count = cursor.execute("""SELECT id FROM Restaurant WHERE id='%s'""" % restid)
                if rows_count > 0:
                    cursor.execute(query, data)
                    db_conn.commit()
                    print(" Restaurant Successfully Deleted")
                else:
                    print("Restaurant doesnt exists")
                line = json_file.readline()
    except Exception as e:
        print(e)


"""QUERIES"""
def query_1():
    try:
        cursor.execute("select r1.name from (select restaurantid, avg(((foodquality+servicequality+ambience+livemusic+valueformoney+cleanliness+foodvariety)*1.0)/7) avgratingacrossall from UserFeedback group by restaurantid order by 1 desc limit 1)tbla, Restaurant r1 where tbla.restaurantid=r1.id")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)

def query_2():
    try:
        print("Enter parameter on which restaurants has to be compared  :")
        parameter = input()
        if parameter== 'foodquality':
            cursor.execute("""select r1.name from (select restaurantid, avg(foodquality) avgratingselected from UserFeedback group by restaurantid order by 1 desc limit 2)tbla, Restaurant r1 where tbla.restaurantid=r1.id;""")
        if parameter=='servicequality':
            cursor.execute("""select r1.name from (select restaurantid, avg(servicequality) avgratingselected from UserFeedback group by restaurantid order by 1 desc limit 2)tbla, Restaurant r1 where tbla.restaurantid=r1.id;""")
        rows=cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)


def query_3():
    try:
        print("Enter the date for which the birthday has to be checked :")
        date_input = input()
        cursor.execute("""select Name, PhoneNumber, emailId from UserDetails where month(birthday)=month('%s') and day(birthday) between day('%s') and day('%s')+7"""%(date_input,date_input,date_input))
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)

def query_4():
    try:
        print("Enter the date for which occassion has to checked :")
        date_input = input()
        cursor.execute("""select Name, PhoneNumber, emailId from UserDetails where month(birthday)=month('%s') or month(spousebirthday)=month('%s') and month(anniversary)=month('%s')"""%(date_input,date_input,date_input))
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        db_conn = pymysql.connect(unix_socket=socket_path, user=db_user, password=db_pass, db=db_name)
        cursor = db_conn.cursor()
        while True:
            print("Select the operations to perform:")
            print("1. Register Restaurant")
            print("2. Load User Feedback")
            print("3. Fetch the top rated restaurant")
            print("4. Top 2 basis on my input")
            print("5. List users with birthdays in next 7 days from the date specified")
            print("6. List users with any of there occasion in given month")
            print("7. Delete Restaurant")
            print("0. Exit")
            operation = input()
            # print(operation)
            if(operation=='1' or operation == 1):
                print("Selected: Register Restaurant")
                register_restaurant()
            if(operation == '2' or operation == 2):
                print("Selected: Load User Feedback")
                user_input()
            if(operation == '3' or operation== 3):
                print("Selected: Fetch top rated restaurant")
                query_1()
            if (operation == '4' or operation == 4):
                print("Selected: Top 2 on the basis of input")
                query_2()
            if (operation == '5' or operation == 5):
                print("Selected: List users with birthday")
                query_3()
            if (operation == '6' or operation == 6):
                print("Selected: List users with any occassion")
                query_4()
            if (operation == '7' or operation == 7):
                print("Selected: Delete Restaurant")
                delete_restaurant()
            if( operation == '0' or operation == 0):
                print("Thank You")
                cursor.close()
                db_conn.close()
                print (db_conn.ping())
                break

    except Exception as e:
        db_conn.close()
        print(e)
