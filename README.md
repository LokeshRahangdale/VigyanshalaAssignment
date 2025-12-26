# VigyanshalaAssignment
#Create Env 
python -m venv venv
#activate env
source venv/bin/activate 

#install fast api, uvicorn
pip install fastapi uvicorn

# run application
uvicorn main:app --reload
