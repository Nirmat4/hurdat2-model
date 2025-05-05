import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_path='../database/atlantico-1851-2024.txt'

records=[]
with open(file_path, 'r') as f:
    storm_id=None
    storm_name=None

    for line in f:
        parts=[p.strip() for p in line.strip().split(',')]

        
        if parts[0].startswith(('AL','EP')) and len(parts) >= 3:
            storm_id=parts[0]
            storm_name=parts[1]
            continue

        
        if storm_id and len(parts) >= 8:
            date_str=parts[0]   
            time_str=parts[1]   
            status=parts[3]   

            
            year=int(date_str[0:4])
            month=int(date_str[4:6])
            day=int(date_str[6:8])
            hour=int(time_str[0:2])

            
            lat=float(parts[4][:-1])
            lon=float(parts[5][:-1])*(-1 if parts[5].endswith('W') else 1)

            
            wind_knots=int(parts[6])
            pressure_mb=int(parts[7]) if parts[7] != '-999' else None

            records.append({
                'storm_id':   storm_id,
                'name':       storm_name,
                'year':       year,
                'month':      month,
                'day':        day,
                'hour':       hour,
                'status':     status,
                'lat':        lat,
                'lon':        lon,
                'wind_knots': wind_knots,
                'pressure_mb':pressure_mb
            })



df=pd.DataFrame(records)
df['datetime']=pd.to_datetime(df[['year','month','day','hour']].apply(
    lambda r: f"{r['year']:04d}-{r['month']:02d}-{r['day']:02d} {r['hour']:02d}:00", axis=1
))

df.to_csv('test.csv', index=False)



storm_id_example='AL022023'

storm=df[df['storm_id'] == storm_id_example]

if storm.empty:
    print(f"⚠️ No se encontró la tormenta con ID {storm_id_example}")
else:
    plt.figure(figsize=(10,6))
    plt.plot(storm['lon'], storm['lat'], marker='o')
    plt.title(f'Trayectoria de {storm_id_example} ({storm["name"].iloc[0]})')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.show()



plt.figure(figsize=(8, 6))
plt.plot(storm['lon'], storm['lat'], marker='o', linewidth=2)
plt.scatter(storm['lon'], storm['lat'], c=storm['wind_knots'], cmap='viridis')
plt.colorbar(label='Viento máximo sostenido (nudos)')
plt.title(f'Tráyectoria de {storm_id_example} ({storm["name"].iloc[0]})')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.grid(True)
plt.show()



plt.figure()
plt.hist(df['wind_knots'], bins=range(0, 200, 10))
plt.title('Distribución de vientos máximos sostenidos')
plt.xlabel('Viento (nudos)')
plt.ylabel('Frecuencia')
plt.show()


plt.figure()
plt.plot(storm['datetime'], storm['pressure_mb'], marker='x')
plt.title(f'Evolución de la presión central de {storm_id_example}')
plt.xlabel('Fecha y hora')
plt.ylabel('Presión (mb)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


if not storm.empty:
    plt.figure(figsize=(12, 8))

    ax=plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([-100, -10, 0, 50])  

    
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')

    
    ax.plot(storm['lon'], storm['lat'], marker='o', color='red', transform=ccrs.PlateCarree())

    
    plt.title(f'Trayectoria de {storm_id_example} ({storm["name"].iloc[0]})')
    plt.show()
