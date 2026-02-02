from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
import tempfile
import os
import shutil
import pandas as pd

from app.services.topsis_service import run_topsis_service
from app.services.email_service import send_email_with_attachment

router = APIRouter(prefix="/api/topsis", tags=["TOPSIS"])


@router.post("/run")
async def run_topsis(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    weights: str = Form(...),
    impacts: str = Form(...),
    email: str = Form(...)
):
    # ----------------------------
    # 1. BASIC FILE VALIDATION
    # ----------------------------
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

    temp_dir = tempfile.mkdtemp()
    input_csv_path = os.path.join(temp_dir, file.filename)

    try:
        # ----------------------------
        # 2. SAVE CSV
        # ----------------------------
        with open(input_csv_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ----------------------------
        # 3. READ CSV & COUNT CRITERIA
        # ----------------------------
        try:
            df = pd.read_csv(input_csv_path)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid CSV file.")

        if df.shape[1] < 3:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain at least one alternative and two criteria."
            )

        num_criteria = df.shape[1] - 1

        # ----------------------------
        # 4. VALIDATE WEIGHTS & IMPACTS
        # ----------------------------
        weight_list = weights.split(",")
        impact_list = impacts.split(",")

        if len(weight_list) != num_criteria:
            raise HTTPException(
                status_code=400,
                detail=f"Number of weights must be {num_criteria}."
            )

        if len(impact_list) != num_criteria:
            raise HTTPException(
                status_code=400,
                detail=f"Number of impacts must be {num_criteria}."
            )

        for imp in impact_list:
            if imp not in ["+", "-"]:
                raise HTTPException(
                    status_code=400,
                    detail="Impacts must be either '+' or '-'."
                )

        # ----------------------------
        # 5. RUN TOPSIS (SAFE)
        # ----------------------------
        output_csv_path = run_topsis_service(
            uploaded_csv_path=input_csv_path,
            weights=weights,
            impacts=impacts
        )

        # ----------------------------
        # 6. SEND EMAIL IN BACKGROUND
        # ----------------------------
        background_tasks.add_task(
            send_email_with_attachment,
            to_email=email,
            subject="TOPSIS Result File",
            body="Please find attached the TOPSIS result file.",
            attachment_path=output_csv_path
        )

        # ----------------------------
        # 7. RETURN RESPONSE IMMEDIATELY
        # ----------------------------
        return {
            "status": "success",
            "message": "TOPSIS executed successfully. Result will be sent to your email."
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        file.file.close()
