(g => { var h, a, k, p = "The Google Maps JavaScript API", c = "google", l = "importLibrary", q = "__ib__", m = document, b = window; b = b[c] || (b[c] = {}); var d = b.maps || (b.maps = {}), r = new Set, e = new URLSearchParams, u = () => h || (h = new Promise(async (f, n) => { await (a = m.createElement("script")); e.set("libraries", [...r] + ""); for (k in g) e.set(k.replace(/[A-Z]/g, t => "_" + t[0].toLowerCase()), g[k]); e.set("callback", c + ".maps." + q); a.src = `https://maps.${c}apis.com/maps/api/js?` + e; d[q] = f; a.onerror = () => h = n(Error(p + " could not load.")); a.nonce = m.querySelector("script[nonce]")?.nonce || ""; m.head.append(a) })); d[l] ? console.warn(p + " only loads once. Ignoring:", g) : d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n)) })({
    key: "AIzaSyDaq6wN4f_x9ieecytb5srCuLo1665HLS4",
    v: "beta",
    // Use the 'v' parameter to indicate the version to use (weekly, beta, alpha, etc.).
    // Used beta version to use the place autocomplete feature.
    // Add other bootstrap parameters as needed, using camel case.
});


let pos, map, new_search_made=false, new_location_clicked=false;


function isIconMouseEvent(e) {
    return "placeId" in e;
}

class ClickEventHandler {
    origin;
    map;
    directionsService;
    directionsRenderer;
    placesService;
    infowindow;
    infowindowContent;
    find_route_bool;
    get_new_location_bool;
    constructor(map, origin, find_route_bool, get_new_location_bool) {
        this.origin = origin;
        this.map = map;
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(map);
        this.placesService = new google.maps.places.PlacesService(map);
        this.infowindow = new google.maps.InfoWindow();
        this.infowindowContent = document.getElementById("infowindow-content");
        this.infowindow.setContent(this.infowindowContent);
        this.find_route_bool = find_route_bool;
        this.get_new_location_bool = get_new_location_bool;
        // Listen for clicks on the map.
        this.map.addListener("click", this.handleClick.bind(this));
    }
    handleClick(event) {
        console.log("You clicked on: " + event.latLng);
        console.log("origin: " + this.origin.lat + ", " + this.origin.lng);   
        // If the event has a placeId, use it.
        if (isIconMouseEvent(event)) {
            console.log("You clicked on place:" + event.placeId);
            // Calling e.stop() on the event prevents the default info window from
            // showing.
            // If you call stop here when there is no placeId you will prevent some
            // other map click event handlers from receiving the event.
            event.stop();
            if (event.placeId && event.placeId !== this.origin.placeId && this.find_route_bool) {
                this.calculateAndDisplayRoute(event.placeId);
                this.getPlaceInformation(event.placeId);
            }
        }
    }
    calculateAndDisplayRoute(placeId) {
      const me = this;
  
      this.directionsService
        .route({
          origin: this.origin,
          destination: { placeId: placeId },
          travelMode: google.maps.TravelMode.WALKING,
        })
        .then((response) => {
          me.directionsRenderer.setDirections(response);
        })
        .catch((e) => window.alert("Directions request failed due to " + e));
    }
    getPlaceInformation(placeId) {

      this.placesService.getDetails({ placeId: placeId }, (place, status) => {
        if (
          status === "OK" &&
          place &&
          place.geometry &&
          place.geometry.location
        ) {}
      });
    }
}


function getCurrLocation(myfnc, find_route_bool, get_new_location_bool) {
    console.log("getting location");
    if (navigator.geolocation) {
        console.log("geolocation supported");
        navigator.geolocation.getCurrentPosition(
            (position) => {
            pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            };
            myfnc();
            new ClickEventHandler(map, pos, find_route_bool, get_new_location_bool);
            },
            
        );
        
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, map.getCenter());
    }
    

    function handleLocationError(browserHasGeolocation, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(
        browserHasGeolocation
            ? "Error: The Geolocation service failed."
            : "Error: Your browser doesn't support geolocation.",
        );
        infoWindow.open(map);
    }
}


