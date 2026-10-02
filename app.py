from fastapi import FastAPI,Request,Form
from fastapi.templating import Jinja2Templates
from database import conn
from fastapi.responses import RedirectResponse

templates=Jinja2Templates(directory="templates")

app=FastAPI()

@app.get("/")
def display(request:Request):
    dbcon=conn()
    con=dbcon.cursor(dictionary=True)
    con.execute("select * from student")
    f=con.fetchall()
    print(f)
    con.close()
    dbcon.close()

    return templates.TemplateResponse(request=request,name="display.html",context={"data":f})

@app.get("/addpage")
def addpage(request:Request):
    return templates.TemplateResponse(request=request,name="addstudent.html",context={})

@app.post("/adddata")
def adddata(request:Request,name:str =Form(...),age:int =Form(...),mark:int =Form(...)):
    dbcon=conn()
    con=dbcon.cursor()
    con.execute("insert into student(name,age,mark) values(%s,%s,%s)",(name,age,mark))
    dbcon.commit()
    if con.rowcount >=1 :
        con.close()
        dbcon.close()
        return RedirectResponse(url="/",status_code=303)
    
    else:
        con.close()
        dbcon.close()
        return {
            "message":"data not saved"
        }
@app.post("/updatedata/{id}")
def updatedata(request:Request,id:int,name:str = Form(...),age:int = Form(...),mark:int = Form(...)):
    dbcon=conn()
    con=dbcon.cursor()
    con.execute("update student set name=%s,age=%s,mark=%s where id=%s",(name,age,mark,id))
    dbcon.commit()
    if con.rowcount >=1 :
        con.close()
        dbcon.close()
        return RedirectResponse(url="/",status_code=303)
    
    else:
        con.close()
        dbcon.close()
        return {
            "message":"data not saved"
        }


@app.get("/update/{id}")
def delete(request:Request,id:int):
    dbcon=conn()
    con=dbcon.cursor(dictionary=True)
    con.execute("select * from student where id=%s",(id,))
    f=con.fetchone()
    con.close()
    dbcon.close()
    return templates.TemplateResponse(request=request,name="updatestudent.html",context={"datas":f})

@app.get("/delete/{id}")
def delete(request:Request,id:int):
    dbcon=conn()
    con=dbcon.cursor()
    con.execute("delete from student where id=%s",(id,))
    dbcon.commit()

    if con.rowcount >= 1:
        con.close()
        dbcon.close()
        return RedirectResponse(url="/",status_code=303)
    else:
        con.close()
        dbcon.close()
        return { "message":"delete not invalid id"}


    