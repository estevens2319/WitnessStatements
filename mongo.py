from pymongo import MongoClient

import datetime
# from NER import NER_func

def store_in_db(text,case_id):
   CONNECTION_STRING = "mongodb+srv://mohit19sv:mohitsv@cluster0.hj4st4q.mongodb.net/witness_statement"
   client = MongoClient(CONNECTION_STRING)
   db = client.witness_statement
   coll = db[case_id]
   # print(coll)
   curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   
   emp_rec1 = {
        "Timestamp": curr_time,
        "Case ID": case_id,
        "Statement": text
        } 
   coll.insert_one(emp_rec1)

#    ner_result = NER_func(text)
#    db_2 = client.NER
#    coll_2 = db_2[case_id]
#    ner_result['Timestamp'] = curr_time
#    ner_result['Case ID'] = case_id
#    coll_2.insert_one(ner_result)

   return "finished"

def show_mongodb_statements(case_id):
   CONNECTION_STRING = "mongodb+srv://mohit19sv:mohitsv@cluster0.hj4st4q.mongodb.net/witness_statement"
   client = MongoClient(CONNECTION_STRING)
   db = client.witness_statement
   coll=db[case_id]
   cursor = coll.find()
   dict_statements = {} 
   for record in cursor:
      dict_statements[len(dict_statements)+1] = record['Statement']
      # print(record['Statement'])
   return dict_statements

def show_mongodb_ner(case_id):
   CONNECTION_STRING = "mongodb+srv://mohit19sv:mohitsv@cluster0.hj4st4q.mongodb.net/witness_statement"
   client = MongoClient(CONNECTION_STRING)
   db = client.NER
   coll = db[case_id]
   cursor = coll.find()
   dict_NER = {}
   keys_to_exclude=['_id','Case ID','DATE','Timestamp']
   for record in cursor:
      record_new = {key: value for key, value in record.items() if key not in keys_to_exclude}
      dict_NER[len(dict_NER)+1] = record_new
   return dict_NER

show_mongodb_statements('John')