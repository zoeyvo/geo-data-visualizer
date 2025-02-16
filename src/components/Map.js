// import { LitElement, html, css } from "lit";
// import L from "leaflet";
// import "leaflet/dist/leaflet.css";

// class MapComponent extends LitElement {
//     static styles = css`
//         .map {
//             width: 100%;
//             height: 100vh;
//             min-height: 300px;
            
//         }
//     `;

    
//     firstUpdated() {
//         this.updateComplete.then(() => {
//             const mapContainer = this.shadowRoot.querySelector(".map");
//             if (!mapContainer) {
//                 console.error("Map container not found!");
//                 return;
//             }
    
//             this.map = L.map(mapContainer).setView([20, 0], 2);
//             L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
//                 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
//             }).addTo(this.map);
    
//         });
//     }

   
//     render() {
//         return html`<div class="map"></div>`;
//     }
// }

// customElements.define("map-component", MapComponent);



import { LitElement, html, css } from "lit";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

class MapComponent extends LitElement {
    static styles = css`
        .map {
            width: 100%;
            height: 100vh;
            min-height: 300px;
        }
    `;

    firstUpdated() {
        console.log("🌍 Initializing Map...");

        const mapContainer = this.shadowRoot.querySelector(".map");
        if (!mapContainer) {
            console.error("❌ Map container not found!");
            return;
        }

        this.map = L.map(mapContainer).setView([20, 0], 2);

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.map);
    }

    render() {
        return html`<div class="map"></div>`;
    }
}

customElements.define("map-component", MapComponent);
