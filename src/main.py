from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from tests.util import get_all_src_py_files_hash
from src.api import api_router
from src.users.errors import MissingValueException
from src.common.custom_exception import CustomException

app = FastAPI()

app.include_router(api_router)

@app.exception_handler(CustomException)
def handle_custom_exception(request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.error_code,
            "error_msg": exc.error_message
        }
    )
    
@app.exception_handler(RequestValidationError)
def handle_request_validation_error(request, exc):
    err = MissingValueException()
    return JSONResponse(
        status_code=err.status_code,
        content={
            "error_code": err.error_code,
            "error_msg": err.error_message
        }
    )

@app.get("/health")
def health_check():
    # 서버 정상 배포 여부를 확인하기 위한 엔드포인트입니다.
    # 본 코드는 수정하지 말아주세요!
    hash = get_all_src_py_files_hash()
    return {
        "status": "ok",
        "hash": hash
    }
