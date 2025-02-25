run:
	npx @tailwindcss/cli -i ./styles/app.css -o ./static/css/app.css
	@uvicorn main:app --reload --host 0.0.0.0 --port 1234

dev:
	@uvicorn main:app --reload --host 0.0.0.0 --port 1234

css:
	npx @tailwindcss/cli -i ./styles/app.css -o ./static/css/app.css --watch
