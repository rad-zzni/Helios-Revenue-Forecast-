Member 1: Rad -- Forecasting logic
Member 2: Oscar -- Backend
Member 3: Desmond -- Frontend


---
# How to push your changes using git
Paste the following in your terminal and replace "<changes made>" with the actual changes you made:

```
git add . 
git commit -m "<changes made>"
git push origin main
```

---
# How to pull the updated version of main to work-on using git
Paste the following in your terminal and replace <branch-name> with your branch name.

```
git pull origin <branch-name>
```


---
# How to run
In order to run everything in parallel, paste the following in 3 separate terminals:

Terminal 1:
```
cd frontend && npm start
```

Terminal 2:
```
cd backend && node server.js
```

Terminal 3:
```
cd forecasting && python forecast.py
```