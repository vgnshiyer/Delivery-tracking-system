import React from 'react'
import mapboxgl from 'mapbox-gl';
import { useEffect, useState } from 'react';

function Map({ dummy }) {
    const data = dummy.features[0].geometry.coordinates
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
        let i = 0;
        function loop() {
            setTimeout(() => {
                // Create a DOM element for each marker.
                const el = document.createElement('div');
                el.className = 'marker';
                el.style.backgroundImage = `url(https://cdn3.iconfinder.com/data/icons/flat-badges-vol1/100/63_-512.png)`;
                el.style.width = `30px`;
                el.style.height = `30px`;
                el.style.backgroundSize = '100%';

                // add marker to map
                const m = new mapboxgl.Marker(el)
                    .setLngLat([data[i][0], data[i][1]])
                    .addTo(map);
                i++;
                if (i < 4) {
                    setTimeout(() => {m.remove();}, 3000);
                    loop();
                }
            }, 3000);
        }
        loop();
    }, []);
    return (
        <div className="h-screen max-w-screen-2xl mx-auto" id='my-map' />
    )
}

export default Map