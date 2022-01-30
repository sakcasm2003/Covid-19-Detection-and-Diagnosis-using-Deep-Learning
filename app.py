import os
import streamlit as st

from database import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine




st.title("Report for Covid-19 Detection")

def opendb():
    engine = create_engine('sqlite:///db.sqlite3') # connect
    Session =  sessionmaker(bind=engine)
    return Session()

def save_file(path,record):
    try:
        db = opendb()
        img = Images(path=path,patient=record.id)
        db.add(img)
        db.commit()
        db.close()
        return True
    except Exception as e:
        st.write("database error:",e)
        return False


optionlist = ['View Patients','Register New Patients','Add Patients X-ray']
choice = st.sidebar.selectbox("select option",optionlist)

if choice == optionlist[1]:
    with st.form("Register_form"):
        name = st.text_input("Patients Name")
        age = st.number_input("Patients Age",min_value=5, max_value=100,value=35)
        gender = st.radio("Patient's Gender",['Male','Female','Other'])    
        btn = st.form_submit_button("Save Patient Details")
    
    if btn and name:
        try:
            db=opendb()
            pObj = Patients(name=name,age=age,gender=gender)
            db.add(pObj)
            db.commit()
            db.close()
            st.success("Patients Details successfully saved")
        except Exception as e:
            st.error(f"error occured {e}")
if choice == optionlist[2]:
    database = opendb()
    results = database.query(Patients).all()
    database.close()
    records = [row.__dict__ for row in results]
    records_clean = []
    for row in records:
        row.pop('_sa_instance_state')
        records_clean.append(row)

    
    patient = st.sidebar.selectbox('select Patients',[row['name'] for row in records_clean])
    if patient:
        database = opendb()
        record = database.query(Patients).filter(Patients.name==patient).all()[0]
        if record:
            st.markdown(f"""
            # Patients Detail Below
            #### ID : {record.id}
            #### Name : {record.name}
            #### Age : {record.age}
            #### Gender : {record.gender}
            """)
            with st.form("Xray_form"):
                st.warning("The name of imagefile must be in the following format [patient_name.png or patient_name.jpg]")
                image = st.file_uploader("Upload Patient Xray Image",type=['.jpg','.png'])
                btn2 = st.form_submit_button("Upload Xray Scan")
            if btn2 and image:
                path = os.path.join('uploads',image.name)
                with open(path,'wb') as f:
                    f.write(image.getbuffer())
                status = save_file(path,record)
                if status:
                    st.sidebar.success("file uploaded")
                    st.sidebar.image(path,use_column_width=True)
                else:   
                    st.sidebar.error('upload failed')
            else:
                st.error("Some error occurred")
        database.close()
        


