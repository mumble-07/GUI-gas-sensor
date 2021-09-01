from firebase import firebase

# firebase = firebase.FirebaseApplication("https://gassensor-database-default-rtdb.firebaseio.com/", None)
# data = {
#   # 'CO': ppm_gasarray[0],
#   # 'Toulene': ppm_gasarray[1],
#   # 'Ammonia': ppm_gasarray[2],
#   # 'Methane': ppm_gasarray[3],
#   # 'Ethanol': ppm_gasarray[4]

#   "body": "Test"
# }

# result = firebase.post('/gassensor-database-default-rtdb/gasdata:', data)

# print(result)

firebase_data = firebase.FirebaseApplication("https://gassensor-db-default-rtdb.firebaseio.com/", None)
   
    
  data = {
      'Ammonia': raw_Ammonia,
      'CO': raw_CO,
      'Ethanol': raw_Ethanol,
      'Isobutane': raw_Isobutane,
      'Methane': raw_Methane,
      'Toluene': raw_Toluene,
      'H_Timestamp': datetime.today().strftime("%H"),
      'M_Timestamp': datetime.today().strftime("%M"),
      'Gas_Status': 0
          }
    
    result = firebase_data.put('/gassensor-db-default-rtdb/gasdata:',"-MhvYPVvC3476qBwCADx", data)
    print(result)