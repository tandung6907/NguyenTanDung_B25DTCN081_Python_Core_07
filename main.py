from typing import List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

danh_sach_sach = [
    {
        "id": 1,
        "ten_sach": "Nhà Giả Kim",
        "tac_gia": "Paulo Coelho",
        "nam_xuat_ban": 1988,
        "so_luong": 5
    },
    {
        "id": 2,
        "ten_sach": "Đắc Nhân Tâm",
        "tac_gia": "Dale Carnegie",
        "nam_xuat_ban": 1936,
        "so_luong": 6
    },
]

class SachTao(BaseModel):
    ten_sach: str
    tac_gia: str
    nam_xuat_ban: int
    so_luong: int

class SachCapNhat(BaseModel):
    ten_sach: Optional[str] = None
    tac_gia: Optional[str] = None
    nam_xuat_ban: Optional[int] = None
    so_luong: Optional[int] = None

class SachPhanHoi(SachTao):
    id: int


@app.post("/api/v1/books", response_model=SachPhanHoi, status_code=201)
async def them_sach(sach: SachTao):

    sach_moi = sach.model_dump()
    sach_moi["id"] = len(danh_sach_sach) + 1

    danh_sach_sach.append(sach_moi)

    return sach_moi


@app.get("/api/v1/books", response_model=List[SachPhanHoi])
async def lay_danh_sach_sach():

    if not danh_sach_sach:
        raise HTTPException(
            status_code=404,
            detail="Không có cuốn sách nào trong danh sách."
        )

    return danh_sach_sach

@app.get("/api/v1/books/{book_id}", response_model= SachPhanHoi)
async def lay_sach_theo_id(id: int):
    sach = next((s for s in danh_sach_sach if s["id"] == id), None)

    if not sach:
        raise HTTPException(status_code= 404, detail= "Không tìm thấy sách")
    return sach

@app.patch("/api/v1/books/{book_id}", response_model= SachPhanHoi)
async def cap_nhat_sach_theo_id(id: int, sach: SachCapNhat):
    sach_can_tim = next((s for s in danh_sach_sach if s["id"] == id), None)

    if not sach_can_tim:
        raise HTTPException(status_code= 404, detail= "Không tìm thấy sách")

    sach_moi = sach.model_dump(exclude_unset= True)

    for key, value in sach_moi.items():
        sach_can_tim[key] = value

    return sach_can_tim

@app.delete("/api/v1/books/{book_id}", response_model= SachPhanHoi)
async def xoa_sach_theo_id(id: int):
    sach_can_xoa = next((s for s in danh_sach_sach if s["id"] == id), None)

    if not sach_can_xoa:
        raise HTTPException(status_code= 404, detail= "Không tìm thấy sách")

    danh_sach_sach.remove(sach_can_xoa)

    return {"message" : "Xóa thành công"}