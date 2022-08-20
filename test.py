from flask import  Flask , request, jsonify
import mysql.connector as connection
import pymongo
app = Flask(__name__)

def connection_with_sql():
    try:
        conn = connection.connect(host="localhost", database='student', user='root', passwd="mysql", use_pure=True)
        return conn
    except Exception as e:
        return jsonify((str(e)))

def connection_with_mongodb():
    try:
        client = pymongo.MongoClient("mongodb+srv://Divyanshu:mongodb@cluster0.ytdqx1j.mongodb.net/?retryWrites=true&w=majority")
        db = client.test
        collection = db['test']
        return collection

    except Exception as e:
        return jsonify((str(e)))

@app.route('/sql/insert',methods=['GET' , 'POST'])
def test1():
    """
        In PostMan
        {
        "id":1135,
        "fname":"div",
        "lname":"singh",
        "rdate":"1997-10-12",
        "sclass":"Eleventh",
        "section":"B",
        }
        """
    conn = connection_with_sql()
    cur = conn.cursor()

    if(request.method=='POST'):
        student_id = request.json['id']
        first_name = request.json['fname']
        last_name = request.json['lname']
        registration_date = request.json['rdate']
        student_class = request.json['sclass']
        section = request.json['section']

        try:
            query = " INSERT INTO StudentDetails VALUE ({}, '{}', '{}', '{}', '{}', '{}')".format(student_id, first_name, last_name, registration_date, student_class, section)
            cur.execute(query)
            conn.commit()
            return jsonify(("Values are inserted !!"))
        except Exception as e:
            return jsonify((str(e)))

@app.route('/sql/update',methods=['GET' , 'POST'])
def test2():
    """
    In PostMan
    {
    "id":1135,
    "fname":"div",
    "lname":"singh",
    "rdate":"1997-10-12",
    "sclass":"Eleventh",
    "section":"B",
    "cnd":"Studentid=1145"
    }
    """
    conn = connection_with_sql()
    cur = conn.cursor()

    if(request.method=='POST'):
        student_id = request.json['id']
        first_name = request.json['fname']
        last_name = request.json['lname']
        registration_date = request.json['rdate']
        student_class = request.json['sclass']
        section = request.json['section']
        cond = request.json['cnd']

        try:
            query = " UPDATE StudentDetails SET Studentid ='{}', FirstName ='{}', LastName ='{}', RegistrationDate ='{}', Class ='{}', Section ='{}'  WHERE {}".format(student_id, first_name, last_name, registration_date, student_class, section,cond)
            cur.execute(query)
            conn.commit()
            return jsonify(("Values are updated !!"))
        except Exception as e:
            return jsonify((str(e)))

@app.route('/sql/show',methods=['GET' , 'POST'])
def test3():
    """
    In PostMan
    {
    "cnd":"Studentid=1135"
    }
    """
    conn = connection_with_sql()
    cur = conn.cursor()

    if(request.method=='POST'):
        cond = request.json['cnd']

        try:
            query = " SELECT * FROM StudentDetails WHERE {}".format(cond)
            cur.execute(query)
            return jsonify((cur.fetchall()))
        except Exception as e:
            return jsonify((str(e)))

#mongodb
@app.route('/mongodb/insert',methods=['GET' , 'POST'])
def test11():
    """
        In PostMan
        {
        "CompanyName":"iNeuron",
        "Product":"Ai",
        "courseOffered": "Deep learning"
        }
    """
    collection = connection_with_mongodb()

    if(request.method=='POST'):
        cmp = request.json['CompanyName']
        product = request.json['Product']
        coff = request.json['courseOffered']

        try:
            record = {
                'CompanyName': str(cmp), 'Product': str(product), 'courseOffered': str(coff)
            }
            return jsonify((str(collection.insert_one(record))))
        except Exception as e:
            return jsonify((str(e)))

@app.route('/mongodb/update',methods=['GET' , 'POST'])
def test12():
    """
        In PostMan
        {
        "CompanyName":"iNeuron",
        "Product":"Ai",
        "courseOffered": "Deep learning",
        "cond":"CompanyName":"iNeuron"
        }
    """
    collection = connection_with_mongodb()

    if(request.method=='POST'):
        cmp = request.json['CompanyName']
        product = request.json['Product']
        coff = request.json['courseOffered']
        cond = request.json['cond']
        myquery = list(map(str,cond.split(":")))

        try:
            record = {"$set" : {'CompanyName': str(cmp), 'Product': str(product), 'courseOffered': str(coff)}}
            return jsonify((str(collection.update_one({myquery[0]:myquery[1]}, record))))
        except Exception as e:
            return jsonify((str(e)))

@app.route('/mongodb/show',methods=['GET' , 'POST'])
def test13():
    """
        In PostMan
        {
        "CompanyName":"iNeuron",
        "Product":"Ai",
        "courseOffered": "Deep learning",
        "cond":"CompanyName":"iNeuron"
        }
    """
    collection = connection_with_mongodb()

    if(request.method=='POST'):
        try:
            x1 = [str(x) for x in collection.find()]
            return jsonify(( x1 ))
        except Exception as e:
            return jsonify((str(e)))

if __name__=='__main__'  :
    app.run()



