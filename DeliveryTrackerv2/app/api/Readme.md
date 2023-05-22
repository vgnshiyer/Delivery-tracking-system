# Delivery Tracking System

## BEFORE YOU BEGIN

All Responses will have the following format

```json
{
    "data" : "Content of type json"
}
```

### List of vehicles

**Definition**

`GET /vehicles`

**Response**

- `200 OK` on success

```json
{
    "data" : [ "vehicle1", "vehicle2" ]
}
```

### Lookup latest vehicle coordinates

**Definition**

`GET /vehicles/<str:vehiclename>`

**Arguments**

- `"vehiclename : str"` Name of the vehicle

**Response**

- `200 OK` on success
- `404 NOT FOUND` if vehicle does not exist

```json
{
    "data": {
        "truck-type": "cargo",
        "truck-number": "7",
        "timestamp": "19/12/2021 09:52:35",
        "coordinates": { 
            "latitude": "72.9715347290039", 
            "longitude": "19.1967292074432"
        }
    }
}
```
