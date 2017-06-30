/* Leaflet */

var geo = {
	BS3:  {lat: 33.645323, long: -117.846083, name: "Biological Sciences III"},
	DBH:  {lat: 33.643259, long: -117.841978, name: "Donald Bren Hall"},
	EH:   {lat: 33.643764, long: -117.841012, name: "Engineering Hall"},
	ELH:  {lat: 33.644470, long: -117.840714, name: "Engineering Lecture Hall"},
	HG:   {lat: 33.648247, long: -117.844513, name: "Humanities Gateway"},
	HH:   {lat: 33.647330, long: -117.843980, name: "Humanities Hall"},
	HIB:  {lat: 33.648412, long: -117.843832, name: "Humanities Instructional Building"},
	HICF: {lat: 33.646874, long: -117.846804, name: "Humanities Interim Classroom Facility"},
	HSLH: {lat: 33.645587, long: -117.844662, name: "Howard Schneiderman Lecture Hall"},
	IAB:  {lat: 33.648219, long: -117.845335, name: "Intercollegiate Athletics Building"},
	ICF:  {lat: 33.644433, long: -117.839968, name: "Interim Classroom Facility"},
	ICS:  {lat: 33.644283, long: -117.841800, name: "Information & Computer Science"},
	LLIB: {lat: 33.647132, long: -117.841093, name: "Langson Library"},
	MM:   {lat: 33.649325, long: -117.844454, name: "Music & Media Building"},
	MPAA: {lat: 33.647068, long: -117.836951, name: "Multipurpose Academic & Administrative Building"},
	MSTB: {lat: 33.642084, long: -117.844415, name: "Multipurpose Science & Technology Building"},
	PCB:  {lat: 33.644509, long: -117.842806, name: "Parkview Classroom Building"},
	PSCB: {lat: 33.643407, long: -117.843494, name: "Physical Sciences Classroom Building"},
	PSLH: {lat: 33.643399, long: -117.843958, name: "Physical Sciences Lecture Hall"},
	RH:   {lat: 33.644508, long: -117.844120, name: "Rowland Hall"},
	SBSG: {lat: 33.647374, long: -117.839088, name: "Social & Behavioral Sciences Gateway"},
	SE:   {lat: 33.646151, long: -117.838889, name: "Social Ecology I"},
	SE2:  {lat: 33.646556, long: -117.839149, name: "Social Ecology II"},
	SH:   {lat: 33.646210, long: -117.844836, name: "Steinhaus Hall"},
	SSH:  {lat: 33.646225, long: -117.840065, name: "Social Science Hall"},
	SSL:  {lat: 33.645902, long: -117.839999, name: "Social Science Lab"},
	SSLH: {lat: 33.647227, long: -117.839731, name: "Social Science Lecture Hall"},
	SSPA: {lat: 33.646939, long: -117.839552, name: "Social Science Plaza A"},
	SST:  {lat: 33.646456, long: -117.840271, name: "Social Science Tower"},
	SSTR: {lat: 33.646983, long: -117.840235, name: "Social Science Trailer"}
};

var mymap = L.map("bldgs").setView([33.64625, -117.84215], 16);
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw", {
	maxZoom: 18,
	id: "mapbox.streets"
}).addTo(mymap);
var key = Object.keys(geo);
for (var i = 0, e; e = geo[key[i]]; i++) {
	var marker = L.marker([e.lat, e.long]).bindPopup(e.name).addTo(mymap);
}

mymap.locate({watch: true})
.on("locationfound", function(e){
    var marker = L.marker([e.latitude, e.longitude]).bindPopup("You are here. :)").addTo(mymap);
    var circle = L.circle([e.latitude, e.longitude], e.accuracy / 2, {
        weight: 1,
        color: "blue",
        fillColor: "#cacaca",
        fillOpacity: 0.5
    }).addTo(mymap);
})
.on("locationerror", function(e){
    console.log(e);
});

/* Data Tables */
$("#hmm").DataTable();