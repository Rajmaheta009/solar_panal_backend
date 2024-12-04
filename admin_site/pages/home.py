from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

app=FastAPI()

class PagesSection(BaseModel):
    sector_name:str
    sector_title:str
    sector_subtitle:str
    sector_multimedia:str
    sector_background:str




Connection_string="mongodb://localhost:27017"

Connect=AsyncIOMotorClient(Connection_string)
Database_name=Connect.solar_panal
Collation_name=Database_name.get_collection('pages')

@app.get("/get_data")
async def get_data():
    data= await Collation_name.find().to_list(length=None)
    return data

@app.post("/add_data",status_code=201)
async def add_data(field:PagesSection):
    result = await Collation_name.insert_one(field.dict())
    inserted_data ={"add_data_status":"data Add successfully"}
    return inserted_data

@app.put("/update_data",status_code=200)
async def update_data(field:PagesSection,SectorName):
    existing_document = await Collation_name.find_one({"sector_name": SectorName})
    if not existing_document:
        raise HTTPException(status_code=404, detail="Data not found")
    update_result = await Collation_name.update_one(
        {"sector_name": SectorName},  # Filter
        {"$set": field.dict()})
    if update_result.modified_count > 0:
        return {"update_data_status": "Data updated successfully"}