async function initMap(stop_loc_set, map_elm_id, find_route_bool, get_new_location_bool, updating_bool, trip_pos) {
    let infoWindow;
    var markers = [];
    var search_markers = [];
    // Request needed libraries.
    //@ts-ignore
    const { Map } = await google.maps.importLibrary("maps");
    const mapDiv = document.getElementById(map_elm_id);
    const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary("marker");
    const {PlacesService} = await google.maps.importLibrary("places")
    infoWindow = new google.maps.InfoWindow();


    map = new Map(mapDiv, {
        //zoom: 4,
        mapId: "DEMO_MAP_ID",
    });

    


    for (i in stop_loc_set) {
        loc = stop_loc_set[i];
        switch (loc[3]) {
            case "stop":
                background = "#FBBC04";
                borderColor = "#137333";
                glyphColor = "white";
                break;
            case "transport":
                background = "#A1C9FA";
                borderColor = "#137333";
                glyphColor = "white";
                break;
            case "lodging":
                background = "#DE8DF7";
                borderColor = "#137333";
                glyphColor = "white";
                break;
        }
        const pin = new PinElement({
            background: background,
            borderColor: borderColor,
            glyphColor: glyphColor,
        });
        markers.push(new AdvancedMarkerElement({
            map: map,
            position: { lat: loc[0], lng: loc[1] },
            title: loc[2],
            content: pin.element,
        },
        ));
    }
    
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < markers.length; i++) {
        bounds.extend(markers[i].position);
    }

    map.fitBounds(bounds);

    var listener = google.maps.event.addListener(map, "idle", function() { 
        if (map.getZoom() > 16) map.setZoom(16); 
        google.maps.event.removeListener(listener); 
        if (stop_loc_set.length==0) {
            map.setCenter({lat:trip_pos.ltd, lng:trip_pos.lng});
            console.log("trip pos: ", trip_pos);
            console.log("centered at :", {lat:trip_pos.ltd, lng:trip_pos.lng});
        }
    });

    
    function getPosFunction() {
        console.log(pos);
        console.log("find route bool: ",find_route_bool);
        console.log("get location bool: ", get_new_location_bool);
        if(stop_loc_set.length == 0) {
            console.log("no stop loc set");
            map.setCenter(pos);
        }
        
    }
    getCurrLocation(getPosFunction, find_route_bool, get_new_location_bool); //Also assigns current location to pos

    if(stop_loc_set.length == 0) {
        console.log("no stop loc set");
        map.setCenter(pos);
    }

    if(get_new_location_bool){
        map.addListener("click", (mapsMouseEvent) => {
            
            console.log("click event");
            
            if(updating_bool || new_location_clicked){
                markers[markers.length-1].setMap(null);
                markers.pop();
            }
            
            position = mapsMouseEvent.latLng;
            console.log("see: ", mapsMouseEvent.placeId);
            if(updating_bool) {
                switch (stop_loc_set[0][3]) {
                    case "stop":
                        background = "#FBBC04";
                        borderColor = "#137333";
                        glyphColor = "white";
                        break;
                    case "transport":
                        background = "#A1C9FA";
                        borderColor = "#137333";
                        glyphColor = "white";
                        break;
                    case "lodging":
                        background = "#DE8DF7";
                        borderColor = "#137333";
                        glyphColor = "white";
                        break;
                }
                const pin = new PinElement({
                    background: background,
                    borderColor: borderColor,
                    glyphColor: glyphColor,});
                
                markers.push(new AdvancedMarkerElement({
                    map: map,
                    position: position,
                    title: "new stop",
                    content: pin.element,
                },
                ));
            }
            else{
                const pin = new PinElement();

                markers.push(new AdvancedMarkerElement({
                    map: map,
                    position: position,
                    title: "new stop",
                    content: pin.element,
                },
                ));
            }
            
            document.getElementById("ltd-field").value = position.lat();
            document.getElementById("lng-field").value = position.lng();
            new_location_clicked = true;
            console.log("new loc: ", position.lat(), position.lng());
        });


        const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement({
            locationBias: {radius: 100, center: {lat:trip_pos.ltd, lng:trip_pos.lng}},
        });
        placeAutocomplete.id = "place-autocomplete-input";
        const card = document.getElementById("place-autocomplete-card");
        card.appendChild(placeAutocomplete);
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(card);

        placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
            if(new_search_made) {
                search_markers[search_markers.length-1].setMap(null);
                search_markers.pop();
            }
            await place.fetchFields({
            fields: ["displayName", "formattedAddress", "location"],
            });
            // If the place has a geometry, then present it on a map.
            if (place.viewport) {
            map.fitBounds(place.viewport);
            } else {
            map.setCenter(place.location);
            map.setZoom(17);
            }
        
            search_markers.push(new AdvancedMarkerElement({
                map: map,
                position: place.location,
                title: place.displayName
            }));
            new_search_made = true;
            console.log("bias towards: ", trip_pos);
        });
    }

    console.log("find_route_bool: ", find_route_bool);
    console.log("get_new_location_bool: ", get_new_location_bool);
    console.log("stop_loc_set len: ", stop_loc_set.length);
    
    
}

async function initSearch() {
    // Request needed libraries.
    //@ts-ignore
    await google.maps.importLibrary("places");
  
    // Create the input HTML element, and append it.
    //@ts-ignore
    const placeAutocomplete = new google.maps.places.PlaceAutocompleteElement();
  
    //@ts-ignore
    document.getElementById("place-autocomplete-card").appendChild(placeAutocomplete);
  
    // Inject HTML UI.
    const selectedPlaceTitle = document.createElement("p");
  
    selectedPlaceTitle.textContent = "";
    document.body.appendChild(selectedPlaceTitle);
  
    const selectedPlaceInfo = document.createElement("pre");
  
    selectedPlaceInfo.textContent = "";
    document.body.appendChild(selectedPlaceInfo);
    // Add the gmp-placeselect listener, and display the results.
    //@ts-ignore
    placeAutocomplete.addEventListener("gmp-placeselect", async ({ place }) => {
      await place.fetchFields({
        fields: ["displayName", "formattedAddress", "location"],
      });

        document.getElementById("ltd-field").value = place.location.lat();
        document.getElementById("lng-field").value = place.location.lng();
        document.getElementById("loc-name-field").value = place.displayName;
        document.getElementById("loc-id-field").value = place.id;
        document.getElementById("formatted-address-field").value = place.formattedAddress;

    });
    




}
  
