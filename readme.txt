venv\scripts\activate

To debug run:
python deskop/dev.py

To test build version (Note ):
python desktop/build.py   

Switch between these two lines for build and package py
dist = resource_path("frontend/dist") # use this if u are running python .\desktop\package.py 
# dist = os.path.abspath("../frontend/dist")  # use this if u are running python .\desktop\build.py 


To build exe:
python desktop/package.py   