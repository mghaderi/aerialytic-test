import React, { useState } from 'react';
import { CalculationResult } from '../types/types';

interface Props {
    latitude: string;
    longitude: string;
    setLatitude: (lat: string) => void;
    setLongitude: (lng: string) => void;
    onResult: (result: CalculationResult) => void;
    onError: (error: string) => void;
    setLoading: (loading: boolean) => void;
    setMapPosition: (lat: number, lng: number) => void;
}

// FormComponent collects user input and triggers the backend calculation
const FormComponent: React.FC<Props> = ({
    latitude,
    longitude,
    setLatitude,
    setLongitude,
    onResult,
    onError,
    setLoading,
    setMapPosition,
}) => {
    // Local state for optional offset angle
    const [offsetAngle, setOffsetAngle] = useState<string>('');

    // Handle form submission: validate inputs and make API call
    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        onError('');
        onResult(null as any);
        setLoading(true);

        // Parse numeric values from input strings
        const latNum = Number(latitude);
        const lngNum = Number(longitude);
        const offsetNum = offsetAngle !== '' ? Number(offsetAngle) : null;

        // === Input Validation ===
        if (isNaN(latNum) || latNum < -90 || latNum > 90) {
            onError('Please enter valid latitude (-90 to 90)');
            setLoading(false);
            return;
        }
        if (isNaN(lngNum) || lngNum < -180 || lngNum > 180) {
            onError('Please enter valid longitude (-180 to 180)');
            setLoading(false);
            return;
        }
        if (offsetAngle !== '' && (isNaN(offsetNum!) || offsetNum! < 0 || offsetNum! > 90)) {
            onError('Please enter valid Offset Angle (0 to 90)');
            setLoading(false);
            return;
        }

        try {
            // Prepare payload for backend
            const data = {
                latitude: latNum,
                longitude: lngNum,
                ...(offsetNum !== null && { offset_angle: offsetNum }),
            };

            // Send POST request to backend API
            const res = await fetch('/api/calculate/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });

            if (!res.ok) throw new Error('Something went wrong. Try again.');

            // Parse and handle result
            const result = await res.json();
            onResult(result);
            setMapPosition(latNum, lngNum);
        } catch (e: any) {
            onError(e.message || 'Something went wrong. Try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="input-form">
            <div className="form-group">
                <label htmlFor='latitude'>Latitude:</label>
                <input id='latitude' type="number" value={latitude} onChange={(e) => setLatitude(e.target.value)} step="any" required />
            </div>
            <div className="form-group">
                <label htmlFor='longitude'>Longitude:</label>
                <input id='longitude' type="number" value={longitude} onChange={(e) => setLongitude(e.target.value)} step="any" required />
            </div>
            <div className="form-group">
                <label htmlFor='offest'>Offset Angle (optional):</label>
                <input id='offest' type="number" value={offsetAngle} onChange={(e) => setOffsetAngle(e.target.value)} step="any" />
            </div>
            <button type="submit">Calculate Optimal Angles</button>
        </form>
    );
};

export default FormComponent;
