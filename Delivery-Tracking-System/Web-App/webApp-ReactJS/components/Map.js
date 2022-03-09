import React from 'react'
import mapboxgl from 'mapbox-gl';
import { useEffect, useState } from 'react';

function track(map, vehicle_name) {
    // Create a DOM element for each marker.
    const el = document.createElement('div');
    el.className = 'marker';
    el.style.backgroundImage = `url(https://cdn3.iconfinder.com/data/icons/flat-badges-vol1/100/63_-512.png)`;
    el.style.width = `30px`;
    el.style.height = `30px`;
    el.style.backgroundSize = '100%';

    // Listening to events from api gateway
    mapMarker1 = [];
    var source = newEventSource("http://api-gateway:5000/api/vechicles/cargo-delivery-truck");
    source.addEventListener('message', function (e) {
        data = JSON.parse(e.data);
        console.log(data);
        for (var i = 0; i < mapMarker1.length; i++) {
            // remove previous marker
            mapMarker1[i].remove();
            // remove the element from the array too
            //mapMarker1.splice(i,1);
        }
        // add marker to map
        const m = new mapboxgl.Marker(el)
            .setLngLat([data.latitude, data.longitude])
            .addTo(map);
        mapMarker1.push(m);
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

        

        track(map, vehicle_name);
    }, []);
    return (
        <div className="h-screen max-w-screen-2xl mx-auto" id='my-map' />
    )
}

export default Map