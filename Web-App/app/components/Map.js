import React from 'react'
import mapboxgl from 'mapbox-gl';
import { useEffect, useState } from 'react';

function mark(map, coords, vehicle_name) {
    // console.log(coords)
    if (map.getSource(vehicle_name)) map.removeSource(vehicle_name);
    const mark = map.addSource(vehicle_name, {
        'type': 'geojson',
        'data': {
            'type': 'Feature',
            'properties': {},
            'geometry': {
                'type': 'LineString',
                'coordinates': coords
            }
        }
    });
    //add source for vehicle path tracking

    if (map.getLayer(vehicle_name)) map.removeLayer(vehicle_name);
    map.addLayer({
        'id': vehicle_name,
        'type': 'line',
        'source': vehicle_name,
        'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color': '#FFFF00',
            'line-width': 8
        }
    });
}

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function track(map, vehicle_name, mapMarker, coords) {
    // el = mark(vehicle_name);
    const el = document.createElement('div');
    el.className = 'marker';
    el.style.backgroundImage = "url(/images/" + vehicle_name + ".png)"
    el.style.width = `30px`;
    el.style.height = `30px`;
    el.style.backgroundSize = '100%';

    // Listening to events from api gateway

    // for local development testing
    // var source = new EventSource("http://192.168.29.110:5000/api/vehicles/" + vehicle_name);

    // for production in kubernetes
    var source = new EventSource("http://localhost:3000/api/vehicles/" + vehicle_name);
    source.addEventListener('message', function (e) {
        let res = JSON.parse(e.data.replaceAll(/'/g, '"'));
        // console.log(res);
        for (var i = 0; i < mapMarker.length; i++) {
            // remove previous marker
            mapMarker[i].remove();
            // remove the element from the array too
            mapMarker.splice(i, 1); // uncomment this to save memory..
        }

        // create the popup
        const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(
            '<B style="font-size:13px">' + vehicle_name + '</B>'
        );

        // add marker to map
        const m = new mapboxgl.Marker(el)
            .setLngLat([res.coordinates.latitude, res.coordinates.longitude])
            .setPopup(popup)
            .addTo(map);
        coords.push([res.coordinates.latitude, res.coordinates.longitude])
        // mark(map, coords, vehicle_name);
        mapMarker.push(m);
    }, false);
}

function Map() {
    //map
    const [pageIsMounted, setPageIsMounted] = useState(false)
    mapboxgl.accessToken = 'pk.eyJ1IjoiYnJheDI1MDciLCJhIjoiY2xsYWY1enc3MWo4ZjNsbndnanZjaGdxciJ9.AbY1vj4s-fm7bNUERWBEGg';
    useEffect(() => {
        setPageIsMounted(true)
        const map = new mapboxgl.Map({
            container: 'my-map', // container ID
            style: 'mapbox://styles/brax2507/cl0gk3l6m003714p6cpgngplg/draft', // style URL
            center: [73.21314042281224, 19.140294971985828], // starting position [lng, lat]
            zoom: 9, // starting zoom
            pitch: 50
        });

        // get vehicle names to track
        let vehicles = JSON.parse(httpGet("http://localhost:3000/api/vehicles"))["data"]

        var vars = {};
        var coords = {};
        for (let i = 0; i < vehicles.length; i++) {
            vars[i] = [];
            coords[i] = [];
            track(map, vehicles[i], vars[i], coords[i]);
        }
    }, []);
    return (
        <div className="h-screen max-w-screen-2xl mx-auto" id='my-map' />
    )
}

export default Map