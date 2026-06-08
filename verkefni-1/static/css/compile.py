# munið að vísa (cd ...) terminal ofaní css möppuna

files_names = [
   "pico.orange",
   "grid",
   "table-form",
   "colors",
   "custom",
   "menues",
   "icomoon",
   "chatbox",
   "kvikun"
]
data = "" 

for file_name in files_names :
   with open(file_name+".css" ,"r") as file_handle :
      temp_data = file_handle.read()
      data = data + temp_data #  öll *.css skjölin eru lesin inn í data breytuna

with open ('styles.min.css', 'w') as file_handle : 
  file_handle.write(data)
