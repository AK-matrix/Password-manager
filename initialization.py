import pickle
f = open("passwords.bin","wb")
pickle.dump({},f)
f.close()
