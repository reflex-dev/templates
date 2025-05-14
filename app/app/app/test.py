from starlette.responses import JSONResponse


async def test(request):
    """
    Test function to check if the application is running.
    """
    print("hi")
    return JSONResponse({"message": "Test successful!"})
