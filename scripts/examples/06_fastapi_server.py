"""SQLite üzerinden basit REST API."""
import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query

DB = Path("data/sqlite/yokatlas.sqlite")
app = FastAPI(title="YÖK Atlas API", version="1.0.0")


def q(sql: str, params: tuple = ()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


@app.get("/")
def root():
    return {"mesaj": "YÖK Atlas API", "endpointlar": ["/programs", "/programs/{code}", "/stats"]}


@app.get("/programs")
def list_programs(
    city: str | None = Query(None),
    type: str | None = Query(None),
    limit: int = Query(50, le=500),
):
    sql, params = "SELECT * FROM programs WHERE 1=1", []
    if city:
        sql += " AND city = ?"; params.append(city)
    if type:
        sql += " AND type = ?"; params.append(type)
    sql += " LIMIT ?"; params.append(limit)
    return q(sql, tuple(params))


@app.get("/programs/{code}")
def get_program(code: str):
    rows = q("SELECT * FROM programs WHERE program_code = ?", (code,))
    if not rows:
        raise HTTPException(404, "Program bulunamadı")
    return rows[0]


@app.get("/stats")
def stats():
    return {
        "toplam_program": q("SELECT COUNT(*) c FROM programs")[0]["c"],
        "şehirler": q("SELECT city, COUNT(*) adet FROM programs GROUP BY city ORDER BY adet DESC LIMIT 10"),
        "gruplar": q("SELECT program_group, COUNT(*) adet FROM programs GROUP BY program_group ORDER BY adet DESC LIMIT 10"),
    }