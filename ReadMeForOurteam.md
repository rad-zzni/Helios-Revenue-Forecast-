Member 1: Rad -- Forecasting logic
Member 2: Oscar -- Backend
Member 3: Desmond -- Frontend


---
# How to push your changes using git
Make sure you are working on your own branch. Replace `<your-branch>` and `<changes made>` with the appropriate values:

```
git add .
git commit -m "<changes made>"
git push origin <your-branch>
```

---
# How to pull the updated version of main to work on
Run this to update your local main branch:

```
git checkout main
git pull origin main
```

Then switch back to your branch and merge the new changes:

```
git checkout <your-branch>
git merge main
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