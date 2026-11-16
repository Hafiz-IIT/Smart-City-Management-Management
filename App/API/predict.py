from fastapi import APIRouter, Query

from App.Services.sim import predict_bin_overflow, predict_traffic_hotspots

router = APIRouter(prefix="/api/predict", tags=["predict"])


@router.get("")
def predict(type: str | None = Query(default=None)):
    if type == "traffic":
        return {"items": predict_traffic_hotspots()}
    if type == "waste":
        return {"items": predict_bin_overflow()}
    return {"ok": True, "note": "use ?type=traffic or ?type=waste"}
