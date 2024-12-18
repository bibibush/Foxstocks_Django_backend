import random

dayData = [{"day":str(i),"price":random.randint(530,560)*100} for i in range(1,31+1)]

weekData = [{"week":str(w), "price": random.randint(530,570)*100} for w in range(1,25 + 1)]

months = ["Jan","Feb","Mar","Avr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthData = [{"month":m,"price":random.randint(530,580)*100} for m in months]

yearData = [{"year": str(y), "price":random.randint(530,600)*100} for y in range(2014,2024 + 1)]
