import React, { useState, useCallback, useEffect } from 'react';

// Layout wrapper for consistent page structure
import Layout from './layouts/Index';

// Form for user input (latitude, longitude, offset angel)
import FormComponent from './components/Form';

// Component to display calculation results
import Calculators from './components/Calculators';

// Google Map component to show location and handle clicks
import MapComponent from './components/Map';

// Types for calculation results
import { CalculationResult } from './types/types';

import './App.css';


function App() {
    // State for form inputs
    const [latitude, setLatitude] = useState<string>('43.65');
    const [longitude, setLongitude] = useState<string>('-79.38');

    // Result returned from API after calculation
    const [result, setResult] = useState<CalculationResult | null>(null);

    // Error message and loading indicator
    const [error, setError] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false);

    // Map state: center and marker position
    const [mapCenter, setMapCenter] = useState({ lat: 43.65, lng: -79.38 });
    const [markerPosition, setMarkerPosition] = useState<{ lat: number; lng: number } | null>({ lat: 43.65, lng: -79.38 });

    // Map API key from environment variable
    const apiKey = process.env.REACT_APP_Maps_API_KEY;

    // Handle map click: update form values based on selected coordinates
    const handleMapClick = useCallback((e: any) => {
        if (e.detail?.latLng) {
            const { lat, lng } = e.detail.latLng;
            setLatitude(lat.toString());
            setLongitude(lng.toString());
        }
    }, []);

    // Sync map center and marker when form inputs are updated (and valid)
    useEffect(() => {
        const latNum = Number(latitude);
        const lngNum = Number(longitude);
        const isValidLat = !isNaN(latNum) && latNum >= -90 && latNum <= 90;
        const isValidLng = !isNaN(lngNum) && lngNum >= -180 && lngNum <= 180;
        if (latitude !== '' && isValidLat && longitude !== '' && isValidLng) {
            setMapCenter({ lat: latNum, lng: lngNum });
            setMarkerPosition({ lat: latNum, lng: lngNum });
        }
    }, [latitude, longitude]);

    return (
        <Layout>
            <FormComponent
                latitude={latitude}
                longitude={longitude}
                setLatitude={setLatitude}
                setLongitude={setLongitude}
                onResult={setResult}
                onError={setError}
                setLoading={setLoading}
            />
            {loading && <p>Loading...</p>}
            {error && <p className="error-message">{error}</p>}
            {result && <Calculators result={result} />}
            <MapComponent center={mapCenter} marker={markerPosition} onClick={handleMapClick} apiKey={apiKey} />
        </Layout>
    );
}

export default App;
