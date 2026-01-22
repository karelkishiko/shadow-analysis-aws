from fastapi import FastAPI, HTTPException
from pathlib import Path
import traceback

from pydantic import BaseModel
import numpy as np
import pandas as pd

from app.solarposition import get_solarposition
from app.shadowingfunction_wallheight_13 import shadowingfunction_wallheight_13

app = FastAPI(title="Shadow Analysis API")

# Chemins absolus (évite les problèmes Windows / dossiers)
BASE_DIR = Path(__file__).resolve().parent.parent  # => dossier shadow-app
DSM_PATH = BASE_DIR / "assets" / "dsm_local_array.npy"


class ShadowRequest(BaseModel):
    lat: float
    lon: float
    utc_offset_hours: int = -6


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shadow")
def shadow(req: ShadowRequest):
    try:
        # 1) Vérifier que le fichier DSM existe
        if not DSM_PATH.exists():
            raise HTTPException(
                status_code=500,
                detail=f"DSM file not found at: {str(DSM_PATH)}"
            )

        # 2) Charger DSM
        dsm = np.load(DSM_PATH)
        dsm = np.nan_to_num(dsm, nan=0.0)

        # 3) Temps (UTC)
        local_now = pd.Timestamp.now().floor("min")
        utc_time = local_now - pd.DateOffset(hours=req.utc_offset_hours)
        times = pd.DatetimeIndex([utc_time])

        # 4) Position solaire
        df = get_solarposition(times, req.lat, req.lon)
        altitude = float(df["elevation"].iloc[0])
        azimuth = float(df["azimuth"].iloc[0])

        # 5) Shadow
        scale = 1
        walls = np.zeros_like(dsm)
        dirwalls = np.zeros_like(dsm)

        sh, wallsh, wallsun, facesh, facesun = shadowingfunction_wallheight_13(
            dsm, azimuth, altitude, scale, walls, dirwalls * np.pi / 180.0
        )

        preview = sh[:20, :20].tolist()

        return {
            "local_time": str(local_now),
            "utc_time": str(utc_time),
            "lat": req.lat,
            "lon": req.lon,
            "azimuth": azimuth,
            "altitude": altitude,
            "shadow_shape": list(sh.shape),
            "shadow_min": float(np.min(sh)),
            "shadow_max": float(np.max(sh)),
            "shadow_mean": float(np.mean(sh)),
            "shadow_preview_20x20": preview,
        }

    except HTTPException:
        raise
    except Exception as e:
        # Pour voir l’erreur clairement dans Swagger + terminal
        tb = traceback.format_exc()
        print(tb)
        raise HTTPException(status_code=500, detail=str(e))


