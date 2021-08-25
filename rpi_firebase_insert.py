from firebase import firebase

firebase = firebase.FirebaseApplication("https://gassensor-database-default-rtdb.firebaseio.com/", None)
data = {
  # 'CO': ppm_gasarray[0],
  # 'Toulene': ppm_gasarray[1],
  # 'Ammonia': ppm_gasarray[2],
  # 'Methane': ppm_gasarray[3],
  # 'Ethanol': ppm_gasarray[4]

  "body": "Test"
}

result = firebase.post('/gassensor-database-default-rtdb/gasdata:', data)

print(result)

