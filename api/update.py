def handler(request, response):
    response.status_code = 200
    response.send("✅ Vercel found update.py")
