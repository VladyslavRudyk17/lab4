from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from auth import get_role, require_admin
from database import get_session
from models.apartments import Apartment
from models.resident import Resident

app = FastAPI(title="ОСББ API")

# ================= ПУНКТ 1: Адмін-сторінка =================
@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    return """
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8">
        <title>ОСББ Адмін-панель</title>
        <style>
            body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
            input, button { display: block; width: 100%; margin-bottom: 10px; padding: 8px; box-sizing: border-box; }
            button { background-color: #007bff; color: white; border: none; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>Додати нового жителя</h2>
        <input id="name" placeholder="ПІБ (напр. Іван Франко)" required>
        <input id="phone" placeholder="Телефон (напр. +380671234567)" required>
        <input id="email" placeholder="Email (напр. ivan@osbb.ua)" required>
        <input id="apt_id" type="number" placeholder="ID Квартири (1-15)">
        <button onclick="addResident()">Створити запис</button>
        <p id="result"></p>

        <script>
            async function addResident() {
                const data = {
                    full_name: document.getElementById('name').value,
                    phone: document.getElementById('phone').value,
                    email: document.getElementById('email').value,
                    apartment_id: parseInt(document.getElementById('apt_id').value) || null
                };
                
                const response = await fetch('/residents/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': 'admin-key-123'
                    },
                    body: JSON.stringify(data)
                });
                
                const resultText = await response.text();
                document.getElementById('result').innerText = response.ok ? "Успішно додано!" : "Помилка: " + resultText;
            }
        </script>
    </body>
    </html>
    """

# ================= APARTMENTS (Квартири) =================
@app.get("/apartments/")
def read_apartments(session: Session = Depends(get_session), role: str = Depends(get_role)):
    return session.exec(select(Apartment)).all()

@app.get("/apartments/{apartment_id}")
def get_apartment(apartment_id: int, session: Session = Depends(get_session), role: str = Depends(get_role)):
    apartment = session.get(Apartment, apartment_id)
    if apartment is None:
        raise HTTPException(status_code=404, detail="Квартиру не знайдено")
    return apartment

@app.post("/apartments/")
def create_apartment(apartment: Apartment, session: Session = Depends(get_session), role: str = Depends(require_admin)):
    session.add(apartment)
    session.commit()
    session.refresh(apartment)
    return apartment

# ================= RESIDENTS (Жителі) =================
@app.get("/residents/")
def read_residents(session: Session = Depends(get_session), role: str = Depends(get_role)):
    return session.exec(select(Resident)).all()

@app.get("/residents/{resident_id}")
def get_resident(resident_id: int, session: Session = Depends(get_session), role: str = Depends(get_role)):
    resident = session.get(Resident, resident_id)
    if resident is None:
        raise HTTPException(status_code=404, detail="Жителя не знайдено")
    return resident

@app.post("/residents/")
def create_resident(resident: Resident, session: Session = Depends(get_session), role: str = Depends(require_admin)):
    session.add(resident)
    session.commit()
    session.refresh(resident)
    return resident

@app.put("/residents/{resident_id}")
def update_resident(resident_id: int, updated_data: Resident, session: Session = Depends(get_session), role: str = Depends(require_admin)):
    db_resident = session.get(Resident, resident_id)
    if not db_resident:
        raise HTTPException(status_code=404, detail="Жителя не знайдено")
    db_resident.full_name = updated_data.full_name
    db_resident.phone = updated_data.phone
    db_resident.email = updated_data.email
    db_resident.apartment_id = updated_data.apartment_id
    session.add(db_resident)
    session.commit()
    session.refresh(db_resident)
    return db_resident

@app.delete("/residents/{resident_id}")
def delete_resident(resident_id: int, session: Session = Depends(get_session), role: str = Depends(require_admin)):
    db_resident = session.get(Resident, resident_id)
    if not db_resident:
        raise HTTPException(status_code=404, detail="Жителя не знайдено")
    session.delete(db_resident)
    session.commit()
    return {"message": "Жителя успішно видалено"}