import React from 'react'
import mapboxgl from 'mapbox-gl';
import { useEffect, useState } from 'react';

function mark(vehicle_name) {
    // Create a DOM element for each marker.
    const el = document.createElement('div');
    el.className = 'marker';
    if (vehicle_name === "cargo-delivery-truck") {
        el.style.backgroundImage = `url(images/truck1.png)`;
    } else {
        el.style.backgroundImage = `url(images/truck2.png)`;
    }
    el.style.width = `30px`;
    el.style.height = `30px`;
    el.style.backgroundSize = '100%';
    return el;
}

function track(map, vehicle_name,mapMarker) {
    // el = mark(vehicle_name);
    const el = document.createElement('div');
    el.className = 'marker';
    if (vehicle_name === "cargo-delivery-truck") {
        el.style.backgroundImage = "url(https://cdn3.iconfinder.com/data/icons/flat-badges-vol1/100/63_-512.png)";
    } else {
        el.style.backgroundImage = "url(https://cdn-icons-png.flaticon.com/512/2555/2555001.png)";
    }
    el.style.width = `30px`;
    el.style.height = `30px`;
    el.style.backgroundSize = '100%';
    // Listening to events from api gateway
    var source = new EventSource("http://192.168.29.110:5000/api/vehicles/" + vehicle_name);
    source.addEventListener('message', function (e) {
        let res = JSON.parse(e.data);
        console.log(res);
        for (var i = 0; i < mapMarker.length; i++) {
            // remove previous marker
            mapMarker[i].remove();
            // remove the element from the array too
            mapMarker.splice(i, 1); // comment this to save memory..
        }
        // add marker to map
        const m = new mapboxgl.Marker(el)
            .setLngLat([res.coordinates.latitude, res.coordinates.longitude])
            .addTo(map);
        mapMarker.push(m);
    }, false);
}

function Map() {
    //map
    const [pageIsMounted, setPageIsMounted] = useState(false)
    mapboxgl.accessToken = 'pk.eyJ1IjoiYnJheDI1MDciLCJhIjoiY2t4azgyOXBxNmRwaDJ1cTNjMGRqcjF3ZCJ9.0pJi--39nsT8km17AeiY3g';
    useEffect(() => {
        setPageIsMounted(true)
        const map = new mapboxgl.Map({
            container: 'my-map', // container ID
            style: 'mapbox://styles/brax2507/cl0gk3l6m003714p6cpgngplg/draft', // style URL
            center: [73.21314042281224, 19.140294971985828], // starting position [lng, lat]
            zoom: 9 // starting zoom
        });

        let vehicles = ["cargo-delivery-truck", "nano-delivery-truck"];
        var vars = {};
        for (let i = 0; i < vehicles.length; i++) {
            vars[i] = [];
            track(map, vehicles[i], vars[i]);
        }
    }, []);
    return (
        <div className="h-screen max-w-screen-2xl mx-auto" id='my-map' />
    )
}

export default Map