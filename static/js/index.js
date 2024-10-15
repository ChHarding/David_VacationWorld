var mapboxapi = "{{ MAPBOX_API_KEY }}";
mapboxgl.accessToken = mapboxapi;
const map = new mapboxgl.Map({
  container: "map",
  style: "mapbox://styles/mapbox/streets-v12",
  center: [0, 0],
  zoom: 2,
});
map.addControl(new mapboxgl.NavigationControl());

const geocoder = new MapboxGeocoder({
  accessToken: mapboxgl.accessToken,
  mapboxgl: mapboxgl,
  marker: false,
  placeholder: "Search for places",
});

// Add navigation controls
map.addControl(geocoder);

// Store all markers in an array
let markers = [];

// Function to add a pin
function addPin(lng, lat, title) {
  const marker = new mapboxgl.Marker({
    draggable: true,
  })
    .setLngLat([lng, lat])
    .addTo(map);

  const popupContent = `
          <h3>${title}</h3>
          <button onclick="editPinName(${markers.length})">Edit</button>
          <button onclick="deletePin(${markers.length})">Delete</button>
      `;

  const popup = new mapboxgl.Popup().setHTML(popupContent);
  marker.setPopup(popup);

  markers.push({ marker, title });
  return marker;
}

// Function to edit pin name
function editPinName(index) {
  const newTitle = prompt(
    "Enter new name for this location:",
    markers[index].title
  );
  if (newTitle) {
    markers[index].title = newTitle;
    const popupContent = `
              <h3>${newTitle}</h3>
              <button onclick="editPinName(${index})">Edit</button>
              <button onclick="deletePin(${index})">Delete</button>
          `;
    markers[index].marker.getPopup().setHTML(popupContent);
  }
}

// Function to delete pin
function deletePin(index) {
  if (confirm("Are you sure you want to delete this pin?")) {
    markers[index].marker.remove();
    markers.splice(index, 1);
    // Update remaining markers' popup content to reflect new indices
    markers.forEach((marker, i) => {
      const popupContent = `
                  <h3>${marker.title}</h3>
                  <button onclick="editPinName(${i})">Edit</button>
                  <button onclick="deletePin(${i})">Delete</button>
              `;
      marker.marker.getPopup().setHTML(popupContent);
    });
  }
}

// Example: Add some sample pins
map.on("load", () => {
  addPin(-74.006, 40.7128, "New York City");
  addPin(2.3522, 48.8566, "Paris");
  addPin(139.6917, 35.6895, "Tokyo");
});

// function to search for a location, fly to it and create pin
geocoder.on("result", function (e) {
  const coordinates = e.result.center;
  const placeName = e.result.place_name;

  // Add a pin for the selected location
  addPin(coordinates[0], coordinates[1], placeName);

  // Fly to the selected location
  map.flyTo({
    center: coordinates,
    zoom: 14,
  });
});

// Add click event to add new pins
map.on("click", (e) => {
  const title = prompt("Enter a name for this location:");
  if (title) {
    addPin(e.lngLat.lng, e.lngLat.lat, title);
  }
});

const secondsPerRevolution = 120;
// Above zoom level 5, do not rotate.
const maxSpinZoom = 5;
// Rotate at intermediate speeds between zoom levels 3 and 5.
const slowSpinZoom = 3;

let userInteracting = false;
let spinEnabled = true;

function spinGlobe() {
  const zoom = map.getZoom();
  if (spinEnabled && !userInteracting && zoom < maxSpinZoom) {
    let distancePerSecond = 360 / secondsPerRevolution;
    if (zoom > slowSpinZoom) {
      // Slow spinning at higher zooms
      const zoomDif = (maxSpinZoom - zoom) / (maxSpinZoom - slowSpinZoom);
      distancePerSecond *= zoomDif;
    }
    const center = map.getCenter();
    center.lng -= distancePerSecond;
    // Smoothly animate the map over one second.
    // When this animation is complete, it calls a 'moveend' event.
    map.easeTo({ center, duration: 1000, easing: (n) => n });
  }
}

map.on("mousedown", () => {
  userInteracting = true;
});

// Restart spinning the globe when interaction is complete
map.on("mouseup", () => {
  userInteracting = false;
  spinGlobe();
});

// These events account for cases where the mouse has moved
// off the map, so 'mouseup' will not be fired.
map.on("dragend", () => {
  userInteracting = false;
  spinGlobe();
});
map.on("pitchend", () => {
  userInteracting = false;
  spinGlobe();
});
map.on("rotateend", () => {
  userInteracting = false;
  spinGlobe();
});

// When animation is complete, start spinning if there is no ongoing interaction
map.on("moveend", () => {
  spinGlobe();
});

map.addLayer({
  id: "pins",
  type: "symbol",
  source: "pins",
  layout: {
    "text-field": ["get", "name"],
    "text-allow-overlap": true,
  },
});

spinGlobe();
