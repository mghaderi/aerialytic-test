import { APIProvider, Map, Marker, useMap } from '@vis.gl/react-google-maps';
import { useRef, useEffect } from 'react';

// Internal component to pan the map when `center` changes
const PanToCenter: React.FC<{ center: { lat: number; lng: number } }> = ({ center }) => {
    const map = useMap();

    useEffect(() => {
        if (map && center) {
            map.panTo(center);
        }
    }, [center, map]);

    return null;
};

interface Props {
    center: { lat: number; lng: number };
    marker: { lat: number; lng: number } | null;
    onClick: (e: any) => void;
    apiKey: string | undefined;
}

// MapComponent renders the Google Map with marker and handles center updates
const MapComponent: React.FC<Props> = ({ center, marker, onClick, apiKey }) => {
    const mapRef = useRef<google.maps.Map | null>(null);

    useEffect(() => {
        if (mapRef.current) {
            mapRef.current.panTo(center);
        }
    }, [center]);

    // Display fallback if API key is missing
    if (!apiKey) {
        return <p className="error-message">Google Maps API key not found or invalid.</p>;
    }

    return (
        <APIProvider apiKey={apiKey}>
            <div className="map-container" data-testid="map-container">
                <Map
                    defaultCenter={center}
                    defaultZoom={10}
                    gestureHandling="greedy"
                    onClick={onClick}
                >
                    <PanToCenter center={center} />
                    {marker && <Marker position={marker} />}
                </Map>
            </div>
        </APIProvider>
    );
};

export default MapComponent;
